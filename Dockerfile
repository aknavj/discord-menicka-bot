FROM python:3
FROM gorialis/discord.py

RUN mkdir -p `pwd`
WORKDIR `pwd`

COPY . .

CMD [ "python3", "discord_bot.py" ]