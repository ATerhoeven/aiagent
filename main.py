import os
import argparse
import sys
from tabnanny import verbose
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolMessageParam, ChatCompletionMessage
from call_function import available_functions, call_function
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
    messages: list[ChatCompletionMessageParam | ChatCompletionMessage | dict] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # model-calling logic-loop

    for _ in range(20):
        # call the model, handle responses, etc.


        # get a response from the model with a hard-coded prompt from the command line
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages, # type: ignore
            tools=available_functions,
            )

        # printing metadata if the verbose flag is set after checking if usage is not None
        if response.usage == None:
            raise RuntimeError("no Tokens used, check api key")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")

        # grab the response in a message variable
        message: ChatCompletionMessage = response.choices[0].message
        # append the model's message to the messages list
        messages.append(message)
        
        if message.tool_calls != None:
            for tool_call in message.tool_calls:
                # narrow down the type tool_call can have
                if tool_call.type != "function":
                    continue

                result_message = call_function(tool_call)
                if len(result_message["content"]) == 0:
                    raise Exception("Error: returned content was empty")

                # append the tool call to the messages list
                messages.append(result_message)

                if args.verbose:
                    print(f"-> {result_message['content']}")
          
        else:
            print(message.content)
            return
    sys.exit("Error: After 20 iterations, the model was not able to produce a resolution")


        
if __name__ == "__main__":
    main()
