Welcome to discordRadioBot! This is a Python-based Discord bot that can play an internet radio stream! It was made specifically to compliment an [AzuraCast](https://www.azuracast.com/) installation but should work with any internet radio stream.

---
# Deployment
The intended deployment method is to use a Docker container. You can alternatively use any host with Python and just run the bot.py directly, but this requires extra steps.
## Docker
The Docker container takes two environment variables: your bot's token and a stream's URL.

### Using Docker Compose
Before you create the compose file, you will need to create a file for your environment variables. Let's create a file called `.env` and then paste the following contents:
```env
BOT_TOKEN=
STREAM_URL=
```
Now enter your Discord bot's token (Client Secret in the OAuth section) and a URL to the internet radio's stream. Here's an example of what a completed env file would look like:
```env
BOT_TOKEN=secretsecretsecretsecretsecretsecretsecret
STREAM_URL="https://yourdomain.tld/listen/stationName/radio.mp3"
```

Now that we have our env file ready, we can create the compose file. Create a file named `docker-compose.yml` and paste the following contents:
```yml
services:
  discordRadioBot:
    image: ghcr.io/maximized490/discordradiobot:latest
    restart: unless-stopped
    env_file: ".env"
```
Now we're ready to start our container.
`docker-compose up -d`
If we run `docker logs discordRadioBot`, we should see...
```
YYYY-MM-DD HH:MM:SS INFO     discord.client logging in using static token
YYYY-MM-DD HH:MM:SS INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: blahblahblahblahblahblahblahblah).
Logged in as A Discord Bot's Name
```

### Using `docker run`
Before you create the container, you will need to create a file for your environment variables. Let's create a file called `.env` and then paste the following contents:
```env
BOT_TOKEN=
STREAM_URL=
```
Now enter your Discord bot's token (Client Secret in the OAuth section) and a URL to the internet radio's stream. Here's an example of what a completed env file would look like:
```env
BOT_TOKEN=secretsecretsecretsecretsecretsecretsecret
STREAM_URL="https://yourdomain.tld/listen/stationName/radio.mp3"
```

Now that we have our env file ready, we can create the container.
```bash
docker run -d --restart unless-stopped \
  --name "discordRadioBot" \
  --env-file .env \
  ghcr.io/maximized490/discordradiobot:latest
```
Now we should have a container! If we run `docker logs discordRadioBot`, we should see...
```
YYYY-MM-DD HH:MM:SS INFO     discord.client logging in using static token
YYYY-MM-DD HH:MM:SS INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: blahblahblahblahblahblahblahblah).
Logged in as A Discord Bot's Name
```
## Local
As long as you have Python installed on your computer, you should be able to simpylk download the bot.py file and run it. The file expects two environment variables which you can set before running the code.
> [!CAUTION]
> Setting the environment variables in the way shown below is not the "proper" way to handle sensitive information like a bot token.

### Linux/macOS
`STREAM_URL="yourStreamsURL" BOT_TOKEN="secret" python bot.py`
### Windows
`set STREAM_URL="yourStreamsURL" && set BOT_TOKEN="secret" && python bot.py
`

---
# Usage
Let's see how to invite the bot to our server and what commands we can use.
## Invite Bot
Before you invite your bot, you will need to give it a special permission called Nessage Content Intent. You can find it in the Bot tab under the Privileged Gateway Intents section. Simply toggle on that setting and you'll be good to go.

The bot will need the following permissions: View Channels, Send Messages, Read Message History, Connect, and Speak. This equates to the integer `3214336` in Discord's numeric-based permission system. You can use the following pre-configured invite link to add your bot to your server:<br>
`https://discord.com/oauth2/authorize?client_id=yourBotsClientID&scope=bot&permissions=3214336`<br>
Replace the "yourBotsClientID" placeholder with your bot's Client ID, found on either the General Information or OAuth tabs. Below is an example URL assuming our Client ID was `12345`.<br>
`https://discord.com/oauth2/authorize?client_id=12345&scope=bot&permissions=3214336`

## Commands

**radio!join**<br>
Joins the voice channel that the requestor is in.

**radio!leave**<br>
Leaves the current voice channel. This also resets settings like volume.

**radio!volume <1-100>**<br>
Sets the bot's internal volume on a scale from 1 to 100. This equates to 1-100% user volume.

**radio!pause** / **radio!unpause**<br>
**radio!mute** / **radio!unmute**<br>
Pauses and unpauses the radio stream.
