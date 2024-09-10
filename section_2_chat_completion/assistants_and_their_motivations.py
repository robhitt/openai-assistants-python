# We're going to make a simple assistant that helps us solve math problems.
# Rather than let the LLM solve the math problem, we'll convert the word problem into Python code.

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# We can see that in Math the LLM may be hallucinating
# In these cases we may want to build/use an assistant.
# answer = 123456 * 456789
# print(answer)

response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    temperature=0,  # 0 is good for deterministic responses

    # The below does not work well w/o an assistant
    # messages=[
    #     {'role': 'system', 'content': 'You help solve math problems.'},
    #     {'role': 'user', 'content': 'What is 123456 times 456789?'}
    # ]

    # We convert the word problem into Python code
    messages=[
        {'role': 'system', 'content': 'You convert word problems into Python code. Only return the python code equivalent, no other commentary.'},
        {'role': 'user', 'content': 'What is 4 times 5?'},
    ]
)

print(eval(response.choices[0].message.content))




