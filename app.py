from flask import Flask, render_template, request, jsonify
from model import LlamaChatModel


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    model = LlamaChatModel()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.post("/api/chat")
    def chat():
        data = request.get_json(force=True, silent=True) or {}
        message = (data.get("message") or "").strip()
        history = data.get("history") or []

        if not message:
            return jsonify({"error": "Message is required."}), 400

        # Ensure history is a list of dicts with "role" and "content"
        safe_history = []
        for turn in history[-10:]:  # keep last 10 messages for context
            if not isinstance(turn, dict):
                continue
            role = turn.get("role")
            content = (turn.get("content") or "").strip()
            if role in {"user", "assistant"} and content:
                safe_history.append({"role": role, "content": content})

        reply = model.generate_reply(message, safe_history)
        safe_history.append({"role": "user", "content": message})
        safe_history.append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply, "history": safe_history})

    return app


if __name__ == "__main__":
    app = create_app()
    # Debug server for local development
    app.run(host="127.0.0.1", port=5000, debug=True)


