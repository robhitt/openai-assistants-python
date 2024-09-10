# Assistants have 3 specific types of TOOLS we can use:
# 1. code_interpreter
# 2. file_search
# 3. function calling

# We will use Function Calling for this example

import time
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI()


def word_definition_quiz(word, definition_options):
    print("Welcome to the word definition quiz!")
    print(f"What is the correct definition of the word: {word}?")

    word_definition_quiz([])
