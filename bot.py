import telebot
import os
from telebot import types

# Il token viene preso dalla bash tramite export BOT_TOKEN='...'
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# URL della tua Web App
WEB_APP_URL = 'https://hidrospartite.github.io/Hidros/'

# Dizionario per la pulizia automatica
last_messages = {}

print("--- 🚀 BOT HIDROS ATTIVO (Senza barra verde) ---")

# Configura il tasto "Menu" (quello fisso a sinistra vicino alla graffetta)
# Questo tasto NON genera la barra verde
bot.set_chat_menu_button(None, types.MenuButtonWebApp("Archivio 🏐", types.WebAppInfo(url=WEB_APP_URL)))

@bot.message_handler(commands=['start'])
def handle_start(message):
    # Usiamo un tasto Inline invece di quello grigio per evitare la barra verde
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text="🏐 APRI ARCHIVIO HIDROS", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    ))
    
    bot.send_message(
        message.chat.id, 
        "<b>Benvenuto!</b>\nUsa il tasto qui sotto o il pulsante 'Archivio' nel menu per sfogliare i video.", 
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    chat_id = message.chat.id
    file_id = message.web_app_data.data 
    
    print(f"📥 Ricevuto ID: {file_id}")

    # Pulizia automatica messaggio precedente
    if chat_id in last_messages:
        try: 
            bot.delete_message(chat_id, last_messages[chat_id])
        except Exception as e:
            print(f"Errore pulizia: {e}")

    try:
        # Invia il video pulito
        sent = bot.send_video(
            chat_id, 
            file_id, 
            caption="Ecco il set richiesto! 🏐"
        )
        last_messages[chat_id] = sent.message_id
        
    except Exception as e:
        print(f"❌ Errore nell'invio: {e}")
        bot.send_message(chat_id, "⚠️ Errore nell'invio del video.")

if __name__ == "__main__":
    bot.infinity_polling()
