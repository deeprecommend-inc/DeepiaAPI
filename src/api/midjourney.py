# https://medium.com/@neonforge/how-to-automate-midjourney-image-generation-with-python-and-gui-automation-ac9ca5f747ae
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pyautogui as pg

discord_token = "YOUR_DISCORD_TOKEN"
load_dotenv()
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())

def exec_midjourney(prompt):
    prompt_counter = 0

    msg = prompt.content

    while prompt_counter < len(prompts):
        # Start Automation by typing "automation" in the discord channel
        if msg == 'automation':
            time.sleep(3)
            pg.press('tab')
            for i in range(1):
                time.sleep(3)
                pg.write('/imagine')
                time.sleep(5)
                pg.press('tab')
                pg.write(prompt)
                time.sleep(3)
                pg.press('enter')
                time.sleep(5)
                prompt_counter += 1

        # continue Automation as soon Midjourney bot sends a message with attachment.
        for attachment in message.attachments:
            time.sleep(3)
            pg.write('/imagine')
            time.sleep(5)
            pg.press('tab')
            pg.write(prompts[prompt_counter])
            time.sleep(3)
            pg.press('enter')
            time.sleep(5)
            prompt_counter += 1
    
    return attachment
