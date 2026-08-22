import json
import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolUnionParam
from call_function import available_functions
from config import system_prompt


def main():
    print("Hello from aiagent!")
    # load the api key and raise an Error if it does not exist
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("api key not found")

    # use the argparse module to convert a command-line input into a prompt
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # create a client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    

    # create a list of messages for storing the conversation
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # get a response from the model with a hard-coded prompt from the command line
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        )

    # printing metadata if the verbose flag is set after checking if usage is not None
    if response.usage == None:
        raise RuntimeError("no Tokens used, check api key")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")

    # grab the response in a message variable
    message = response.choices[0].message
    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            # narrow down the type tool_call can have
            if tool_call.type != "function":
                continue
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        print(message.content)

if __name__ == "__main__":
    main()
