import os
import time
import pathlib

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Construct the relative path to the file
current_dir = pathlib.Path(__file__).parent
relative_path = '../admin_course_docs/02-Assistant-with-Knowledge-Retrieval/SP500_Prices_5Year.csv'
filename = (current_dir / relative_path).resolve()

client = OpenAI()

file = client.files.create(
    file=open(filename, 'rb'),
    purpose='assistants'
)
file_id = file.id  # ''

assistant = client.beta.assistants.create(
    name="Stock visualizer",
    instructions="Use this csv file to use code to help visualize stock data",
    model="gpt-4o-mini",
    # tools=[{'type': 'file_search'}],  # OpenAI no longer handles file_search for csv files, converted to txt
    tools=[{'type': 'code_interpreter'}],
    tool_resources={
        "code_interpreter": {
            "file_ids": [file_id]
        }
    }
)
assistant_id = assistant.id
# assistant_id = ''  # saved id to avoid recreating an assistant every time

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='Can you create a plot of the historical adjusted closing price of the S&P 500? The first row in the file are the column names separated by commas. All the data is comma separated similar to a CSV file.',
    attachments=[{
        'file_id': file_id,
        'tools': [{"type": "code_interpreter"}],
    }]
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
    # instructions=f"Use file {file_id} to answer the questions. The first row are the column names. All data is comma separated."
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

            with open('rob_example_image.png', 'wb') as file:
                file.write(my_file.content)

            print('\n')
        else:
            print(thread_message.content[0].text.value)
            print("\n")


display_thread_messages(messages)




