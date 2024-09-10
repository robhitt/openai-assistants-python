from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()

client = OpenAI()

# Step 1 - Create Assistant
assistant = client.beta.assistants.create(
    name="Mortgage Bot",
    instructions="You use Python code to help answer questions about mortgage and interest payments.",
    tools=[{'type': 'code_interpreter'}],
    model="gpt-3.5-turbo"
)

# Step 2 - Create Thread
thread = client.beta.threads.create()

# Step 3: Create Message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='I want to buy a house that costs $2.1 Million on a 30 year fixed loan at 7.8% interest. What will my monthly payments be?'
)

# Step 4: Run The Thread with the assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Give a detailed analysis and considerations regarding the mortgage payments."
)

# while run.status != 'completed':
#     print(run.status)
#     run = client.beta.threads.runs.retrieve(
#         thread_id=thread.id,
#         run_id=run.id
#     )
#     time.sleep(5)


def wait_on_run(run, thread):
    while run.status == 'queued' or run.status == 'in_progress':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        time.sleep(0.5)
        print(run.status)
    return run


wait_on_run(run, thread)


# Step 5 - Display the response
def display_thread_messages(thread_messages):
    for thread_message in thread_messages:
        print(thread_message.content[0].text.value)
        print("\n")


messages = client.beta.threads.messages.list(
    thread_id=thread.id,
    order='asc',
    after=message.id
)
display_thread_messages(messages)

# List messages in thread,
# We want to do this so we can add add new messages

print("=========================")
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='What if I put a down payment of 200k on the house, how would that change my monthly payments?'
)

# print(client.beta.threads.messages.list(thread_id=thread.id))


# Execute new run with the new thread message
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

wait_on_run(run, thread)

messages = client.beta.threads.messages.list(thread_id=thread.id, order='asc', after=message.id)

display_thread_messages(messages)

# Delete Assistant
response = client.beta.assistants.delete(assistant.id)
