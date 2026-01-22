from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
import threading

# =========================
# INTERNAL PIPELINES
# =========================
from core.run_book_engine import run_engine
from core.build_book_index import ingest_pdf
from core.index.indexer import build_and_persist_index
from core.utils.path import book_index_dir
from core.build_book_index import index_book

app = Flask(__name__)
CORS(app)

# =========================
# PROJECT ROOT & PATHS
# =========================
PROJECT_ROOT = Path(__file__).resolve().parent.parent

UPLOAD_FOLDER = PROJECT_ROOT / "uploads"
DATA_FOLDER = PROJECT_ROOT / "data"

UPLOAD_FOLDER.mkdir(exist_ok=True)
DATA_FOLDER.mkdir(exist_ok=True)

# =========================
# UPLOAD BOOK
# =========================
@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        return jsonify({"message": "No PDF file provided"}), 400

    pdf = request.files["pdf"]
    book_name = request.form.get("book_name")

    if not book_name:
        return jsonify({"message": "Book name is required"}), 400

    if pdf.filename == "":
        return jsonify({"message": "No file selected"}), 400

    safe_id = secure_filename(book_name)

    save_path = UPLOAD_FOLDER / f"{safe_id}.pdf"
    pdf.save(str(save_path))

    threading.Thread(
        target=index_book,
        args=(safe_id, str(save_path)),
        daemon=True
    ).start()

    return jsonify({
        "status": "success",
        "message": (
            f"'{book_name}' uploaded successfully. "
            "Indexing started and may take a few minutes."
        )
    })

# =========================
# LIST AVAILABLE BOOKS
# =========================
@app.route("/books", methods=["GET"])
def list_books():
    books = [file.stem for file in UPLOAD_FOLDER.glob("*.pdf")]
    return jsonify({"books": books})

# =========================
# RUN CHAT
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    book_id = data.get("book_id")
    question = data.get("question")

    if not book_id or not question:
        return jsonify({"message": "book_id and question are required"}), 400

    try:
        # 🔑 Resolve index PATH here (not ID)
        index_path = book_index_dir(book_id)

        answer = run_engine(
            engine_id="chat",
            index_path=str(index_path),
            question=question
        )

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
# =========================
# Lesson Plan builder
# =========================
@app.route("/lesson-plan", methods=["POST"])
def lesson_plan():
    data = request.json

    book_id = data.get("book_id")
    chapter = data.get("chapter")
    topic = data.get("topic")

    index_path = book_index_dir(book_id)

    lesson_plan = run_engine(
        engine_id="lesson_plan",
        index_path=str(index_path),
        params={
            "chapter": chapter,
            "topic": topic
        }
    )

    return jsonify({"lesson_plan": lesson_plan})

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)
