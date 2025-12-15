import discord
import asyncio
import os
from playwright.sync_api import sync_playwright

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 123456789012345678  # SEU ID AQUI

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def tirar_print_shop():
    print("Iniciando Playwright...")
    with sync_playwright() as p:
        print("Abrindo Chromium...")
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-gpu"]
        )

        page = browser.new_page(
            viewport={"width": 1920, "height": 1080}
        )

        print("Abrindo taming.io...")
        page.goto("https://taming.io", timeout=60000)

        print("Aguardando carregamento do jogo...")
        page.wait_for_timeout(30000)

        print("Clicando na shop...")
        page.mouse.click(1850, 80)

        page.wait_for_timeout(6000)

        caminho = "/tmp/shop.png"
        print("Tirando screenshot...")
        page.screenshot(path=caminho)

        browser.close()
        print("Screenshot pronta!")
        return caminho

@client.event
async def on_ready():
    print("Bot online")
    client.loop.create_task(loop())

async def loop():
    canal = client.get_channel(CHANNEL_ID)

    while True:
        try:
            imagem = await asyncio.to_thread(tirar_print_shop)
            await canal.send(
                content="🛒 **Shop do Taming.io** (screenshot)",
                file=discord.File(imagem)
            )
        except Exception as e:
            print("ERRO NO LOOP:", e)
            await canal.send(f"❌ Erro ao gerar screenshot:\n```{e}```")

        await asyncio.sleep(900)

client.run(TOKEN)