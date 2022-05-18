from posixpath import split
import discord as disc
from os import stat
from os.path import exists
import json

bot = disc.Bot()

# Paste the Guild IDs of the server's you'd like the bot to work in 
guilds = []

# Paste your Bot Token here
private_token = ''

# Paste the ID of the role a user must have to 

wordlist_template = {'words': []}

def load_json(guild_id: int):
    # if file is empty, create and initialize before reading
    if not exists(f'{guild_id}_words.json') or stat(f'{guild_id}_words.json').st_size == 0:
        save_json(guild_id, wordlist_template)

    # return saved word list as dictionary
    with open(f'{guild_id}_words.json', 'r+') as file:
        return json.load(file)

def save_json(guild_id: int, new_dict: dict):
    # save provided dict to file
    with open(f'{guild_id}_words.json', 'w+') as file:
        json.dump(new_dict, file)

@bot.event
async def on_ready():   # idk some template shit
    print(f'We have logged in as {bot.user}')

word_group = bot.create_group(name="words", description='A set of commands to add, remove, and list words', guild_ids=guilds)

@word_group.command(name="list", description="List the words (comma separated)")
async def list_words(ctx):
    gid = ctx.interaction.guild_id
    ret_str = ''
    try:
        words = load_json(gid)
        for word in words['words']:
            ret_str = f'{ret_str}, {word}'
        if ret_str == '':
           await ctx.respond(f'The wordlist is empty, add words first to see them listed')
        else:
            with open(f'{gid}_list.txt', 'w+') as output:
                output.write(ret_str[2:])
            await ctx.respond(f"Word count: { len(words['words']) }", file=disc.File(f'{gid}_list.txt'))
            return
    except:
        print(f'Error loading words for guild {gid}')
        await ctx.respond("Error loading words from file.")
    

@word_group.command(name="add", description="Add a new word to the list")
async def insert_word(ctx, arg):
    gid = ctx.interaction.guild_id
    try:
        words = load_json(gid)
        
        split_input = [word.lower().strip() for word in arg.split(',')]    # split by commas. lowercase and clean individual words

        for word in split_input:
            if word in words['words']: # check and handle duplicate entry
                await ctx.respond(f'The word \'{word}\' already exists in this server\'s wordlist')
            else:   # non-duplicates
                words['words'].append(word)
                await ctx.respond(f'The word \'{word}\' has been added to your wordlist')
        save_json(gid, words)

    except:
        print(f'Error inserting word "{arg}" for guild {gid}')
        await ctx.respond("Error inserting word.")


@word_group.command(name="remove", description="Remove a word from the list")
@disc.default_permissions(manage_messages=True)
async def remove_word(ctx, arg):
    gid = ctx.interaction.guild_id
    try:
        words = load_json(gid)
        
        split_input = [word.lower().strip() for word in arg.split(',')]

        for word in split_input:
            if word in words['words']:   # remove word if it exists in list
                words['words'].remove(word)
                await ctx.respond(f'The word \'{word}\' has been removed from your wordlist')
            else:   # word not in list
                await ctx.respond(f'The word \'{word}\' was not found in your wordlist')
        save_json(gid, words)

    except:
        print(f'Error removing word "{arg}" for guild {gid}')
        await ctx.respond("Error removing word.")

bot.run(private_token)
