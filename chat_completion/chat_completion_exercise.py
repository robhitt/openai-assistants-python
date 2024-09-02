# Using a while loop create a chatbot that answers questions about astronomy & the universe
# w simplified explanations that a 5 year odl could understand.
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

print('Welcome to your own tutor about the universe!')
print("To exit, type 'BYE'")

question = ''

messages = [{
    'role': 'system',
    'content': 'You are a chatbot that answers questions about astronomy and the universe. You will give responses with simplified explanations that a 5 year old could understand.'
}]

while question != "BYE":
    question = input("Ask me a question about astronomy and the universe: ")

    messages.append({'role': 'user', 'content': question})

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        temperature=0.5,
        messages=[
            {
                'role': 'user',
                'content': question
            }
        ]
    )

    reply = response.choices[0].message.content
    print('\n')
    print(reply)
    print('\n')

    messages.append({'role': 'assistant', 'content': reply})
