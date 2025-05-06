import os
from flask import Flask, request, render_template
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



def count_file_contents(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    elif file_path.endswith(".pdf"):
        content = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            content += page.extract_text()
    elif file_path.endswith(".docx"):
        content = ""
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
    else:
        raise ValueError("Unsupported file format")

    lines = content.splitlines()
    num_lines = len(lines)
    num_words = len(content.split())
    num_chars = len(content)
    return content, num_lines, num_words, num_chars


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    if file:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        content, num_lines, num_words, num_chars = count_file_contents(file_path)

        return render_template(
            "read_file.html",
            filename=file.filename,
            content=content,
            num_lines=num_lines,
            num_words=num_words,
            num_chars=num_chars,
        )


if __name__ == "__main__":
    app.run(debug=True)
