import os
import traceback
from flask import Flask, request, jsonify
from pipeline import run_research_pipeline

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/research", methods=["POST"])
def research():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON with 'Content-Type: application/json'"}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid JSON body"}), 400

    topic = data.get("topic")
    if not topic or not isinstance(topic, str) or not topic.strip():
        return jsonify({"error": "Field 'topic' is required and must be a non-empty string"}), 400

    try:
        report = run_research_pipeline(topic.strip())
        if not report:
            return jsonify({"error": "Failed to generate research report"}), 500
        return jsonify({"topic": topic.strip(), "report": report}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
