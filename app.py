import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ----------------------------------------
# LOAD ENV
# ----------------------------------------

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    raise ValueError("HF_API_KEY not found in .env file")

# ----------------------------------------
# HUGGINGFACE CLIENT
# ----------------------------------------

hf_client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct",
    token=HF_API_KEY
)

# ----------------------------------------
# FLASK APP
# ----------------------------------------

app = Flask(__name__)
CORS(app)

# ----------------------------------------
# ROOT ROUTE
# ----------------------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Legal AI Backend Running"
    })

# ----------------------------------------
# LOAD DATASETS
# ----------------------------------------

DATASET_FOLDER = "datasets"
laws = []

for file in os.listdir(DATASET_FOLDER):
    if file.endswith(".json"):

        path = os.path.join(DATASET_FOLDER, file)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            laws.extend(data)

print("Total laws loaded:", len(laws))

# ----------------------------------------
# DOMAIN → LAW MAP
# ----------------------------------------

intent_map = {

"theft":["378","379"],
"property_damage":["427"],
"assault":["323"],
"noise_nuisance":["268"],
"drunk_driving":["185","279"],
"cybercrime":["66"],
"corruption":["prevention of corruption"]

}

# ----------------------------------------
# LLM CLASSIFIER
# ----------------------------------------

def classify_domain(text):

    prompt = f"""
You are a legal classification system.

Classify the following scenario into ONE of these domains:

theft
property_damage
assault
noise_nuisance
drunk_driving
cybercrime
corruption

Return ONLY the domain name.

Scenario:
{text}
"""

    response = hf_client.text_generation(
        prompt,
        max_new_tokens=10
    )

    domain = response.strip().lower()

    return domain

# ----------------------------------------
# LAW RETRIEVAL
# ----------------------------------------

def retrieve_laws(intent):

    matches = []
    sections = intent_map.get(intent, [])

    for law in laws:

        section = law.get("section","").lower()
        act = law.get("act","").lower()

        for s in sections:

            if s in section or s in act:

                matches.append({
                    "legal_info": law,
                    "score": 1.0
                })

    return matches[:2]

# ----------------------------------------
# LLM EXPLANATION GENERATOR
# ----------------------------------------

def generate_explanation(scenario, law):

    prompt = f"""
A user described the following legal scenario:

{scenario}

Relevant law:

Act: {law['act']}
Section: {law['section']}
Description: {law['description']}
Punishment: {law['punishment']}

Explain this law in simple sentences and tell the user what legal action they can take.
"""

    response = hf_client.text_generation(
        prompt,
        max_new_tokens=200
    )

    return response.strip()

# ----------------------------------------
# MAIN API
# ----------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json
    scenario = data.get("scenario","")

    if not scenario:
        return jsonify({"error":"No scenario provided"}),400

    # Step 1: LLM classification
    intent = classify_domain(scenario)

    # Step 2: Retrieve law
    results = retrieve_laws(intent)

    if not results:
        return jsonify({
            "conversational_response":"I couldn't find exact laws for this scenario.",
            "results":[]
        })

    law = results[0]["legal_info"]

    # Step 3: LLM explanation
    explanation = generate_explanation(scenario, law)

    return jsonify({
        "domain": intent,
        "conversational_response": explanation,
        "results": results
    })

# ----------------------------------------
# HEALTH CHECK
# ----------------------------------------

@app.route("/health")
def health():

    return jsonify({
        "status":"running",
        "laws_loaded": len(laws)
    })

# ----------------------------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
