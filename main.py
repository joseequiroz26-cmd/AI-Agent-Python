import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from functions.prompts import system_prompt
from functions.call_function import available_functions, call_function
import json


def main() -> None:
    parser = argparse.ArgumentParser(description="AI code Assistant")
    parser.add_argument("user_prompt", type=str, help="This is the user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError ("The API is None, please verify")

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
    ]
    if args.verbose:
            print(f"User prompt: {args.user_prompt}\n")
    generate_content(client, messages, args.verbose)
    

    
def generate_content(client:OpenAI, messages:list, verbose:bool):
    for interaction in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages = messages,
            temperature = 0,
            tools = available_functions,
        )
        
        if response.usage is None:
            raise RuntimeError ("There were not response this time")

        if verbose:
            print("Prompt tokens: ",response.usage.prompt_tokens)
            print("Response tokens: ",response.usage.completion_tokens)


        message = response.choices[0].message
        messages.append(message)

        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose)

                if not result_message["content"]:
                    raise RuntimeError("Function returned empty content")
                
                if verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)

        else:
            print(message.content)
            return

    print("The maximum number of iterations has been reached")

    raise SystemExit(1)




            
if __name__== "__main__":
    main()


