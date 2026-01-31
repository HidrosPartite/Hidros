import telebot
import os
from telebot import types

# Recupera il Token
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

WEB_APP_URL = 'https://hidrospartite.github.io/Hidros/'

# Dizionario per la pulizia della chat
last_messages = {}

print(f"Bot connesso con successo: {bot.get_me().first_name}")

# --- 1. TEST DI RISPOSTA ---
@bot.message_handler(func=lambda message: message.text and message.text.lower() == 'ciao')
def test_messaggio(message):
    bot.reply_to(message, "👋 Ti sento forte e chiaro! Inviami un video ora per ricevere l'ID.")

# --- 2. RECUPERO FILE_ID (Corretto per evitare errori 400) ---
@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    file_id = None
    
    if message.video:
        file_id = message.video.file_id
    elif message.document and message.document.mime_type and message.document.mime_type.startswith('video'):
        file_id = message.document.file_id

    if file_id:
        # Usiamo HTML <code> per evitare errori con i caratteri speciali dell'ID
        risposta = f"✅ <b>FILE_ID RICEVUTO:</b>\n\n<code>{file_id}</code>"
        bot.reply_to(message, risposta, parse_mode='HTML')
    else:
        bot.reply_to(message, "❌ Invia un file video per ottenere l'ID.")

# --- 3. GESTIONE INVIO VIDEO DALLA WEB APP ---
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    chat_id = message.chat.id
    file_id_ricevuto = message.web_app_data.data 

    if chat_id in last_messages:
        try:
            bot.delete_message(chat_id, last_messages[chat_id])
        except Exception:
            pass

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Torna all'archivio 🗄️", web_app=types.WebAppInfo(url=WEB_APP_URL))
    markup.add(btn)

    try:
        sent_message = bot.send_video(
            chat_id,
            file_id_ricevuto,
            caption="Ecco il contenuto richiesto! 🏐",
            reply_markup=markup
        )
        last_messages[chat_id] = sent_message.message_id
    except Exception:
        bot.send_message(chat_id, "⚠️ Errore: L'ID video nel database non è valido o il bot non ha accesso al file.")

# --- 4. MESSAGGIO DI START ---
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Ciao! Benvenuto nell'Archivio Hidros. Apri l'app per scegliere un match.")

if __name__ == "__main__":
    print("Bot Hidros online con auto-pulizia...")
    bot.infinity_polling()
