import telebot
import openai
import os
import time



bot = telebot.TeleBot("6282182565:AAFFt_rjHhh9gf1bwr8LQAR7DmH81tWf24A")
openai.api_key = "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"
model = "gpt-3.5-turbo"
stop_symbols = "###"



# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "user", "content": "Hello!"}
#   ]
# )
# b = []
# a = {"role": "user", "content": 'rq'}
# print(completion.choices[0].message["content"])
# print(type(completion.choices[0].message["content"]))

b = 'AaAa'
b.lower()
print(b)
print(b.lower())