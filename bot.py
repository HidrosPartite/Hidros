import telebot
import os
import time
from telebot import types

# Il token viene preso dalla bash tramite export BOT_TOKEN='...'
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# URL della tua Web App
WEB_APP_URL = 'https://hidrospartite.github.io/Hidros/'

# Dizionario per ricordarsi l'ultimo messaggio inviato
last_messages = {}

print("--- 🚀 BOT HIDROS ATTIVO ---")

# Impostazione del pulsante Menu (quello grigio a sinistra della tastiera)
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

# Handler per ottenere i FILE_ID dai video caricati
@bot.message_handler(content_types=['video', 'document'])
def get_file_id(message):
    file_id = None
    if message.video:
        file_id = message.video.file_id
    elif message.document:
        file_id = message.document.file_id
    
    if file_id:
        print(f"🎬 FILE ID TROVATO: {file_id}")
        bot.reply_to(message, f"Copiato!\n\nID: `{file_id}`", parse_mode='Markdown')

# Comando Start
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

# Ricezione dati dalla Web App
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    chat_id = message.chat.id
    file_id = message.web_app_data.data 
    
    print(f"📥 Ricevuto ID: {file_id}")

    # Gestione cancellazione ultimo messaggio per pulizia
    if chat_id in last_messages:
        try: 
            bot.delete_message(chat_id, last_messages[chat_id])
        except Exception as e:
            print(f"Non ho potuto cancellare il messaggio: {e}")

    # Invio del video con gestione errore Rate Limit o ID non valido
    try:
        sent = bot.send_video(
            chat_id, 
            file_id, 
            caption="Ecco il set richiesto! 🏐"
        )
        last_messages[chat_id] = sent.message_id
        
    except Exception as e:
        print(f"❌ Errore nell'invio: {e}")
        # Se l'errore è dovuto a troppe richieste, avvisiamo il terminale
        if "Too Many Requests" in str(e):
             print("⚠️ ATTENZIONE: Sei in Rate Limit. Fermo il bot per un momento.")
        bot.send_message(chat_id, "⚠️ Errore: non riesco a inviare il video. Riprova tra un momento.")

# --- MODIFICA QUI: Gestione Polling Anti-Crash e Rate Limit ---
if __name__ == "__main__":
    while True:
        try:
            print("--- 📡 Il Bot sta ascoltando... ---")
            bot.polling(none_stop=True, timeout=60, interval=0)
        except Exception as e:
            print(f"⚠️ Errore connessione: {e}")
            # Se cade la connessione o c'è un errore, aspetta 15 secondi invece di restartare a raffica
            time.sleep(15)
