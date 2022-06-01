import discord as disc
from os import stat
from os.path import exists
import json
import logging

logging.basicConfig(filename="interactions.log", level=logging.INFO)

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

def slice(arr, start, end):
    return arr[:start] + arr[end:]

@bot.event
async def on_ready():   # idk some template shit
    print(f'Started successfully as {bot.user}')

word_group = bot.create_group(name="words", description='A set of commands to add, remove, and list words', guild_ids=guilds)

@word_group.command(name="list", description="List the words (comma separated)")
async def list_words(ctx):
    gid = ctx.interaction.guild_id
    logging.info(f'User {ctx.interaction.user.name} (id:{ctx.interaction.user.id}) listing words in guild \'{ctx.interaction.guild.name}\' (id: {gid})')
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
            # await ctx.respond(f"Word count: { len(words['words']) }", file=disc.File(f'{gid}_list.txt'))
            await ctx.respond(file=disc.File(f'{gid}_list.txt'))
    except:
        logging.error(f'Error loading words. Invoked by {ctx.interaction.user.name} (id: {ctx.interaction.user.id}) in channel \'{ctx.interaction.channel.name}\' (id: {ctx.interaction.channel_id}) in guild \'{ctx.interaction.guild.name}\' (id: {gid}).')
        await ctx.respond("Error loading words from file.")
    

@word_group.command(name="add", description="Add a new word to the list")
async def insert_word(ctx, word):
    gid = ctx.interaction.guild_id
    logging.info(f'User {ctx.interaction.user.name} (id:{ctx.interaction.user.id}) adding word(s) \'{word}\' in guild \'{ctx.interaction.guild.name}\' (id: {gid})')
    try:
        words = load_json(gid)
        
        split_input = [to_insert.lower().strip() for to_insert in word.split(',')]    # split by commas. lowercase and clean individual words

        for to_insert in split_input:
            if to_insert in words['words']: # check and handle duplicate entry
                await ctx.respond(f'The word \'{to_insert}\' already exists in this server\'s wordlist')
            else:   # non-duplicates
                words['words'].append(to_insert)
                await ctx.respond(f'The word has been added to your wordlist')
        save_json(gid, words)

    except:
        logging.error(f'Error inserting word(s). Invoked by {ctx.interaction.user.name} (id: {ctx.interaction.user.id}) in channel \'{ctx.interaction.channel.name}\' (id: {ctx.interaction.channel_id}) in guild \'{ctx.interaction.guild.name}\' (id: {gid}). Word(s): {word}')
        await ctx.respond("Error inserting word.")


@word_group.command(name="count", description="See how many words are in the list")
async def count_words(ctx):
    gid = ctx.interaction.guild_id
    logging.info(f'User {ctx.interaction.user.name} (id:{ctx.interaction.user.id}) getting word count in guild \'{ctx.interaction.guild.name}\' (id: {gid})')
    try:
        words = load_json(gid)
        await ctx.respond(f"Word count: {len(words['words'])}")
    except:
        logging.error(f'Error getting word count. Invoked by {ctx.interaction.user.name} (id: {ctx.interaction.user.id}) in channel \'{ctx.interaction.channel.name}\' (id: {ctx.interaction.channel_id}) in guild \'{ctx.interaction.guild.name}\' (id: {gid}).')
        await ctx.respond(f"Error getting word count.")


@word_group.command(name="remove", description="Remove a word from the list")
@disc.default_permissions(manage_messages=True)
async def remove_word(ctx, word):
    gid = ctx.interaction.guild_id
    logging.info(f'User {ctx.interaction.user.name} (id:{ctx.interaction.user.id}) removing word(s) \'{word}\' in guild \'{ctx.interaction.guild.name}\' (id: {gid})')
    try:
        words = load_json(gid)
        
        split_input = [to_remove.lower().strip() for to_remove in word.split(',')]

        for to_remove in split_input:
            if to_remove in words['words']:   # remove word if it exists in list
                words['words'].remove(to_remove)
                await ctx.respond(f'The word \'{to_remove}\' has been removed from your wordlist')
            else:   # word not in list
                await ctx.respond(f'The word \'{to_remove}\' was not found in your wordlist')
        save_json(gid, words)
    except:
        logging.error(f'Error removing word(s). Invoked by {ctx.interaction.user.name} (id: {ctx.interaction.user.id}) in channel \'{ctx.interaction.channel.name}\' (id: {ctx.interaction.channel_id}) in guild \'{ctx.interaction.guild.name}\' (id: {gid}). Word(s): {word}')
        await ctx.respond("Error removing word.")

@word_group.command(name="find", description="Find the index of a word in the list")
async def find_word(ctx, word):
    gid = ctx.interaction.guild_id
    logging.info(f'User {ctx.interaction.user.name} (id:{ctx.interaction.user.id}) finding word {word} in guild \'{ctx.interaction.guild.name}\' (id: {gid})')
    try:
        words = load_json(gid)
        await ctx.respond(f"Word \'{word}\' found at index {words['words'].index(word)}")
    except(ValueError):
        await ctx.respond(f'Word \'{word}\' is not in the wordlist.')
    except:
        logging.error(f'Error finding word. Invoked by {ctx.interaction.user.name} (id: {ctx.interaction.user.id}) in channel \'{ctx.interaction.channel.name}\' (id: {ctx.interaction.channel_id}) in guild \'{ctx.interaction.guild.name}\' (id: {gid}).')
        await ctx.respond("Error loading words from file.")

@word_group.command(name="massdel", description="Delete all words between two given indeces")
@disc.default_permissions(manage_messages=True)
async def massdel(ctx, start_index, end_index):
    gid = ctx.interaction.guild_id
    logging.info(f'User {ctx.interaction.user.name} (id:{ctx.interaction.user.id}) mass deleting between {start_index} and {end_index} in guild \'{ctx.interaction.guild.name}\' (id: {gid})')
    try:
        words = load_json(gid)
        save_json(gid, slice(words, start_index, end_index))
        await ctx.respond(f'Words between \'{start_index}\' and \'{end_index}\' deleted. You better not have boofed it.')
    except:
        logging.error(f'Error on mass delete. Invoked by {ctx.interaction.user.name} (id: {ctx.interaction.user.id}) in channel \'{ctx.interaction.channel.name}\' (id: {ctx.interaction.channel_id}) in guild \'{ctx.interaction.guild.name}\' (id: {gid}).')
        await ctx.respond(f'You boofed something. Check the list before trying this again.')


bot.run(private_token)
