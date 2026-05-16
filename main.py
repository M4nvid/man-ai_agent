import os
import argparse
from dotenv import load_dotenv


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError ("Environment variable not found")

from google import genai

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Parsing arguments for the agent")
    parser.add_argument("user_prompt", type=str, help="Adds a User prompt")
    args = parser.parse_args()
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=args.user_prompt
)
    
    if response.usage_metadata is None:
        raise RuntimeError ("Failed API request?")
    
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
