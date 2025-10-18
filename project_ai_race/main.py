"""Entry point for the PDF extraction and QA pipeline."""
from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import pandas as pd
from tqdm import tqdm

from .extraction.formula_extractor import extract_formulas
from .extraction.table_extractor import extract_tables
from .extraction.text_extractor import extract_paragraphs
from .postprocessing.markdown_converter import to_markdown
from .postprocessing.validator import validate
from .preprocessing.pdf_loader import load_pdf_paths, open_pdf
from .qa.answer_selector import select_answers
from .qa.indexer import VectorIndex, build_index
from .qa.question_parser import parse_questions
from .qa.retriever import retrieve
from .utils.file_handler import ensure_dir, read_text, write_text
from .utils.logger import configure_logging


@dataclass
class ExtractedDocument:
    """Container for extracted document artifacts."""

    name: str
    markdown_path: Path
    markdown_content: str
    warnings: List[str]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PDF extraction and QA pipeline.")
    parser.add_argument(
        "--stage",
        required=True,
        choices=["extraction", "qa", "evaluate"],
        help="Pipeline stage to execute.",
    )
    parser.add_argument(
        "--input_dir",
        type=Path,
        default=Path("data/input"),
        help="Directory containing input PDFs or extracted artifacts.",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=Path("data/output"),
        help="Target directory for extracted markdown and answer.md.",
    )
    parser.add_argument(
        "--questions",
        type=Path,
        help="CSV file with multiple choice questions (required for stage=qa).",
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=5,
        help="Number of passages to retrieve for each question.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.35,
        help="Base threshold for multi-label answer selection.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR).",
    )
    return parser.parse_args()


def extract_single_pdf(pdf_path: Path, output_root: Path) -> ExtractedDocument:
    """Process a single PDF into structured markdown output."""
    logging.info("Extracting %s", pdf_path.name)
    document_dir = ensure_dir(output_root / pdf_path.stem)
    images_dir = ensure_dir(document_dir / "images")

    pages_payload: List[Dict[str, object]] = []
    metadata: Dict[str, object] = {"title": pdf_path.stem}

    with open_pdf(pdf_path) as pdf:
        if pdf.metadata and pdf.metadata.get("Title"):
            metadata["title"] = pdf.metadata["Title"]

        for page in pdf.pages:
            paragraphs = extract_paragraphs(page)
            tables = extract_tables(page)
            formulas = extract_formulas(page)

            images: List[str] = []
            for idx, _ in enumerate(getattr(page, "images", [])):
                placeholder_name = f"{pdf_path.stem}_p{page.page_number}_img{idx}.txt"
                placeholder_path = images_dir / placeholder_name
                if not placeholder_path.exists():
                    placeholder_path.write_text(
                        "Image placeholder generated during extraction.\n",
                        encoding="utf-8",
                    )
                images.append(f"images/{placeholder_name}")

            pages_payload.append(
                {
                    "page_number": page.page_number,
                    "paragraphs": paragraphs,
                    "tables": tables,
                    "formulas": formulas,
                    "images": images,
                }
            )

    structured_document: Dict[str, object] = {
        "document_name": pdf_path.stem,
        "metadata": metadata,
        "pages": pages_payload,
    }

    warnings = validate(structured_document)
    for warning in warnings:
        logging.warning("%s: %s", pdf_path.name, warning)

    markdown_content = to_markdown(structured_document)
    markdown_path = document_dir / "main.md"
    write_text(markdown_path, markdown_content)

    return ExtractedDocument(
        name=pdf_path.stem,
        markdown_path=markdown_path,
        markdown_content=markdown_content,
        warnings=warnings,
    )


def render_task_extract(documents: Sequence[ExtractedDocument]) -> str:
    """Render the TASK EXTRACT section for answer.md."""
    if not documents:
        return "### TASK EXTRACT\n\n_No documents were extracted._\n"

    sections: List[str] = ["### TASK EXTRACT", ""]
    for doc in documents:
        sections.append(doc.markdown_content.strip())
        sections.append("")
    return "\n".join(sections).strip() + "\n"


def render_task_qa(results: Sequence[Dict[str, object]]) -> str:
    """Render the TASK QA section for answer.md."""
    lines: List[str] = ["### TASK QA", ""]
    if not results:
        lines.append("_No QA predictions were generated._")
        return "\n".join(lines).strip() + "\n"

    for idx, result in enumerate(results, start=1):
        selections = result.get("selected", [])
        labels = [label for label, _ in selections]
        label_text = ", ".join(labels) if labels else "None"
        score_text = ", ".join(f"{label}:{score:.3f}" for label, score in selections) if selections else "n/a"

        lines.append(
            f"- Question {idx}: count={len(labels)} answers={label_text} (scores: {score_text})"
        )
    lines.append("")
    return "\n".join(lines).strip() + "\n"


def merge_answer_sections(answer_path: Path, *, extract_section: str | None = None, qa_section: str | None = None) -> None:
    """Combine TASK EXTRACT and TASK QA sections into answer.md."""
    existing_extract = None
    existing_qa = None

    if answer_path.exists():
        content = read_text(answer_path)
        if "### TASK QA" in content:
            extract_part, qa_part = content.split("### TASK QA", 1)
            existing_extract = extract_part.strip()
            existing_qa = ("### TASK QA" + qa_part).strip()
        else:
            existing_extract = content.strip()

    final_sections = []
    chosen_extract = extract_section or existing_extract
    chosen_qa = qa_section or existing_qa

    if chosen_extract:
        final_sections.append(chosen_extract.strip())
    if chosen_qa:
        final_sections.append(chosen_qa.strip())

    if final_sections:
        write_text(answer_path, "\n\n".join(final_sections).strip() + "\n")
    else:
        answer_path.unlink(missing_ok=True)


def run_extraction(input_dir: Path, output_dir: Path) -> List[ExtractedDocument]:
    """Run the extraction pipeline across all PDFs in input_dir."""
    ensure_dir(output_dir)
    pdf_paths = load_pdf_paths(input_dir)
    if not pdf_paths:
        logging.warning("No PDF files found in %s", input_dir)
        return []

    documents: List[ExtractedDocument] = []
    for pdf_path in tqdm(pdf_paths, desc="Extracting PDFs"):
        document = extract_single_pdf(pdf_path, output_dir)
        documents.append(document)

    extract_section = render_task_extract(documents)
    answer_path = output_dir / "answer.md"
    merge_answer_sections(answer_path, extract_section=extract_section)
    logging.info("Extraction artifacts saved to %s", output_dir)
    return documents


def build_index_from_markdown(markdown_files: Sequence[Path]) -> VectorIndex:
    """Create a retrieval index from markdown documents."""
    chunks: List[str] = []
    for md_path in markdown_files:
        content = read_text(md_path)
        pieces = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
        chunks.extend(pieces)
    if not chunks:
        raise ValueError("No textual content found for indexing.")
    return build_index(chunks)


def run_qa(
    extracted_dir: Path,
    output_dir: Path,
    questions_path: Path,
    top_k: int,
    threshold: float,
) -> List[Dict[str, object]]:
    """Run the QA pipeline given extracted markdown and question CSV."""
    markdown_files = sorted(extracted_dir.glob("*/main.md"))
    if not markdown_files:
        raise FileNotFoundError(
            f"No extracted markdown files found under {extracted_dir}. Run stage 'extraction' first."
        )

    logging.info("Building retrieval index from %d markdown files.", len(markdown_files))
    index = build_index_from_markdown(markdown_files)

    if not questions_path or not questions_path.exists():
        raise FileNotFoundError("Questions CSV not provided or not found.")

    dataframe = pd.read_csv(questions_path)
    questions = parse_questions(dataframe.itertuples(index=False, name=None))
    logging.info("Loaded %d questions from %s", len(questions), questions_path)

    qa_results: List[Dict[str, object]] = []
    for question_text, options in tqdm(questions, desc="Answering questions"):
        retrieved = retrieve(index, question_text, top_k=top_k)
        context = [chunk for chunk, _ in retrieved]
        selected = select_answers(
            question_text,
            options,
            context=context,
            base_threshold=threshold,
        )
        qa_results.append(
            {
                "question": question_text,
                "options": options,
                "selected": selected,
            }
        )

    qa_section = render_task_qa(qa_results)
    answer_path = output_dir / "answer.md"
    merge_answer_sections(answer_path, qa_section=qa_section)
    logging.info("QA predictions saved to %s", answer_path)
    return qa_results


def run_evaluate(output_dir: Path) -> None:
    """Provide a lightweight check on the generated outputs."""
    answer_path = output_dir / "answer.md"
    if not answer_path.exists():
        logging.warning("answer.md not found in %s. Run extraction/qa first.", output_dir)
        return
    content = read_text(answer_path)
    logging.info("answer.md contains %d characters.", len(content))
    logging.debug("answer.md preview:\n%s", content[:500])


def main() -> None:
    """Kick off the pipeline orchestration."""
    args = parse_arguments()
    configure_logging(getattr(logging, args.log_level.upper(), logging.INFO))

    if args.stage == "extraction":
        run_extraction(args.input_dir, args.output_dir)
    elif args.stage == "qa":
        run_qa(args.input_dir, args.output_dir, args.questions, args.top_k, args.threshold)
    elif args.stage == "evaluate":
        run_evaluate(args.output_dir)
    else:
        raise ValueError(f"Unsupported stage: {args.stage}")


if __name__ == "__main__":
    main()
