import discord
import asyncio
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1450256585313226946

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def tirar_print():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get("https://taming.io")
    driver.implicitly_wait(25)

    # 👉 clique genérico (a shop abre pelo jogo)
    driver.find_element("tag name", "canvas").click()
    driver.implicitly_wait(10)

    caminho = "/tmp/shop.png"
    driver.save_screenshot(caminho)
    driver.quit()
    return caminho

@client.event
async def on_ready():
    print("Bot online")
    client.loop.create_task(loop())

async def loop():
    canal = client.get_channel(CHANNEL_ID)

    while True:
        try:
            imagem = await asyncio.to_thread(tirar_print)
            await canal.send(
                content="🛒 Screenshot da shop do Taming.io\nVerifique se há **Majestic Butterfly**",
                file=discord.File(imagem)
            )
        except Exception as e:
            print(e)

        await asyncio.sleep(900)  # 15 minutos

client.run(TOKEN)