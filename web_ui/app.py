# web_ui/app.py
from flask import Flask, request, render_template, jsonify


class WebInterface:
    def __init__(self, search_engine):
        self.app = Flask(__name__)
        self.search_engine = search_engine

        # Définir les routes
        @self.app.route("/", methods=["GET"])
        def home():
            return render_template("search.html")

        @self.app.route("/search", methods=["GET"])
        def search():
            query = request.args.get("q", "")
            if not query:
                return jsonify({"results": []})

            results = self.search_engine.search(query)
            return jsonify({"results": results})

    def run(self, host="0.0.0.0", port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)
