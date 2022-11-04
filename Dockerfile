FROM python:3
ADD bot.py bot.py
RUN pip install -U --pre aiogram
CMD python3 bot.py