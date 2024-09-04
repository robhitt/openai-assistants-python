# "gpt-4o-mini"
# import os
# import time
# import pathlib

from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# client = OpenAI(
#     # Defaults to api_key=os.environ.get("OPENAI_API_KEY")
# )


# from openai import OpenAI

client = OpenAI()


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed
print(event)
