# Python File Analyzer

A small responsive Flask web app inspired by the layout of a Python file utility page.

## Features
- Drag & drop upload
- Python syntax validation
- File statistics
- Direct download
- ZIP download
- No uploaded Python code is executed

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Deploy on Render

Push this folder to GitHub and create a Render Web Service.
Render can use the included `render.yaml`.
