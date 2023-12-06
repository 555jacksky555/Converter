import telebot
from Config import TOKEN, keys
from Exceptions import APIException, Crypta

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = 'Please enter: ' \
            '\n- <Currency you have> \n- <Currency you need>' \
            '\n- <You currency amount> \n- <Ex: USD EUR 10.50>\n List of available currencies: /currencies'
    bot.reply_to(message, text)


@bot.message_handler(commands=['currencies'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):

    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('The message should have format: USD EUR 21.56')

        base, quote, amount = values
        total_base = Crypta.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'You have entered incorrect values \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Service is not available right now - try again later \n{e}')
    else:
        text = f'{amount} {base.upper()} = {total_base} {quote.upper()}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
