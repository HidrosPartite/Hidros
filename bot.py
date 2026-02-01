import telebot
import os
from telebot import types

# Recupera il Token dalla bash (export BOT_TOKEN=...)
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

WEB_APP_URL = 'https://hidrospartite.github.io/Hidros/'

# Dizionario per non intasare la chat di messaggi
last_messages = {}

print("--- 🚀 AVVIO BOT HIDROS ---")

try:
    me = bot.get_me()
    print(f"✅ Connesso come: {me.first_name}")
    print("📡 In attesa di messaggi...")
except Exception as e:
    print(f"❌ ERRORE: Token non trovato o non valido. Hai fatto 'export BOT_TOKEN=...'?")
    print(f"Dettaglio errore: {e}")

# 1. COMANDO START: Crea il pulsantone grigio (FONDAMENTALE)
@bot.message_handler(commands=['start'])
def handle_start(message):
    print(f"👤 Utente {message.chat.id} ha avviato il bot.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Questo tasto è l'UNICO che abilita l'invio dei video dall'app al bot
    web_app_btn = types.KeyboardButton(text="🏐 APRI ARCHIVIO HIDROS", web_app=types.WebAppInfo(url=WEB_APP_URL))
    markup.add(web_app_btn)
    
    bot.send_message(
        message.chat.id, 
        "<b>Benvenuto nell'Archivio Hidros!</b>\n\n"
        "Clicca il tasto grigio qui sotto per vedere i video.\n"
        "<i>Se apri l'app dal link blu, i video non funzioneranno.</i>", 
        parse_mode='HTML',
        reply_markup=markup
    )

# 2. GESTIONE VIDEO DALLA WEB APP
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    chat_id = message.chat.id
    file_id = message.web_app_data.data 
    print(f"📥 Ricevuto ID dall'app: {file_id}")

    # Pulizia messaggi precedenti
    if chat_id in last_messages:
        try: bot.delete_message(chat_id, last_messages[chat_id])
        except: pass

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Torna all'archivio 🗄️", web_app=types.WebAppInfo(url=WEB_APP_URL)))

    try:
        sent = bot.send_video(
            chat_id, 
            file_id, 
            caption="Ecco il contenuto richiesto! 🏐", 
            reply_markup=markup
        )
        last_messages[chat_id] = sent.message_id
        print("✅ Video inviato correttamente.")
    except Exception as e:
        print(f"❌ Errore invio video: {e}")
        bot.send_message(chat_id, f"⚠️ Non riesco a inviare questo video.\nID: <code>{file_id}</code>\n\nVerifica che sia un FILE_ID valido.", parse_mode='HTML')

# 3. TEST MANUALE (Per capire se il bot ti sente)
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    print(f"💬 Messaggio ricevuto: {message.text}")
    bot.reply_to(message, "Ti sento! Per i video usa il tasto 'APRI ARCHIVIO HIDROS' in basso.")

if __name__ == "__main__":
    bot.infinity_polling()
