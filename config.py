from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("15527090"))
API_HASH = getenv("33e43e71a6d85dde11988e70b6980a0e")

BOT_TOKEN = getenv("7995860392:AAGAdTb83LrJ3Bdj3QOC2F2aBUznrvy3W4A")
OWNER_ID = int(getenv("8044097780"))

MONGO_DB_URI = getenv("mongodb+srv://Mahoaga:<db_1234554321m>@cluster0.8ni5ega.mongodb.net/")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/ultroidofficial_chat")
