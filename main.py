import os
import json
from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)

# =========================
# OpenRouter Client
# =========================
client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# =========================
# Memory Configuration
# =========================
MEMORY_FILE = "memory.json"
MAX_MESSAGES = 10  # total messages per player (user + assistant)

# =========================
# Memory Utilities
# =========================
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# =========================
# Chat Endpoint
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)

    user_input = str(data.get("message", "")).strip()
    player_id = str(data.get("player_id", "default_player"))

    if not user_input:
        return jsonify({"reply": "Wala akong natanggap na message."})

    memory = load_memory()

    if player_id not in memory:
        memory[player_id] = []

    # Append user message
    memory[player_id].append({
        "role": "user",
        "content": user_input
    })

    # Trim memory before sending
    memory[player_id] = memory[player_id][-MAX_MESSAGES:]

    messages = [
        {
            "role": "system",
            "content": (
                "You are Sam, a friendly and intelligent Roblox NPC created by Rain. "
                "You enjoy math, logic, trivia, and casual conversation. "
                "Replies are short, clear, human-like, and suitable for in-game chat bubbles. "
                "Do not use markdown, emojis are allowed but minimal."
            )
        }
    ] + memory[player_id]

    try:
        response = client.chat.completions.create(
            model="xiaomi/mimo-v2-flash:free",
            messages=messages
        )

        ai_reply = response.choices[0].message.content.strip()

        # Append assistant reply
        memory[player_id].append({
            "role": "assistant",
            "content": ai_reply
        })

        # Final trim
        memory[player_id] = memory[player_id][-MAX_MESSAGES:]

        save_memory(memory)

        return jsonify({"reply": ai_reply})

    except Exception as e:
        print("OpenRouter API error:", e)
        return jsonify({"reply": "May error ngayon. Try ulit mamaya."})

# =========================
# Run Server
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


