from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

do_not_delete_file_ids = [
    "file-v6OYyC6qSO6QI3Jo8D8ivUnX",
    "file-A5BZ7PkrUbDEFx9VoQ7cKxu5",
    "file-h7BZGVane2M4KjLwcg6548Ot",
    "file-IHe4TN3qKBbk4MLH6WcT8v1M",
    "file-uPmZvHVmq8wP3l4u1OjiCTxv",
    "file-fylsmz0nCUnUk64tzXjMTUFR",
]

files = client.files.list()

print(f"There are currently {len(files.data)} files on your openai account.")
for file in files:
    if file.id not in do_not_delete_file_ids:
        client.files.delete(file.id)

files = client.files.list()
print(f"After removal, there are currently {len(files.data)} files on your openai account.")
