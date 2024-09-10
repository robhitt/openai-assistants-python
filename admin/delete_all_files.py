from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

do_not_delete_file_ids = []

files = client.files.list()

print(f"There are currently {len(files.data)} files on your openai account.")
for file in files:
    if file.id not in do_not_delete_file_ids:
        client.files.delete(file.id)

files = client.files.list()
print(f"After removal, there are currently {len(files.data)} files on your openai account.")
