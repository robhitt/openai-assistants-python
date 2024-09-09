# Assistants have 3 specific types of TOOLS we can use:
# 1. code_interpreter
# 2. file_search
# 3. function calling

# In this example we are using the code_interpreter too
# to upload a CSV file and return images
import time
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI()

file = client.files.create(
    file=open("SP500_Prices_5Year.csv", "rb"),
    purpose='assistants'
)
file_id = file.id
# file_id = ''

assistant = client.beta.assistants.create(
    name="S&P 500 Data Visualizer",
    instructions="Analyze data in the provided CSV file, create visualizations, and provide a summary of trends.",

    # Description is more general, if both instructions and description are provided, the instructions are used.
    # description="You are great at creating beautiful data visualizations. You analyze data present in .csv files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
    model="gpt-4o-mini",
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
    content="Create 2 data visualizations based on the trends in your file.",

    # Since the assistant already has the file in its context, you can omit the attachments argument when creating the message,
    # and the assistant will still be able to use the file for generating visualizations.
    # attachments=[{
    #     "file_id": file_id,
    #     "tools": [{"type": "code_interpreter"}]
    # }]
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

    # Note: tool_resources associated w the assistant can not be overridden here.
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
client.files.delete(file_id)

# Recent Assistant
client.beta.assistants.delete(assistant_id)
