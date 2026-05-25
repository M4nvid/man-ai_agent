import os
import argparse
from dotenv import load_dotenv
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError ("Environment variable not found")

from google import genai
from google.genai import types
from call_function import available_functions

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Parsing arguments for the agent")
    parser.add_argument("user_prompt", type=str, help="Adds a User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
)
    
    if response.usage_metadata is None:
        raise RuntimeError ("Failed API request?")
    
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
       
    if not response.function_calls:
        print("Response:")
        print(response.text)
    else:
        for function_call in response.function_calls: 
            print (f"Calling function: {function_call.name}({function_call.args})")


if __name__ == "__main__":
    main()
