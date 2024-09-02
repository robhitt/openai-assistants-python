import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

script_dir = os.path.dirname(os.path.abspath(__file__))
print('\n')
print('script_dir: ', script_dir)
print('\n')

# Construct the relative path to the file
relative_path = '../course-docs/02-Assistant-with-Knowledge-Retrieval/Wonka Chocolate Facility Rules.pdf'
filename = os.path.join(script_dir, relative_path)
filename = os.path.normpath(filename)

# file = client.files.create(
#     file=open(filename, 'rb'),
#     purpose='assistants'
# )
#
# print("file.id", file.id)
#
# print(file)

# file-v6OYyC6qSO6QI3Jo8D8ivUnX

for file in client.files.list():
    print(file.filename)

assistant = client.beta.assistants.create(
    name="Rules Explainer",
    instructions="You answer information about rules based on your knowledgebase of PDF files.",
    model="gpt-3.5-turbo-1106",
    tools=[{"type": "file_search"}]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='Can I bring my cat to the Wonka Chocolate Facility?',
    attachments=[{"file_id": "file-v6OYyC6qSO6QI3Jo8D8ivUnX", "tools": [{"type": "file_search"}]}]
)

print("------------------")
print(message)
print("------------------")

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    # instructions=""  If receiving an error that it can't find the file, f"use file with id: {file.id} to answer questions" }
)


def wait_on_run(run, thread):
    while run.status == 'queued' or run.status == 'in_progress':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        time.sleep(2)
        print(run.status)
    return run


wait_on_run(run, thread)

messages = client.beta.threads.messages.list(
    thread_id=thread.id,
    order='asc',
)


def display_thread_messages(thread_messages):
    for thread_message in thread_messages:
        print(thread_message.content[0].text.value)
        print("\n")


display_thread_messages(messages)