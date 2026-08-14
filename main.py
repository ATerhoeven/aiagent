import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


# load the api key and raise an Error if it does not exist
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("api key not found")

# use the argparse module to convert a command-line input into a prompt
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

# create a client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
 )

# create a list of messages for storing the conversation
messages: list[ChatCompletionMessageParam] = [
    {"role": "user", "content": args.user_prompt},
]

# get a response from the model with a hard-coded prompt from the command line
response = client.chat.completions.create(model="openrouter/free", messages=messages, )

# printing the hard-coded user prompt
print(f"User prompt: {args.user_prompt}")

# printing the number of tokens used after checking if it is not None
if response.usage == None:
    raise RuntimeError("no Tokens used, check api key")

print(f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")

# printing the models response on the terminal
print(response.choices[0].message.content)

def main():
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()
