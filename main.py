import json
import asyncio
from telethon import TelegramClient

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

async def main():
    target = input("Group/channel name, @username, link or ID: ").strip()
    limit = int(input("Number of messages to delete: "))

    client = TelegramClient("session", config["api_id"], config["api_hash"])
    await client.start()

    await client.get_dialogs()
    
    if target.lstrip("-").isdigit():
        target = int(target)
    
    entity = await client.get_entity(target)

    deleted = 0
    async for message in client.iter_messages(entity, limit=limit, from_user="me"):
        await client.delete_messages(entity, [message.id], revoke=True)

        deleted += 1
        print(f"[{deleted}/{limit}] Message {message.id} deleted")

        await asyncio.sleep(config["delay"])

    print(f"{deleted} messages deleted")
    await client.disconnect()

asyncio.run(main())
