import telebot
import openai
import time
from googletrans import Translator

bot = telebot.TeleBot("6282182565:AAFFt_rjHhh9gf1bwr8LQAR7DmH81tWf24A")
openai.api_key = "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"
model = "gpt-3.5-turbo"
stop_symbols = "###"
default_mes = [{"role": "system", "content": "You're a bot who paraphrases the text. You just take the text and send a "
                                             "new version of it, with no comments."}]
translator = Translator()
users = {}
this_time = time.time()


def _get_user(id):
    user = users.get(id, {'id': id, 'messages': [], 'last_prompt_time': 0})
    users[id] = user
    return user


def _process_rq(user_id, rq):
    user = _get_user(user_id)
    if time.time() - user['last_prompt_time'] > 600:
        user['last_prompt_time'] = 0
        user['messages'] = default_mes

    if rq and len(rq) > 0 and len(rq) < 3000:

        rq = translator.translate(rq, dest='en', src='ru').text

        print(f">>> ({user_id}) {rq}")
        message = {"role": "user", "content": rq}
        user['messages'].append(message)
        user['messages'] = user['messages'][-6:]
        print("Sending to OpenAI: " + user['messages'][-1]["content"])
        full_ans = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=user['messages']
        ).choices[0]
        eng_ans = full_ans.message["content"]
        if "->" in eng_ans:
            eng_ans = eng_ans.split("->")[0].strip()
        ans = translator.translate(eng_ans, dest='ru', src='en').text

        ans_to_dict = {"role": "assistant", "content": ans}

        # user['messages'].append(ans_to_dict)
        user['messages'] = default_mes

        user['messages'] = user['messages'][-6:]
        print(f"<<< ({user_id}) {ans}")
        user['last_prompt_time'] = time.time()
        return ans
    else:
        user['last_prompt_time'] = 0
        user['messages'] = []
        return "!!! Error! Please use simple short texts"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = _get_user(message.from_user.id)
    user['last_prompt_time'] = 0
    user['messages'] = []
    bot.reply_to(message, f"Started! (History cleared). Using model {model}")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.from_user.id
    rq = message.text
    if time.time() - this_time < 2:
        return 0
    if rq.lower() in ('пошёл нахуй', 'забудь', 'обама', 'пошел нахуй', 'иди нахуй', 'ебало завали', 'завали ебало'):
        user = _get_user(user_id)
        user['last_prompt_time'] = 0
        user['messages'] = []
        bot.send_message(message.chat.id, 'Я всё забыл, хозяин.')
    else:
        ans = _process_rq(user_id, rq)
        bot.send_message(message.chat.id, ans)


if __name__ == '__main__':
    bot.polling()
