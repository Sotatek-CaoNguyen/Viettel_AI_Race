Initial file for Viettel_AI_Race
run
# extraction (tạo markdown từ PDF)
python -m main --stage extraction --input_dir data/input --output_dir data/output

# QA (cần CSV câu hỏi)
python -m main --stage qa --input_dir data/output --output_dir data/output --questions data/questions/questions.csv

# evaluate (kiểm tra answer.md)
python -m main --stage evaluate --output_dir data/output

```project/
├── main.py                      # Entry point cho toàn bộ pipeline
├── requirements.txt             # Dependencies
├── config/
│   ├── extract_config.yaml     # Config cho extraction
│   └── qa_config.yaml          # Config cho QA
│
├── models/
│   ├── checkpoints/            # Model weights
│   ├── extraction/
│   │   ├── table_detector.py  # Table detection model (<4B params)
│   │   ├── text_recognizer.py # OCR/Text recognition
│   │   └── layout_parser.py   # Layout analysis
│   └── qa/
│       ├── retriever.py        # Document retriever
│       └── answerer.py         # Answer selection model (<4B params)
│
├── preprocessing/
│   ├── pdf_loader.py           # Load và parse PDF
│   ├── watermark_remover.py   # Xử lý watermark
│   ├── page_segmenter.py      # Phân đoạn trang
│   └── image_processor.py     # Xử lý hình ảnh
│
├── extraction/
│   ├── table_extractor.py     # Trích xuất bảng
│   ├── formula_extractor.py   # Trích xuất công thức
│   ├── text_extractor.py      # Trích xuất văn bản
│   └── merge_cell_handler.py  # Xử lý merged cells
│
├── postprocessing/
│   ├── markdown_converter.py  # Convert sang Markdown
│   ├── latex_formatter.py     # Format công thức LaTeX
│   ├── html_table_builder.py  # Build HTML tables
│   └── validator.py           # Validate output
│
├── qa/
│   ├── indexer.py             # Build search index (local)
│   ├── retriever.py           # Retrieve relevant context
│   ├── question_parser.py     # Parse questions from CSV
│   └── answer_selector.py     # Select answers
│
├── utils/
│   ├── file_handler.py        # I/O operations
│   ├── logger.py              # Logging
│   └── metrics.py             # Evaluation metrics
│
├── scripts/
│   ├── run_extract.sh         # Script chạy extraction
│   ├── run_choose_answer.sh   # Script chạy QA
│   └── evaluate.sh            # Script đánh giá
│
└── data/
    ├── augmented/             # Augmented training data
    └── cache/                 # Cache cho tốc độ`;
```
