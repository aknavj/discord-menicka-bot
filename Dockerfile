FROM python:3
FROM gorialis/discord.py

ENV DISCORD_TOKEN=MTAwMzc2MTY0NzI1MDMyOTgzMA.GLOMlR.CPUzGswFfz9HmId6mQXiC8WrXpmi3GkpBt89NU

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

# initialize pip
RUN pip install pipenv \ 
    && pipenv install --system --deploy --ignore-pipfile

CMD [ "python3", "app.py" ]