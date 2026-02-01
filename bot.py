import telebot
import os
from telebot import types

# Il token viene preso dalla bash tramite export BOT_TOKEN='...'
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# URL della tua Web App
WEB_APP_URL = 'https://hidrospartite.github.io/Hidros/'

# Dizionario per ricordarsi l'ultimo messaggio inviato e poterlo cancellare
last_messages = {}

print("--- 🚀 BOT HIDROS ATTIVO (Con pulizia messaggi) ---")

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_btn = types.KeyboardButton(
        text="🏐 APRI ARCHIVIO HIDROS", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
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

    # --- SECONDA COSA (RIPRISTINATA): Pulizia automatica ---
    if chat_id in last_messages:
        try: 
            bot.delete_message(chat_id, last_messages[chat_id])
        except Exception as e:
            print(f"Non ho potuto cancellare il messaggio: {e}")

    try:
        # Invia il video SENZA il tasto inline (PRIMA COSA TOLTA come richiesto)
        sent = bot.send_video(
            chat_id, 
            file_id, 
            caption="Ecco il set richiesto! 🏐"
        )
        # Salva l'ID di questo messaggio per cancellarlo alla prossima richiesta
        last_messages[chat_id] = sent.message_id
        
    except Exception as e:
        print(f"❌ Errore nell'invio: {e}")
        bot.send_message(chat_id, "⚠️ Errore: non riesco a inviare il video.")

if __name__ == "__main__":
    bot.infinity_polling()
