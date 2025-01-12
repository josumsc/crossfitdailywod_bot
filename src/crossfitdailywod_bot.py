import json
import os
import telebot
from datetime import datetime
from wodcrawler import WODCrawler

wod_crawler = WODCrawler()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_CONFIG_FILE = "./src/config.json"

with open(BOT_CONFIG_FILE, 'r') as f:
    BOT_CONFIG = json.load(f)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, BOT_CONFIG['welcome_message'])

@bot.message_handler(commands=['wod', 'workout'])
def send_wod(message):
    try:
        date_str = message.text.split()[1] if len(message.text.split()) > 1 else datetime.now().strftime('%y%m%d')
        wod = wod_crawler.download_crossfit_wods()
        if not wod:
            bot.reply_to(message, "No WODs found.")
            return
        elif not date_str in wod.keys():
            bot.reply_to(message, "No WOD found for this date, retrieving last WODs.")
            date_str = sorted(wod.keys())[-1]
        bot.reply_to(message, f"WOD for {date_str}: {wod.get(date_str)}")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['days'])
def send_days(message):
    if wod_crawler.wods:
        bot.reply_to(message, f"Available days: {', '.join(sorted(wod_crawler.wods.keys()))}")
    else:
        try:
            wod = wod_crawler.download_crossfit_wods()
            if not wod:
                bot.reply_to(message, "No WODs found.")
                return
            bot.reply_to(message, f"Available days: {', '.join(sorted(wod.keys()))}")
        except Exception as e:
            bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Available commands: " + ', '.join(BOT_CONFIG['commands']))
    bot.reply_to(message, "In the /wod command, you can add a date in the format YYMMDD.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Please use one of the available commands: " + ', '.join(BOT_CONFIG['commands']))

bot.infinity_polling()
