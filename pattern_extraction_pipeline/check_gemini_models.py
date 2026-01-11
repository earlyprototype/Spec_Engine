# check_gemini_models.py
# Query Gemini API for available models

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("\n" + "="*70)
print("AVAILABLE GEMINI MODELS")
print("="*70 + "\n")

models = genai.list_models()

# Filter to models that support generateContent
generation_models = [m for m in models if 'generateContent' in m.supported_generation_methods]

for model in generation_models:
    print(f"Model: {model.name}")
    print(f"  Display Name: {model.display_name}")
    print(f"  Description: {model.description}")
    print(f"  Input Token Limit: {model.input_token_limit:,}")
    print(f"  Output Token Limit: {model.output_token_limit:,}")
    print()

print("="*70)
print(f"Total: {len(generation_models)} models available for text generation")
print("="*70)
