
from discord.ext import tasks
from os import getenv
from dotenv import load_dotenv
load_dotenv()

from discord import Client, Intents
client = Client(intents=Intents.default())

# setting trigger time
from datetime import time, timezone
utc = timezone.utc
trigger_time = time(hour=5, minute=30, tzinfo=utc)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    trigger_wotd.start()


@tasks.loop(time=trigger_time)
async def trigger_wotd():
    from wordnik.word import WordNik
    channel = client.get_channel((int(getenv("WOTD_CHANNEL"))))
    from datetime import date, datetime
    cur_date = date.today()
    date_iso = cur_date.isoformat()
    word_text = WordNik().get_WOTD(date_iso)

    x_date = datetime.now()
    today = x_date.strftime("%A,%d %B, %Y")
    caption = f'WordNik API Present: Word of the day [{today}]\n{word_text}'
    await channel.send(caption)

client.run(getenv("BOT_TOKEN"))
