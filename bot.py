import telebot
import os
from telebot import types

API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

WEB_APP_URL = 'https://hidrospartite.github.io/Hidros/'
last_messages = {}

print("--- 🚀 BOT HIDROS ATTIVO (Senza barra verde) ---")

# CORREZIONE: Aggiunto web_app= per risolvere il TypeError dello screenshot
bot.set_chat_menu_button(None, types.MenuButtonWebApp(
    text="Archivio 🏐", 
    web_app=types.WebAppInfo(url=WEB_APP_URL)
))

@bot.message_handler(commands=['start'])
def handle_start(message):
    # Usiamo un tasto Inline (sotto il messaggio) invece del tastone grigio
    # Questo è l'UNICO modo per non far apparire la barra verde cerchiata
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text="🏐 APRI ARCHIVIO HIDROS", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    ))
    
    bot.send_message(
        message.chat.id, 
        "<b>Benvenuto!</b>\nClicca il tasto qui sotto per sfogliare l'archivio senza notifiche di sistema.", 
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    chat_id = message.chat.id
    file_id = message.web_app_data.data 
    
    # Pulizia messaggio precedente
    if chat_id in last_messages:
        try: bot.delete_message(chat_id, last_messages[chat_id])
        except: pass

    try:
        sent = bot.send_video(
            chat_id, 
            file_id, 
            caption="Ecco il set richiesto! 🏐"
        )
        last_messages[chat_id] = sent.message_id
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    bot.infinity_polling()
