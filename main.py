import discord
import os
from alpacaUtils import getHighLow
from dotenv import load_dotenv
from commands import isValidCommand, executeCommand
from scrapeUtils import exchangeIsOpen
import datetime

load_dotenv('.env')

print(exchangeIsOpen("NYSE"))

# client = discord.Client()

# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     substr = str(message.content)
#     cmdIDX =  substr.find(" ")
#     if cmdIDX == -1:
#         command = substr
#     else:
#         command = substr[0:cmdIDX]
#     if isValidCommand(command):
#         await executeCommand(command, message)

# client.run(os.getenv('DISCORD_TOKEN'))