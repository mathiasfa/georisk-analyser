from flask import Flask, request, jsonify, send_from_directory
import os
from main import analyser_bien

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/analyser", methods=["POST"])
def analyser():
    data = request.get_json()
    adresse = data.get("adresse")
    
    if not adresse:
        return jsonify({"error": "Adresse manquante"}), 400
    
    rapport = analyser_bien(adresse)
    
    if not rapport:
        return jsonify({"error": "Impossible d'analyser cette adresse"}), 500
    
    return jsonify({"rapport": rapport})

if __name__ == "__main__":
    app.run(debug=True)