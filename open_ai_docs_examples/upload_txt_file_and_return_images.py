# NOTE --> Walk through with .txt file, .csv files are not currently supported

import time
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI()

file = client.files.create(
    file=open("SP500_Prices_5Year.txt", "rb"),
    purpose='assistants'
)
file_id = file.id
# file_id = ''

assistant = client.beta.assistants.create(
    name="S&P 500 Data Visualizer",
    # instructions="You are great at creating beautiful data visualizations. You analyze data present in .txt files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
    description="You are great at creating beautiful data visualizations. You analyze data present in .txt files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}],
    tool_resources={
        "code_interpreter": {
            "file_ids": [file_id]
        }
    }
)
assistant_id = assistant.id
# assistant_id = ""

thread = client.beta.threads.create()

# Messages can contain text, images, or file attachment.
# Message attachments are helper methods that add files to a thread's tool_resources.
# You can also choose to add files to the thread.tool_resources directly.
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Create 2 data visualizations based on the trends in this file.",
    attachments=[{
        "file_id": file_id,
        "tools": [{"type": "code_interpreter"}]
    }]
)

# https://platform.openai.com/docs/assistants/deep-dive/runs-and-run-steps
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,

    # The below arguments are available to override the previously
    # create assistant instructions, model, and tools if need be.
    # model="gpt-4o",
    # instructions="New instructions that override the Assistant instructions",
    # tools=[{"type": "code_interpreter"}, {"type": "file_search"}]

    # Note: tool_resources associated w the assistant can no be overridden here.
    # However, you can use the modify assistant endpoint.
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
            print("=====================")
            print('image here')
            print(thread_message.content[1].text.value)

            image = client.files.content(thread_message.content[0].image_file.file_id)
            image_bytes = image.read()  # my_file.content will also work

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f'ai_image_{timestamp}.png'
            with open(filename, 'wb') as file:
                file.write(image_bytes)

        else:
            print("=====================")
            print(thread_message.content[0].text.value)


display_thread_messages(messages)

# Delete Recent File
# client.files.delete(file_id)

# Recent Assistant
# client.beta.assistants.delete(assistant_id)


# Using the file_search Tool we can search for the file to utilize in our message query
# assistant = client.beta.assistants.create(
#     name="Financial Analyst Assistant",
#     instructions="You are an expert financial analyst. You analyze data present in .csv files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
#     model="gpt-4o",
#     tools=[{"type": "file_search"}],
# )
# assistant_id = "asst_cLNJ1YGLzQvdhjwkDqzoSu71"

# =============== Create vectors from files and upload ===============
# Create a vector store
# vector_store = client.beta.vector_stores.create(
#     name="S&P 500 financial Statements",
#     expires_after={
#         "anchor": "last_active_at",
#         "days": 7
#     }
# )

# Ready the files for upload to OpenAI
# file_paths = ["SP500_Prices_5Year.txt"]
# file_streams = [open(path, "rb") for path in file_paths]

# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#     vector_store_id=vector_store.id, files=file_streams
# )

# You can print the status and the file counts of the batch to see the result of this operation.
# print(file_batch.status)
# print(file_batch.file_counts)
#
# assistant = client.beta.assistants.update(
#     assistant_id=assistant_id,
#     tool_resources={
#         "file_search": {
#             "vector_store_ids": [vector_store.id]
#         }
#     }
# )
#
# thread = client.beta.threads.create()
#
# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     # content="Create 3 data visualizations based on the trends in this file.",
#     content="What is the general trend of the S&P 500?",
#     # attachments=[{
#     #     "file_id": file_id,
#     #     "tools": [{"type": "code_interpreter"}]
#     # }]
# )
#
# print(thread.tool_resources.file_search)
#
#
# # https://platform.openai.com/docs/assistants/deep-dive/runs-and-run-steps
# run = client.beta.threads.runs.create_and_poll(
#     thread_id=thread.id,
#     assistant_id=assistant_id,
#
#     # The below arguments are available to override the previously
#     # create assistant instructions, model, and tools if need be.
#     # model="gpt-4o",
#     # instructions="New instructions that override the Assistant instructions",
#     # tools=[{"type": "code_interpreter"}, {"type": "file_search"}]
#
#     # Note: tool_resources associated w the assistant can no be overridden here.
#     # However, you can use the modify assistant endpoint.
# )
#
#
# def wait_on_run(run, thread):
#     while run.status == 'queued' or run.status == 'in_progress':
#         run = client.beta.threads.runs.retrieve(
#             thread_id=thread.id,
#             run_id=run.id
#         )
#         time.sleep(3)
#         print(run.status)
#     return run
#
#
# wait_on_run(run, thread)
#
# messages = client.beta.threads.messages.list(
#     thread_id=thread.id,
#     order='asc'
# )
#
#
# def display_thread_messages(thread_messages):
#     for thread_message in thread_messages:
#         if thread_message.content[0].type == 'image_file':
#             print('image here')
#             print(thread_message.content[1].text.value)
#
#             my_file = client.files.content(thread_message.content[0].image_file.file_id)
#
#             with open('example_image.png', 'wb') as file:
#                 file.write(my_file.content)
#
#             print('\n')
#         else:
#             print(thread_message.content[0].text.value)
#             print("\n")
#
#
# display_thread_messages(messages)
#
# # Delete Recent File
# client.files.delete(file_id)
#
# # Recent Assistant
# client.beta.assistants.delete(assistant_id)
