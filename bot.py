import discord
import asyncio
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = COLE_AQUI_O_ID_DO_CANAL
ITEM = "majestic butterfly"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def verificar():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://taming.io")
    driver.implicitly_wait(25)

    achou = ITEM in driver.page_source.lower()
    driver.quit()
    return achou

@client.event
async def on_ready():
    print("Bot online")
    client.loop.create_task(loop())

async def loop():
    canal = client.get_channel(CHANNEL_ID)

    while True:
        try:
            existe = await asyncio.to_thread(verificar)
            if existe:
                await canal.send("🦋 **Majestic Butterfly disponível no Taming.io!**")
                await asyncio.sleep(3600)
        except:
            pass

        await asyncio.sleep(600)

client.run(TOKEN)
