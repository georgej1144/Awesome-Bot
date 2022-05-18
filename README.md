# Awesome Bot
Maintains a word list for each server the bot is added to. Each server's words are stored in separate JSON files by Server ID.

## How to add
- Create an application through the discord developer portal
- Create a Bot user inside the application
- Copy your bot token and paste it into bot.py `private_token = 'your token'`
- Copy the Guild IDs of any servers you'd like to add the bot to into and paste them into bot.py `guilds = [guild_id1, guild_id2, guild_id3]`
- In your application in the developer portal, click OAuth2 then URL Generator
- Select `application.commands`, `bot`, and `Use Slash Commands`
- Use the generated URL to finish adding the bot to the servers you'd like

## How to use
- /words list
    - Get every word that's been added to the server's list in a comma separated list
- /words add \[arg\]
    - Add the provided word to the server's list
- /words remove \[arg\]
    - Remove the provided word from the server's list
