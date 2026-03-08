import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found")
    exit()

client = genai.Client(api_key=api_key)

with open("available_models.txt", "w", encoding="utf-8") as f:

    f.write("Available Gemini Models\n\n")

    try:
        models = client.models.list()

        for model in models:
            f.write(model.name + "\n")

        print("✅ Model list saved to available_models.txt")

    except Exception as e:
        f.write("Error listing models: " + str(e))
        print("❌ Error:", e)