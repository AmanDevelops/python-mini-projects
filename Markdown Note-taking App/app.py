import re
import uuid

import markdown
from flask import Flask, request
from spellchecker import SpellChecker

app = Flask(__name__)


import os

os.makedirs('uploads', exist_ok=True)

@app.route("/api/upload", methods=["POST"])
def handle_upload():
    spell = SpellChecker()
    file = request.files["file"]
    file_name = str(uuid.uuid4())
    if file:


        save_path = os.path.join("uploads", file_name + ".html")
        file.save(save_path)

        with open(save_path, "r") as f:
            data = f.read()
            words = re.findall(r"(?<!\()\b\w+\b(?![^()]*\))", data)
        misspelled = spell.unknown(words)

        for word in misspelled:
            correction = spell.correction(word)
            if word in ('https'):
                continue


            if correction is not None:
                data = re.sub(rf"\b{re.escape(word)}\b", correction, data)

        html = markdown.markdown(data)

        with open(save_path, "w") as f:
            f.write(html)

        return {"url": "http://localhost:5000/" + file_name + ".html"}
    return {"success": False}, 400


@app.route("/<file_id>")
def handle_file(file_id):
    file_path = os.path.join("uploads", file_id)
    try:
        with open(file_path, "r") as f:
            return f.read(), 200
    except:
        return "404", 404
