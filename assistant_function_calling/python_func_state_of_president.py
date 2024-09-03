import os
import pathlib
import time
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def president_home_state(president, state_options):
    """
    INPUTS:
        president str = The string name of a US President
        state_options list[str] = A list of potential states that the President was born in, with one of them being correct!

    OUTPUTS:
        response str = The response the user chose as the correct birthplace state.

    """
    print("Hello! Let's test your knowledge of the home states of US Presidents!")
    print(f"In what state was this president born: {president}\n")

    for num, option in enumerate(state_options):
        print('\n')
        print(f"Definition #{num} is: {option}")

    print('\n')
    num_choice = input("What is your choice? (Return the single number option)")

    return state_options[int(num_choice)]


function_json = {
    'type': 'function',
    'function': {
        'name': 'president_home_state',
        'parameters': {
            'type': 'object',
            'properties': {
                'president': {
                    'type': 'string',
                    'description': 'The name of a random US president.'
                },
                'state_options_list': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'A list of strings of US States, where only one is the state where the President was born.'
                }
            },
            'required': ['president', 'state_options_list']
        }
    }
}

assistant = client.beta.assistants.create(
    name='US President Birthplace Quiz',
    instructions='You help create a quiz where you give a US President and a list of birthplace states, where only one is the correct birthplace state. Then you grad ethe user response.',
    model='gpt-3.5-turbo-1106',
    tools=[function_json]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='Create a new quiz question with a US President and a list of potential birthplace states.  Then I will later send you my guess of the correct state and you will grade it.'
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


run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    # instructions=""
)

run_result = wait_on_run(run, thread)

# Extract single tool call
tool_call = run_result.required_action.submit_tool_outputs.tool_calls[0]
name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)

response = president_home_state(arguments['president'], arguments['state_options_list'])


run = client.beta.threads.runs.submit_tool_outputs(
    thread_id=thread.id,
    run_id=run.id,
    tool_outputs=[
        {
            'tool_call_id': tool_call.id,
            'output': json.dumps(response)
        }
    ]
)

messages = client.beta.threads.messages.list(thread.id)
for thread_message in messages:
    print(thread_message.content[0].text.value)
    print("\n")

response = client.beta.assistants.delete(assistant.id)
