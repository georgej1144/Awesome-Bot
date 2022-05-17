import discord as disc
from os import stat
import json

bot = disc.Bot()

# Paste the Guild IDs of the server's you'd like the bot to work in 
guilds = []

# Paste your Bot Token here
private_token = None

wordlist_template = {'words': []}

def load_json(guild_id: int):
    # if file is empty, create and initialize before reading
    if stat(f'{guild_id}_words.json').st_size == 0:
        save_json(guild_id, wordlist_template)

    # return saved word list as dictionary
    with open(f'{guild_id}_words.json', 'r') as file:
        return json.load(file)

def save_json(guild_id: int, new_dict: dict):
    # save provided dict to file
    with open(f'{guild_id}_words.json', 'w+') as file:
        json.dump(new_dict)

@bot.event
async def on_ready():   # idk some template shit
    print(f'We have logged in as {bot.user}')


@bot.slash_command(guild_ids=guilds)
async def list_words(ctx):
    gid = ctx.guild.id
    ret_str = ''
    try:
        words = load_json(gid)
        for word in words:
            ret_str = f'{ret_str}, {word}'
        await ctx.respond(ret_str[2:])
    except:
        print(f'Error loading words for guild {gid}')
        await ctx.respond("Error loading words from file.")
    

@bot.slash_command(guild_ids=guilds)
async def insert_word(ctx, arg):
    gid = ctx.guild.id
    try:
        words = load_json(gid)
        
        if arg in words['words']:   # check and handle duplicate entry
            await ctx.respond(f'The word \'{arg}\' already exists in this server\'s wordlist')
        else:   # non-duplicates
            words['words'].append(arg)
            save_json(gid, words)
            await ctx.respond(f'The word \'{arg}\' has been added to your wordlist')

    except:
        print(f'Error inserting word "{arg}" for guild {gid}')
        await ctx.respond("Error inserting word.")

@bot.slash_command(guild_ids=guilds)
async def remove_word(ctx, arg):
    gid = ctx.guild.id
    try:
        words = load_json(gid)

        if arg in words['words']:   # remove word if it exists in list
            words['words'].remove(arg)
            save_json(gid, words)
            await ctx.respond(f'The word \'{arg}\' has been removed from your wordlist')
        else:   # word not in list
            await ctx.respond(f'The word \'{arg}\' was not found in your wordlist')
    except:
        print(f'Error removing word "{arg}" for guild {gid}')
        await ctx.respond("Error removing word.")

bot.run(private_token)