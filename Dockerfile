FROM python:3
FROM gorialis/discord.py

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

# initialize pip
RUN pip install pipenv \ 
    && pipenv install --system --deploy --ignore-pipfile

CMD [ "python3", "app.py" ]