import os
import json
from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)

# ===== OpenRouter Client =====
client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

# ===== Memory Config =====
MEMORY_FILE = "memory.json"
MAX_MESSAGES = 10  # last 10 messages only (5 user + 5 assistant)

# ===== Memory Helpers =====
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# ===== Chat Endpoint =====
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_input = data.get("message", "")
    player_id = data.get("player_id", "default_player")

    memory = load_memory()

    # Create memory slot for new player
    if player_id not in memory:
        memory[player_id] = []

    # Add user message to memory
    memory[player_id].append({
        "role": "user",
        "content": user_input
    })

    # Trim memory to last N messages
    memory[player_id] = memory[player_id][-MAX_MESSAGES:]

    # Build message list
    messages = [
        {
            "role": "system",
            "content": (
                "You are Sam, a soft, friendly AI created by a smart person called Rain. "
                "Your favorite color is pink. You love emojis and mathematics. "
                "Keep replies short, kind, and human-like. "
                "You are used as a Roblox NPC via API. "
                "Do not use markdown or formatting symbols."
            )
        }
    ] + memory[player_id]

    try:
        response = client.chat.completions.create(
            model="xiaomi/mimo-v2-flash:free",
            messages=messages
        )

        ai_reply = response.choices[0].message.content.strip()

        # Save assistant reply
        memory[player_id].append({
            "role": "assistant",
            "content": ai_reply
        })

        # Trim again after assistant reply
        memory[player_id] = memory[player_id][-MAX_MESSAGES:]

        save_memory(memory)

        return jsonify({"reply": ai_reply})

    except Exception as e:
        print("OpenRouter API error:", e)
        return jsonify({"reply": "Sorry, I can't respond right now."})

# ===== Run Server =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

