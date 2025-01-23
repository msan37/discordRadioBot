Welcome to discordRadioBot! This is a Python-based Discord bot that can play an internet radio stream! It was made specifically to compliment an [AzuraCast](https://www.azuracast.com/) installation but should work with any internet radio stream.

---
# Deployment
The intended deployment method is to use a Docker container. You can alternatively use any host with Python and just run the bot.py directly, but this requires extra steps.
## Docker
Before using either Docker method, you will need to create a file for your environment variables. Let's create a file called `.env` and then paste the following contents:
```env
BOT_TOKEN=
OVERWRITE_STREAMS=
```
For the BOT_TOKEN, just enter your Discord bot's token (Client Secret in the OAuth section).
The OVERWRITE_STREAMS variable is used to specify a list of stations your bot can switch between. It is in JSON format. You need ot specify a station name followed by its URL.
> [!NOTE]
> The `OVERWRITE_STREAMS` environment variable is optional and will overwrite all streams the bot knows. It will need to be used at least once to initialize the bot. If you're not using persistent storage then you'll need to leave it set so that it can properly re-initialize its internal list of stations upon reset.
```env
BOT_TOKEN=secretsecretsecretsecretsecretsecretsecret
OVERWRITE_STREAMS= >
  {
    "Station 1": "https://yourdomain.tld/listen/station1/radio.mp3",
    "Station 2": "https://yourdomain.tld/listen/station2/listen.mp3"
  }
```

### Using Docker Compose
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
#### Example docker-compose.yml
This is an example of a complete compose file. You can use this in something like Portainer (what I do personally).
```yml
services:
  bot:
    image: ghcr.io/maximized490/discordradiobot:latest #You should change this to the latest release version so that your bot doesn't break when I push breaking updates. 
    restart: unless-stopped
    environment:
      BOT_TOKEN: ${BOT_TOKEN}
      OVERWRITE_STREAMS: >
        {
          "Station 1": "https://yourdomain.tld/listen/station1/radio.mp3",
          "Station 2": "https://yourdomain.tld/listen/station2/listen.mp3"
        }
      DEFAULT_VOLUME: 0.25
      DEFAULT_VOLUME_OFFSET: 0.10
```

### Using `docker run`
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
As long as you have Python installed on your computer, you should be able to simply download the bot.py file and run it. The file expects two environment variables which you can set before running the code.
> [!CAUTION]
> Setting the environment variables in the way shown below is not the "proper" way to handle sensitive information like a bot token.
### Linux/macOS
<code>OVERWRITE_STREAMS=`{"Station 1":"https://yourdomain.tld/listen/station1/radio.mp3","Station 2":"https://yourdomain.tld/listen/station2/listen.mp3"}` BOT_TOKEN="secret" python bot.py</code>
### Windows
<code>set OVERWRITE_STREAMS=`{"Station 1":"https://yourdomain.tld/listen/station1/radio.mp3","Station 2":"https://yourdomain.tld/listen/station2/listen.mp3"}` && set BOT_TOKEN="secret" && python bot.py</code>

---
# Usage
Let's see how to invite the bot to our server and what commands we can use.
## Invite Bot
Before you invite your bot, you will need to give it a special permission called Message Content Intent. You can find it in the Bot tab under the Privileged Gateway Intents section. Simply toggle on that setting and you'll be good to go.

The bot will need the following permissions: View Channels, Send Messages, Read Message History, Connect, and Speak. This equates to the integer `3214336` in Discord's numeric-based permission system. You can use the following pre-configured invite link to add your bot to your server:<br>
`https://discord.com/oauth2/authorize?client_id=yourBotsClientID&scope=bot&permissions=3214336`<br>
Replace the "yourBotsClientID" placeholder with your bot's Client ID, found on either the General Information or OAuth tabs. Below is an example URL assuming our Client ID was `12345`.<br>
`https://discord.com/oauth2/authorize?client_id=12345&scope=bot&permissions=3214336`

## Commands

**radio!join**<br>
Joins the voice channel that the requestor is in.

**radio!switch <name>** / **radio!station <name>** / **radio!play <name>**<br>
Switches the currently playing station.<br>
Example: `radio!switch Station 1`

**radio!leave**<br>
Leaves the current voice channel. This also resets settings like volume.

**radio!volume <1-100>**<br>
Sets the bot's internal volume on a scale from 1 to 100. This equates to 1-100% user volume.

**radio!defaultvolume <1-100>**<br>
Sets a default volume the bot will use when joining a channel.

**radio!volumeoffset <1-100>**<br>
The set volume will be multiplied by this number divided by 100 to create an offset. This is extremely useful since 100% volume with Discord's default 100% user volume is *really* loud. I've found that setting the volume offset to 10% provides a much more reasonable 100% volume.<br>
Example: If the current volume is 50% and you use `radio!volumeoffset 50`, this will set the volume to the current volume * 0.5, resulting in a perceived 25% volume.

**radio!pause** / **radio!unpause**<br>
**radio!mute** / **radio!unmute**<br>
Pauses and unpauses the radio stream.
