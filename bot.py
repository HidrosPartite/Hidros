import telebot
import os
from telebot import types

# Assicurati di fare export BOT_TOKEN='...' nella bash
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# L'URL deve essere IDENTICO a quello usato in BotFather
WEB_APP_URL = 'https://hidrospartite.github.io/Hidros/'

last_messages = {}

print("--- 🚀 BOT HIDROS ATTIVO ---")

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Pulsante principale della tastiera
    web_app_btn = types.KeyboardButton(text="🏐 APRI ARCHIVIO HIDROS", web_app=types.WebAppInfo(url=WEB_APP_URL))
    markup.add(web_app_btn)
    
    bot.send_message(
        message.chat.id, 
        "<b>Benvenuto!</b>\nUsa il tasto grigio in basso per sfogliare l'archivio.", 
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    chat_id = message.chat.id
    file_id = message.web_app_data.data 
    print(f"📥 Ricevuto ID: {file_id}")

    # Pulizia automatica per evitare confusione nell'app
    if chat_id in last_messages:
        try: bot.delete_message(chat_id, last_messages[chat_id])
        except: pass

    # Creazione del tasto di ritorno SOTTO il video
    markup = types.InlineKeyboardMarkup()
    # Usiamo lo stesso URL esatto
    markup.add(types.InlineKeyboardButton(
        text="Torna all'archivio 🗄️", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    ))

    try:
        sent = bot.send_video(
            chat_id, 
            file_id, 
            caption="Ecco il set richiesto! 🏐", 
            reply_markup=markup
        )
        last_messages[chat_id] = sent.message_id
    except Exception as e:
        print(f"❌ Errore: {e}")
        bot.send_message(chat_id, "⚠️ Errore nell'invio del video. Verifica l'ID nel file JS.")

if __name__ == "__main__":
    bot.infinity_polling()
