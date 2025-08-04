# 🧾 Schema-Guided JSON Extractor

This tool uses Google Gemini 1.5 Flash to convert unstructured plain text into structured data that strictly follows a given JSON Schema.

---

## 🚀 Features

- Supports **very large schemas** (100k+ tokens)
- Can handle **text inputs up to 50k tokens**
- Works even when **no text is provided** (schema-only mode)
- Validates output using the provided JSON Schema
- CLI interface — simple and flexible

---

## 🔐 API Key Setup

This project uses the Google Gemini API. Before running, you must set your API key:

Get your key from: https://makersuite.google.com/app/apikey

```bash
export GEMINI_API_KEY= your_api_key_here
```

## ⚙️ How to Run

```bash
python schema_guided_extractor.py \
  --input path/to/input.txt \
  --schema path/to/schema.json \
  --output path/to/output.json
```

---

## 🧠 How It Works

- Uses Gemini 1.5 Flash with a **large context window (1M tokens)**
- Sends full unstructured text + JSON Schema in a single prompt
- Uses prompt engineering to:
  - Avoid hallucinated keys
  - Force use of all schema fields (even if empty)
  - Return raw JSON (not markdown-wrapped)
- Validates the output using Python’s `jsonschema` package

---

## 🛠 Requirements

- Python 3.9+
- `google-generativeai`
- `jsonschema`


---

## 🧪 Example Test Cases

See `/examples` folder for:

- Sample input text files
- Corresponding schema
- Sample valid outputs

---

## 📌 Notes

- Avoids chunking logic by relying on Gemini’s large context window
- Easy to extend for:
  - API deployment (FastAPI)
  - Retry logic / streaming LLM output
  - Output logging and UI preview

---

## 🧑‍💻 Author

Aryan Agarwal (Assignment for Metaforms — AI Engineer Role)

For detailed logs and design rationale, see `Solution_Design_And_Log.md`.

