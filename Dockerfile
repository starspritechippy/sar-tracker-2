FROM python:3.11.0-alpine

RUN apk add tesseract-ocr

RUN mkdir /bot/
WORKDIR /bot/

COPY main.py /bot/
COPY image.py /bot/
COPY helpers.py /bot/
COPY regex.py /bot/
COPY constants.py /bot/
COPY .env /bot/
COPY cogs/ /bot/cogs/
COPY classes/ /bot/classes/
COPY requirements.txt /bot/

RUN pip install -r requirements.txt

CMD [ "python", "bot.py" ]