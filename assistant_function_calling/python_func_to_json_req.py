import os
import pathlib
import time
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def word_definition_quiz(word, definition_options):
    print("Welcome to the word quiz!")
    print(f"What is the correct definition of this word: {word}")

    print('\n')
    for num, option in enumerate(definition_options):
        print(f'Definition #{num} is: {option}')

    num_choice = input("What is your choice? Return the #Num Option")
    return definition_options[int(num_choice)]


# word_definition_quiz("hello", ['greeting', 'farewell', 'sandwich'])

function_json = {
    'type': 'function',
    'function': {
        'name': 'word_definition_quiz',
        'parameters': {
            'type': 'object',
            'properties': {
                'word': {
                    'type': 'string',
                    'description': 'A random word'
                },
                'definition_options': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'A Python list of strings of definitions, where only one is the correct definition for the word'
                }
            },
            'required': ['word', 'definition_options']
        }
    }
}

instructions = "You help create a quiz for checking definitions of words, providing a word and then multiple definition options, where only one option is correct."

# assistant = client.beta.assistants.create(
#     name="Word Quiz Game",
#     instructions=instructions,
#     model='gpt-3.5-turbo',
#     tools=[function_json]
# )
# assistant_id = assistant.id
assistant_id = 'asst_h6MWL0xgG01KV3ShbOmaz4NP'

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content="Create a new quiz question word and definition list. Then let me know know if the student answer received is correct."
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
    assistant_id=assistant_id,
    # instructions=""
)

run_result = wait_on_run(run, thread)

# print(run_result.status)
# print(run_result.required_action.submit_tool_outputs)
# print(run_result.required_action.submit_tool_outputs.tool_calls[0])
tool_call = run_result.required_action.submit_tool_outputs.tool_calls[0]
name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)
# print(arguments['word'])
# print(arguments['definition_options'])

response = word_definition_quiz(arguments['word'], arguments['definition_options'])

run = client.beta.threads.runs.submit_tool_outputs(
     thread_id=thread.id,
     run_id=run.id,
     tool_outputs=[{
         'tool_call_id': tool_call.id,
         'output': json.dumps(response)
     }]
 )

run = wait_on_run(run, thread)

messages = client.beta.threads.messages.list(thread.id)
for thread_message in messages:
    print(thread_message.content[0].text.value)
    print("\n")
