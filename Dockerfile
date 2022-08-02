FROM python:3
FROM gorialis/discord.py

ARG DISCORD_TOKEN
ENV DISCORD_TOKEN={DISCORD_TOKEN} \
    PIPENV_DOTENV_LOCATION=.env

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

# initialize pip
RUN pip install pipenv \ 
    && pipenv install --system --deploy --ignore-pipfile

CMD [ "python3", "app.py" ]