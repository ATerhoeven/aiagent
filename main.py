import os
from dotenv import load_dotenv
from openai import OpenAI


# load the api key and raise an Error if it does not exist
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("api key not found")

# create a client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
 )

# get a response from the model with a hard-coded prompt
response = client.chat.completions.create(model="openrouter/free", messages=[
    {
        "role": "user",
        "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    }
] 
)

# printing the models response on the terminal
print(response.choices[0].message.content)

def main():
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()
