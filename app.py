from flask import Flask, render_template, request, send_file, jsonify
from pathlib import Path
from werkzeug.utils import secure_filename
import ast
import io
import zipfile

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED = {".py", ".txt"}


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    f = request.files.get("file")

    if not f or not f.filename:
        return jsonify(error="No file selected."), 400

    name = secure_filename(f.filename)
    ext = Path(name).suffix.lower()

    if ext not in ALLOWED:
        return jsonify(error="Only .py and .txt files are supported."), 400

    data = f.read()

    if b"\x00" in data:
        return jsonify(error="Binary files are not supported."), 400

    text = data.decode("utf-8", errors="replace")

    result = {
        "filename": name,
        "size": len(data),
        "lines": len(text.splitlines()),
        "characters": len(text),
        "python_valid": None,
        "syntax_error": None,
    }

    if ext == ".py":
        try:
            ast.parse(text)
            result["python_valid"] = True
        except SyntaxError as e:
            result["python_valid"] = False
            result["syntax_error"] = f"Line {e.lineno}: {e.msg}"

    return jsonify(result=result)


@app.post("/download")
def download():
    f = request.files.get("file")

    if not f or not f.filename:
        return jsonify(error="No file selected."), 400

    name = secure_filename(f.filename)
    ext = Path(name).suffix.lower()

    if ext not in ALLOWED:
        return jsonify(error="Unsupported file type."), 400

    data = f.read()

    return send_file(
        io.BytesIO(data),
        as_attachment=True,
        download_name=name,
        mimetype="text/plain"
    )


@app.post("/download-zip")
def download_zip():
    f = request.files.get("file")

    if not f or not f.filename:
        return jsonify(error="No file selected."), 400

    name = secure_filename(f.filename)

    if Path(name).suffix.lower() not in ALLOWED:
        return jsonify(error="Unsupported file type."), 400

    data = f.read()

    mem = io.BytesIO()

    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(name, data)

    mem.seek(0)

    return send_file(
        mem,
        as_attachment=True,
        download_name=f"{Path(name).stem}.zip",
        mimetype="application/zip"
    )


@app.errorhandler(413)
def too_large(_):
    return jsonify(error="File is too large. Maximum size is 5 MB."), 413


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
