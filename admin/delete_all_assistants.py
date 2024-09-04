from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

assistants = client.beta.assistants.list()
print(f"There are currently {len(assistants.data)} assistants on your openai account.")

for assistant in assistants:
    id = assistant.id
    deleted_assistant_info = client.beta.assistants.delete(id)
    print(f"Deleted assistant {assistant.name} with id: {deleted_assistant_info.id}.")

assistants = client.beta.assistants.list()

print("=============================================")

print(f"After removal, there are currently {len(assistants.data)} assistants on your openai account.")
