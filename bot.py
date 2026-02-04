import telebot
import os
import time
from telebot import types
from flask import Flask
from threading import Thread

# --- CONFIGURAZIONE ANTI-SLEEP PER RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Il bot Hidros è attivo e funzionante!"

def run():
    # Render assegna automaticamente una porta, di solito la 10000 o 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True # Il thread si chiude se il programma principale si ferma
    t.start()
# --------------------------------------------

# Il token viene preso dall'ambiente (Environment Variables su Render)
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# URL della tua Web App
WEB_APP_URL = 'https://hidrospartite.github.io/Hidros/'

# Dizionario per ricordarsi l'ultimo messaggio inviato
last_messages = {}

print("--- 🚀 BOT HIDROS ATTIVO ---")

# Impostazione del pulsante Menu
try:
    bot.set_chat_menu_button(
        None, 
        types.MenuButtonWebApp(
            type="web_app", 
            text="Archivio 🏐", 
            web_app=types.WebAppInfo(url=WEB_APP_URL)
        )
    )
except Exception as e:
    print(f"Errore impostazione MenuButton: {e}")

# Gestione File ID
@bot.message_handler(content_types=['video', 'document'])
def get_file_id(message):
    file_id = None
    if message.video:
        file_id = message.video.file_id
    elif message.document:
        file_id = message.document.file_id
    
    if file_id:
        print(f"🎬 FILE ID TROVATO: {file_id}")
        bot.send_message(message.chat.id, f"Copiato!\n\nID: `{file_id}`", parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, 
        one_time_keyboard=False,
        input_field_placeholder="Clicca il tasto qui sotto ↓"
    )
    web_app_btn = types.KeyboardButton(
        text="🏐 APRI ARCHIVIO HIDROS", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    markup.add(web_app_btn)
    
    bot.send_message(
        message.chat.id, 
        "<b>Benvenuto!</b>\nUsa il tasto grigio in basso o il tasto blu 'Archivio' per sfogliare.", 
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    chat_id = message.chat.id
    file_id = message.web_app_data.data 
    
    print(f"📥 Ricevuto ID dalla WebApp: {file_id}")

    if chat_id in last_messages:
        try: 
            bot.delete_message(chat_id, last_messages[chat_id])
        except Exception as e:
            print(f"Non ho potuto cancellare il messaggio precedente: {e}")

    try:
        sent = bot.send_video(
            chat_id, 
            file_id, 
            caption="Ecco il set richiesto! 🏐"
        )
        last_messages[chat_id] = sent.message_id
        
    except Exception as e:
        print(f"❌ Errore nell'invio video: {e}")
        bot.send_message(chat_id, "⚠️ Errore: non riesco a inviare il video. Verifica che l'ID sia corretto.")

# Avvio del bot e del server web
if __name__ == "__main__":
    # Avvia il server web per l'anti-sleep
    print("--- 🌐 Avvio server web di controllo ---")
    keep_alive()
    
    # Loop del bot
    while True:
        try:
            print("--- 📡 Il Bot è in ascolto... ---")
            bot.polling(none_stop=True, timeout=60, interval=0)
        except Exception as e:
            print(f"⚠️ Connessione persa, riprovo tra 15 secondi... Errore: {e}")
            time.sleep(15)
