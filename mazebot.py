import discord
import numpy as np
import asyncio
from random import sample
from time import sleep
from random import randint

width = 51
height = 51

client = discord.Client()

def make_maze():
    maze_table = np.zeros((height,width), dtype='i')
    for i in range(2, (height - 2), 1):
        for j in range(2, (width - 2), 1):
            if ((i % 2 == 0) and (j % 2 == 0)):
                maze_table[i][j] = 1
                direction = randint(1,4)
                if (direction == 1):
                    maze_table[i+1][j] = 1
                elif (direction == 2):
                    maze_table[i-1][j] = 1
                elif (direction == 3):
                    maze_table[i][j+1] = 1
                else:
                    maze_table[i][j-1] = 1
    for i in range(0, height, 1):
        for j in range(0, width, 1):
            if ((i == 0) or (j == 0) or (i == height - 1) or (j == width - 1)):
                maze_table[i][j] = 1
    print (maze_table)
    return maze_table

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!maze'):
        maze_table = make_maze()
        for i in range(0, height, 1):
            maze_part = ''
            for j in range(0, width, 1):
                if ((i == 1) and (j == 1)):
                    maze_part = maze_part + ':mouse:'
                elif ((i == height - 2) and (j == width - 2)):
                    maze_part = maze_part + ':cheese:'
                elif (maze_table[i][j] == 0):
                    maze_part = maze_part + '░░'
                else:
                    maze_part = maze_part + '██'
            await client.send_message(message.channel, maze_part)
client.run('bot_secret_token')