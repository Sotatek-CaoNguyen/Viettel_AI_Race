from pathlib import Path
text = Path("Track_2/extraction/structured_extractor.py").read_text(encoding="utf-8")
old = "    @staticmethod\n    def _escape_table_cell(value: object) -> str:\n        text = str(value).strip() if value is not None else \"\"\n        if not text:\n            return \"\"\n        return text.replace(\"|\", \"\\\\|\").replace(\"\n\""
if old not in text:
    raise SystemExit('old fragment not found')
