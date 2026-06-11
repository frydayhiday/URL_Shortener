from flask import Flask, request, jsonify
import json
import os
import uuid

app = Flask(__name__)

DATA_FILE = "links.json"


def load_links():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_links(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/links", methods=["POST"])
def create_link():
    body = request.get_json()

    if not body or "url" not in body:
        return jsonify({"error": "url is required"}), 400

    link_id = str(uuid.uuid4())[:8]

    links = load_links()
    links[link_id] = body["url"]
    save_links(links)

    return jsonify({
        "id": link_id,
        "short_url": f"/{link_id}"
    }), 201


@app.route("/<link_id>", methods=["GET"])
def get_link(link_id):
    links = load_links()

    if link_id not in links:
        return jsonify({"error": "Link not found"}), 404

    return jsonify({
        "id": link_id,
        "url": links[link_id]
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
