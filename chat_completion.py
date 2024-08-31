import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Temperature
# Default 1,
# Temperatures of zero is good for things like programming tasks, where you want the model to be more deterministic
# Higher temperatures will give you more creative responses like story telling
# response = client.chat.completions.create(
#     model='gpt-3.5-turbo',
#     temperature=1,
#     messages=[
#         # Testing Temperature
#         # {'role': 'system', 'content': 'You are a storyteller about the future.'},
#         # {'role': 'user', 'content': 'Tell me a story.'},
#
#         # Assistant training below
#         # {'role': 'system', 'content': 'You are a customer support agent for the Ad tech company NVDA.'},
#         # {'role': 'user', 'content': 'What is the capital of France?'},
#         # {'role': 'assistant', 'content': 'Paris. Thank you for choosing NVDA.'},
#         # {'role': 'user', 'content': 'What is the capital of Spain?'},
#         # {'role': 'assistant', 'content': 'Madrid. Thank you for choosing NVDA.'},
#         # {'role': 'user', 'content': 'What is the capital of Portugal?'},
#     ])
#
# print(response.choices[0].message.content)


# KEEP THE CONVERSATION GOING
print("BEST BUY SUPPORT AGENT CONNECTED! TYPE 'BYE' TO END CONVERSATION")

question = ''

messages = [{'role': 'system', 'content': 'You are a customer support agent for the Best Buy and give computer advice.'}]

while question != "BYE":
    question = input("")
    messages.append({'role': 'user', 'content': question})
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        temperature=0.5,
        messages=messages)

    reply = response.choices[0].message.content
    print('\n')
    print(reply)
    print('\n')

    messages.append({'role': 'assistant', 'content': reply})

