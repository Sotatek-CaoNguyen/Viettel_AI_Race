Initial file for Viettel_AI_Race
run
# extraction (tạo markdown từ PDF)
python -m project.main --stage extraction --input_dir data/input --output_dir data/output

# QA (cần CSV câu hỏi)
python -m project.main --stage qa --input_dir data/output --output_dir data/output --questions data/questions/questions.csv

# evaluate (kiểm tra answer.md)
python -m project.main --stage evaluate --output_dir data/output
