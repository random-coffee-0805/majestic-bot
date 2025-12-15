import discord
import asyncio
import os
from playwright.sync_api import sync_playwright

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1450256585313226946  # SEU ID AQUI

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def tirar_print():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto("https://taming.io", timeout=60000)

        page.wait_for_timeout(20000)  # espera o jogo carregar

        caminho = "/tmp/shop.png"
        page.screenshot(path=caminho, full_page=True)

        browser.close()
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
                content="🛒 Screenshot do Taming.io\nVerifique se há **Majestic Butterfly**",
                file=discord.File(imagem)
            )
        except Exception as e:
            print(e)

        await asyncio.sleep(900)  # 15 minutos

client.run(TOKEN)