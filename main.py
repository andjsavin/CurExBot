import exchange
import telebot
import re
import os

bot = telebot.TeleBot('1971315426:AAGwuOk8oHGijc3VIllXgLizbwuHqDAF4Zs')
#replies Hello! to /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Hello! Use /help to learn about available commands')

#shows list of available commands
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
                     '''/list CUR(optional) or /lst CUR(optional) - shows list of all available rates with .00 precision, base currency is USD
/exchange X CUR1 to CUR2 - converts X amount of CUR1 to CUR2 with .00 precision
/history CUR1/CUR2 for X days - shows an image graph of the selected currency for the last X days''')

#shows list of currencies in comparison to base currency, default currency - USD
@bot.message_handler(regexp=r'(list( [A-Z]{3})*)|(lst( [A-Z]{3})*)')
def list_command(message):
    if re.match(r'[A-Z]{3}', message.text[-3:]):
        base = message.text[-3:]
        currencies = exchange.currency_list(base)
    else:
        base = 'USD'
        currencies = exchange.currency_list()
    bot.send_message(message.chat.id, currencies)

#converts X amount of CUR1 to CUR2 with .00 precision
@bot.message_handler(regexp=r'exchange [1-9]{1}[0-9]{0,15} [A-Z]{3} to [A-Z]{3}')
def exchange_command(message):
    rate = exchange.exchange_cur(message.text[-10:-7], message.text[-3:], int(re.sub('[^0-9]', '', message.text)))
    bot.send_message(message.chat.id, rate)

#shows history graph of CUR1/CUR2 for the last X days
@bot.message_handler(regexp=r'history [A-Z]{3}/[A-Z]{3} for [1-9]{1}[0-9]{0,1} days')
def history_command(message):
    base = message.text[9:12]
    comp = message.text[13:16]
    days = int(re.sub('[^0-9]', '', message.text))
    bot.send_message(message.chat.id, exchange.history_chart(base, comp, days))
    bot.send_photo(message.chat.id, photo=open('images/' + base + comp + str(days) + '.png', 'rb'))
    os.remove('images/' + base + comp + str(days) + '.png')

bot.polling()

