
import google.generativeai as genai
import json
import jsonschema
import argparse
import re
import os

# Configure the API key
# Replace with your actual API key
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def load_file(file_path: str) -> str:
    """Loads text content from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_json(file_path: str) -> dict:
    """Loads a JSON object from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_structured_output(text_content: str, json_schema: dict) -> str:
    """
    Generates structured JSON from unstructured text using a prompt-based approach.
    This method allows for full schema adherence, including fields like '$schema'.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "You are a helpful assistant that converts unstructured text into a valid JSON object. "
            "You will be given unstructured text and a JSON schema. "
            "Your task is to extract all relevant information from the text and format it *strictly* according to the provided JSON schema. "
            "Use the schema as a template and populate the fields with data from the text. "
            "If a field in the schema is not found in the text, include a plausible default of the correct type (e.g., 1.0 for strings, 0 for numbers, empty arrays or objects), but avoid using null unless explicitly allowed in the schema."
            "Do not add any fields not present in the schema. Do not generate a different schema. "
            "Return only the raw JSON object, without any additional text or formatting. The output must be valid JSON."
        )
    )

    prompt = (
        f"Unstructured Text:\n---\n{text_content}\n---\n\n"
        f"JSON Schema:\n---\n{json_schema}\n---\n\n"
        "Extracted JSON object:"
    )

    response = model.generate_content(prompt)
    return response.text

def validate_json(json_data: dict, schema: dict) -> tuple[bool, str]:
    """
    Validates a JSON object against a schema.
    Returns a tuple of (is_valid, error_message)
    """
    try:
        jsonschema.validate(instance=json_data, schema=schema)
        return True, ""
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description="Convert unstructured text to structured JSON using a schema via Google's Gemini API.")
    parser.add_argument("--input", required=False, help="Path to input text file")
    parser.add_argument("--schema", required=True, help="Path to schema JSON file")
    parser.add_argument("--output", required=True, help="Path to save generated output JSON")
    args = parser.parse_args()

    if not args.input:
        print("[!] No input provided. Exiting.")
        return
    
    # Load input and schema
    input_text = load_file(args.input)
    schema = load_json(args.schema)

    # Generate output
    print("\n[+] Calling Gemini LLM to generate structured output...")
    output_raw = generate_structured_output(input_text, schema)

    try:
        # output_json = json.loads(output_raw)
        # Extract JSON block from model output
        match = re.search(r"\{.*\}", output_raw, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in model output.")

        output_json = json.loads(match.group(0))
        
    except json.JSONDecodeError as e:
        print("[!] Error parsing model output as JSON:", str(e))
        print("\nRaw Output:\n", output_raw)
        return

    # Validate
    print("[+] Validating against schema...")
    valid, error = validate_json(output_json, schema)
    if valid:
        print("[✓] Output is valid.")
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_json, f, indent=2)
        print(f"[+] Output saved to {args.output}")
    else:
        print("[!] Output is invalid:", error)
        print("\nGenerated Output:\n", json.dumps(output_json, indent=2))

if __name__ == "__main__":
    main()



# schema_guided_extractor.py (Groq version)

# import json
# import argparse
# import requests
# from jsonschema import validate, ValidationError

# # ------------------------ CONFIG ------------------------
# GROQ_API_KEY = ""  # Replace with your Groq API key
# GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# MODEL = "llama-3.1-8b-instant"  # Groq supported model

# # ------------------------ UTILITIES ------------------------
# def load_file(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return f.read()

# def load_json(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)

# def validate_json(data, schema):
#     try:
#         validate(instance=data, schema=schema)
#         return True, None
#     except ValidationError as e:
#         return False, str(e)

# # ------------------------ LLM PROMPT ------------------------
# def generate_structured_output(input_text, schema):
#     prompt = f"""
#     You are an intelligent AI agent. Your job is to convert unstructured text into a structured JSON format.
#     The output JSON must strictly adhere to this schema:

#     {json.dumps(schema, indent=2)}

#     Here is the unstructured input:
#     """
#     {input_text}
#     """

#     Return only the JSON output.
#     """

#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": MODEL,
#         "messages": [
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0
#     }

#     response = requests.post(GROQ_API_URL, headers=headers, json=payload)

#     if response.status_code != 200:
#         raise Exception(f"Groq API Error {response.status_code}: {response.text}")

#     return response.json()["choices"][0]["message"]["content"]

# # ------------------------ MAIN FUNCTION ------------------------
# def main():
#     parser = argparse.ArgumentParser(description="Convert unstructured text to structured JSON using a schema via Groq.")
#     parser.add_argument("--input", required=False, help="Path to input text file")
#     parser.add_argument("--schema", required=True, help="Path to schema JSON file")
#     parser.add_argument("--output", required=True, help="Path to save generated output JSON")
#     args = parser.parse_args()

#     # Load input and schema
#     # input_text = load_file(args.input)
#     input_text = ''
#     schema = load_json(args.schema)

#     # Generate output
#     print("\n[+] Calling Groq LLM to generate structured output...")
#     output_raw = generate_structured_output(input_text, schema)

#     try:
#         output_json = json.loads(output_raw)
#     except json.JSONDecodeError as e:
#         print("[!] Error parsing model output as JSON:", str(e))
#         print("\nRaw Output:\n", output_raw)
#         return

#     # Validate
#     print("[+] Validating against schema...")
#     valid, error = validate_json(output_json, schema)
#     if valid:
#         print("[✓] Output is valid.")
#         with open(args.output, "w", encoding="utf-8") as f:
#             json.dump(output_json, f, indent=2)
#         print(f"[+] Output saved to {args.output}")
#     else:
#         print("[!] Output is invalid:", error)
#         print("\nGenerated Output:\n", json.dumps(output_json, indent=2))

# if __name__ == "__main__":
#     main()
