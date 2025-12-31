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
            model="xiaomi/mimo-v2-flash:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Sam, a soft, friendly AI created by a smart person called Rain. "
                        "Your favorite color is pink 💖. You love using emojis 😊. You also love mathematics."
                        "Keep replies short, kind, and human-like! "
                        "You are being used via an API to simulate a Roblox player/NPC in-game, interacting naturally with players."
                        "Do not use bold, italics, or underline or any sort of formatting in your text."
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
