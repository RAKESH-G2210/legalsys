import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

app = Flask(**name**)
CORS(app)

# --------------------------------------------------

# ROOT ROUTE (RENDER HEALTH CHECK)

# --------------------------------------------------

@app.route("/")
def home():
return jsonify({
"message": "Legal AI Backend Running"
})

# --------------------------------------------------

# LOAD DATASETS

# --------------------------------------------------

DATASET_FOLDER = "datasets"
laws = []

for file in os.listdir(DATASET_FOLDER):
if file.endswith(".json"):
path = os.path.join(DATASET_FOLDER, file)

```
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        laws.extend(data)
```

print("Total laws loaded:", len(laws))

# --------------------------------------------------

# NLP INTENT TRAINING DATA

# --------------------------------------------------

intent_examples = {

"theft":[
"someone stole my phone",
"my laptop was stolen",
"someone took my wallet",
"bike theft",
"phone stolen",
"someone stole my laptop"
],

"property_damage":[
"someone broke my car window",
"stone hit my car",
"someone threw a stone at my car",
"damaged my property",
"someone vandalized my car"
],

"assault":[
"someone hit me",
"someone attacked me",
"person punched me",
"someone injured me",
"someone beat me"
],

"noise_nuisance":[
"neighbour playing loud music",
"noise disturbance at night",
"loud party next door",
"neighbour making noise"
],

"drunk_driving":[
"drunk driver hit my car",
"driver under alcohol",
"drunk driving accident",
"alcohol driving crash"
],

"cybercrime":[
"my account got hacked",
"someone hacked my instagram",
"password stolen",
"cyber attack"
],

"corruption":[
"police asking money instead of challan",
"officer asking bribe",
"illegal payment to police"
]

}

# --------------------------------------------------

# NLP MODEL

# --------------------------------------------------

vectorizer = TfidfVectorizer()

all_examples = []
intent_labels = []

for intent, examples in intent_examples.items():
for example in examples:
all_examples.append(example)
intent_labels.append(intent)

X = vectorizer.fit_transform(all_examples)

def detect_intent(text):
query = vectorizer.transform([text])
similarity = cosine_similarity(query, X)
idx = similarity.argmax()
return intent_labels[idx]

# --------------------------------------------------

# INTENT → LAW MAP

# --------------------------------------------------

intent_map = {

"theft":["378","379"],
"property_damage":["427"],
"assault":["323"],
"noise_nuisance":["268"],
"drunk_driving":["185","279"],
"cybercrime":["66"],
"corruption":["prevention of corruption"]

}

# --------------------------------------------------

# LAW RETRIEVAL

# --------------------------------------------------

def retrieve_laws(intent):

```
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
```

# --------------------------------------------------

# MAIN API

# --------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

```
data = request.json
scenario = data.get("scenario","")

if not scenario:
    return jsonify({"error":"No scenario provided"}),400

intent = detect_intent(scenario)
results = retrieve_laws(intent)

if not results:
    return jsonify({
        "conversational_response":"I couldn't find exact laws for this scenario.",
        "results":[]
    })

law = results[0]["legal_info"]

explanation = f"""
```

### Legal Analysis

Based on your scenario, this appears to relate to **{intent.replace("_"," ")}**.

Relevant Law:

{law['act']} {law['section']}

{law['description']}

Possible Punishment: {law['punishment']}

You may consider contacting local authorities or filing a complaint depending on the severity of the situation.
"""

```
return jsonify({
    "conversational_response": explanation,
    "results": results
})
```

# --------------------------------------------------

# HEALTH CHECK

# --------------------------------------------------

@app.route("/health")
def health():

```
return jsonify({
    "status":"running",
    "laws_loaded": len(laws)
})
```

# --------------------------------------------------

if **name** == "**main**":

```
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
```
