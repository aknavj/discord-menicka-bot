## Menicka.cz Discord Lunchbot

![APP SCREENSHOT](/app_screenshot.png)

This is simple discord bot which takes feed from menicka.cz server using requests and lxml -> parses part of the html file which we are interested in and pasting the content to the Discord server via Bot.

> DO NOT FORGET TO REGISTER {$DISCORD_TOKEN} environment variable in your system or .env file

### Instalation on local station

- Install pip environment

    pip install pipenv
   
- Install needed requirements

    pip install -r requirements.txt
   
- Create .env file with discord token inside

    echo "DISCORD_TOKEN=<YOUR-SECRET-TOKEN-GOES-HERE>" > .env

- Run discord bot on your local machine

    python3 app.py

### Running inside Docker container

- Build docker image

    docker build -t discord-menicka-bot .

- Run docker image

    docker run -d discord-menicka-bot
