from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# Here the assistant acts as the role='system' and gives instructions to the user
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You convert math problems into Python code and then run the code to show the answer.",
    tools=[{"type": "code_interpreter"}],
    model='gpt-3.5-turbo'
)

thread = client.beta.threads.create()

print("=======================================")

print("assistant.id: ", assistant.id)
print("thread.id: ", thread.id)

print("=======================================")

# Note you always 'create' a new messages even when you're adding to an existing thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content="What is 123456 times 456789?"
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
    # instructions=''  # You can override initial asst instructions here
)

print("run.status: ", run.status)
print("run.id: ", run.id)

print("=======================================")

run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)

print(run.status)

print("=======================================")

messages = client.beta.threads.messages.list(thread_id=thread.id)
print("messages", messages)
# print("most recent message: ", messages.data[0].content[0].text.value)

for thread_message in messages.data:
    print("\n")
    print(thread_message.content[0].text.value)
    print("\n")

print("=======================================")

run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)

print("run_steps: ", run_steps)

print("=======================================")
for step in run_steps:
    print(step.step_details)
    print("\n")

print("=======================================")
my_assistants = client.beta.assistants.list(order='desc', limit='20')
print("my_assistants.data: ", my_assistants.data)

# DELETE ASSISTANT
# response = client.beta.assistants.delete(assistant.id)
# print(response)

