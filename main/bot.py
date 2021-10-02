import telegram # this is from python-telegram-bot package

from django.conf import settings
from django.template.loader import render_to_string

def post_published_quiz_on_telegram(quiz):
    message_html = render_to_string('published_quiz_message.html', {
        'quiz': quiz
    })
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
        text=message_html, parse_mode=telegram.ParseMode.HTML)


def post_rewards_sent_on_telegram(payment, quiz):
    message_html = render_to_string('payment_sent_out_message.html', {
        'payment': payment,
        'quiz': quiz
    })
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
        text=message_html, parse_mode=telegram.ParseMode.HTML)

def post_new_winner_on_telegram(winner):
    message_html = render_to_string('new_winner_message.html', {
        'winner': winner
    })
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
        text=message_html, parse_mode=telegram.ParseMode.HTML)