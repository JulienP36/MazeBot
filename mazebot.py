import discord
import numpy as np
import asyncio
import sys
from random import sample
from time import sleep
from random import randint

client = discord.Client()

def make_maze(width, height):
    maze_table = np.zeros((height,width), dtype='i')
    for i in range(2, (height - 2), 1):
        for j in range(2, (width - 2), 1):
            if ((i % 2 == 0) and (j % 2 == 0)):
                maze_table[i][j] = 1
                direction = randint(1,4)
                if (direction == 1):
                    if (maze_table[i+1][j] == 1):
                        j -= 1
                    else:
                        maze_table[i+1][j] = 1
                elif (direction == 2):
                    if (maze_table[i-1][j] == 1):
                        j -= 1
                    else:
                        maze_table[i-1][j] = 1
                elif (direction == 3):
                    if (maze_table[i][j+1] == 1):
                        j -= 1
                    else:
                        maze_table[i][j+1] = 1
                else:
                    if (maze_table[i][j-1] == 1):
                        j -= 1
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
    if message.content.startswith('!help'):
        await message.channel.send("```Command list :\n\n!maze {width} {height} : generate a maze, minimum value is 5 and max value is 31\n    "
        "If given value is to big or small, the default one is used (11x11), same for no arguments\n    "
        "If only one argument is given, then the maze generate a square with given value\n!help : display available commands```")
    elif message.content.startswith('!maze'):
        width = 11
        height = 11
        try:
            width = int(message.content.split()[1])
            if ((width < 5) or (width > 31)):
                width = 11
                await message.channel.send("Argument too small or big, defaulting to 11\n")
            if (width % 2 == 0):
                width += 1
            try:
                height = int(message.content.split()[2])
                if ((height < 5) or (height > 31)):
                    height = 11
                    await message.channel.send("Argument too small or big, defaulting to 11\n")
                if (height % 2 == 0):
                    height += 1
            except Exception:
                height = width
                await message.channel.send("No height given\n")
                pass
        except Exception:
            await message.channel.send("No arguments given\n")
            pass
        maze_part = "generating " + str(width) + "x" + str(height) + " maze ...\n\n"
        maze_table = make_maze(width, height)
        for i in range(0, height, 1):
            for j in range(0, width, 1):
                if ((i == 1) and (j == 1)):
                    maze_part = maze_part + ':mouse:'
                elif ((i == height - 2) and (j == width - 2)):
                    maze_part = maze_part + ':cheese:'
                elif (maze_table[i][j] == 0):
                    maze_part = maze_part + '░░'
                else:
                    maze_part = maze_part + '██'
            maze_part = maze_part + '\n'
        await message.channel.send(maze_part)
client.run("bot token")