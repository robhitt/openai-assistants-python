# create an Assistant that can take in a long text description of a bill at a restaurant and
# who ordered what and how much items cost, and then split the bill among the party accurately.

# Ex input
# Mary ordered a burger, fries and coke. I ordered just a salad and coke.
# A burger is $10, fries are $5, a salad is $8 and cokes are $2 each.
# We want to leave an 18% tip. Please split the bill between Mary and me, how much do we each owe?

# Need to continue the conversation how much each individual owes, not splitting evenly.
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

client = OpenAI()

assistant = client.beta.assistants.create(
    name="Bill Spliter Bot",
    tools=[{'type': 'code_interpreter'}],
    model="gpt-3.5-turbo",
    instructions="You use Python code to help calculate the correct way to split a bill."
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='''Mary ordered a burger, fries and coke. I ordered just a salad and coke.
A burger is $10, fries are $5, a salad is $8, and cokes are $2 each.
We want to leave an 18% tip. Please split the bill between Mary and me, how much do we each owe?'''
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    # instructions="Give a detailed breakdown of the bill and how it will be split and what is owed."
)


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

messages = client.beta.threads.messages.list(
    thread_id=thread.id,
    order="asc",
    after=message.id
)


def display_thread_messages(messages):
    for message in messages:
        print(message.content[0].text.value)
        print("\n")


display_thread_messages(messages)


print("=================")


# Add additional question
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Do not split the bill evenly.  Have each person ly pay for what they ordered, but don't forget the tip."
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Give a detailed breakdown of the bill and how it will be split and what is owed."
)

wait_on_run(run, thread)

messages = client.beta.threads.messages.list(
    thread_id=thread.id,
    order="asc",
    after=message.id
)

display_thread_messages(messages)

response = client.beta.assistants.delete(assistant.id)
