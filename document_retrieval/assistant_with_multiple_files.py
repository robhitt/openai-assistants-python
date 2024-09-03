import os
import pathlib
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# If you want to delete all assistants on server programattically
# my_assistants = client.beta.assistants.list(order='desc')
#
# for assistant in my_assistants:
#     id = assistant.id
#     client.beta.assistants.delete(id)


# Initial upload of files, only do once so commenting out
# current_dir = pathlib.Path(__file__).parent
# relative_path = '../course-docs/02-Assistant-with-Knowledge-Retrieval/02-Multiple-Files'
#
# files_to_upload = [
#     'ACME Advertising Policy.pdf',
#     'ACME_Dog_Food_Ingredients.pdf',
#     'Corporate Travel Policy.pdf'
# ]
#
#
# def upload_assistant_file(filename):
#     file_path = (current_dir / relative_path / filename).resolve()
#     uploaded_file = client.files.create(file=open(file_path, 'rb'), purpose='assistants')
#     print(uploaded_file.id)
#
#
# for file in files_to_upload:
#     upload_assistant_file(file)

# file-IHe4TN3qKBbk4MLH6WcT8v1M
# file-uPmZvHVmq8wP3l4u1OjiCTxv
# file-fylsmz0nCUnUk64tzXjMTUFR

# for file in client.files.list():
#     print(file.filename)
#     print(file.id)
#     print("\n")

# assistant = client.beta.assistants.create(
#     name='add name here'
#     instructions='You answer information about the company based on the PDF documents available in your knowledge base.',
#     model='gpt-3.5-turbo-1106',
#     tools=[{'type': 'file_search'}, {'type': 'code_interpreter'}],
#     tool_resources={
#         "code_interpreter": {
#             "file_ids": [
#                 'file-IHe4TN3qKBbk4MLH6WcT8v1M',
#                 'file-uPmZvHVmq8wP3l4u1OjiCTxv',
#                 'file-fylsmz0nCUnUk64tzXjMTUFR'
#             ]
#         }
#     }
# )

assistant_id = 'asst_2urNcRd6jmOCTufuAuUjaS8X'

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='Does our dog food allow for artificial ingredients?',
    attachments=[
        {'file_id': "file-IHe4TN3qKBbk4MLH6WcT8v1M", 'tools': [{'type': 'file_search'}, {"type": "code_interpreter"}]},
        {'file_id': "file-uPmZvHVmq8wP3l4u1OjiCTxv", 'tools': [{'type': 'file_search'}, {"type": "code_interpreter"}]},
        {'file_id': "file-fylsmz0nCUnUk64tzXjMTUFR", 'tools': [{'type': 'file_search'}, {"type": "code_interpreter"}]},
    ]
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
    # instructions="Use the file with file_id file-uPmZvHVmq8wP3l4u1OjiCTxv to answer."
)


def wait_on_run(run, thread):
    while run.status == 'queued' or run.status == 'in_progress':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        time.sleep(3)
        print(run.status)
    return run


wait_on_run(run, thread)

messages = client.beta.threads.messages.list(
    thread_id=thread.id,
    order='asc'
)


def display_thread_messages(thread_messages):
    for thread_message in thread_messages:
        if thread_message.content[0].type == 'image_file':
            print('image here')
            print(thread_message.content[1].text.value)

            my_file = client.files.content(thread_message.content[0].image_file.file_id)

            with open('example_image.png', 'wb') as file:
                file.write(my_file.content)

            print('\n')
        else:
            print(thread_message.content[0].text.value)
            print("\n")


display_thread_messages(messages)
