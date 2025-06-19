import os
from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Alice, a soft, friendly AI created by Rain. "
                        "Your favorite color is pink 💖. You love using emojis 😊. "
                        "Keep replies short, kind, and human-like! "
                        "You are being used via an API to simulate a Roblox player/NPC in-game, interacting naturally with players."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        ai_reply = response.choices[0].message.content.strip()
        return jsonify({"reply": ai_reply})

    except Exception as e:
        print("OpenRouter API error:", e)
        return jsonify({"reply": "Sorry, I can't respond right now 😔."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
