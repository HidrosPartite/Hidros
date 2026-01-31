import telebot
import os
from telebot import types

# Recupera il Token (Assicurati di aver fatto 'export BOT_TOKEN=...' nella console)
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

WEB_APP_URL = 'https://hidrospartite.github.io/Hidros/'

# Dizionario per la pulizia della chat (chat_id: message_id)
last_messages = {}

print(f"Bot connesso con successo: {bot.get_me().first_name}")

# --- 1. TEST DI RISPOSTA (Scrivi 'ciao' per vedere se è vivo) ---
@bot.message_handler(func=lambda message: message.text and message.text.lower() == 'ciao')
def test_messaggio(message):
    bot.reply_to(message, "👋 Ti sento forte e chiaro! Inviami un video ora per ricevere l'ID.")

# --- 2. RECUPERO FILE_ID (Gestisce sia Video che Documenti/File) ---
@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    file_id = None
    
    # Se Telegram lo invia come Video
    if message.video:
        file_id = message.video.file_id
    # Se lo invia come File (documento) controlliamo che sia un video
    elif message.document:
        mime = message.document.mime_type
        if mime and mime.startswith('video'):
            file_id = message.document.file_id

    if file_id:
        bot.reply_to(message, f"✅ FILE_ID RICEVUTO:\n\n`{file_id}`", parse_mode='Markdown')
    else:
        bot.reply_to(message, "❌ Questo file non sembra un video. Riprova con un altro file.")

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
        bot.send_message(chat_id, "Errore: L'ID del video salvato nel database non è valido.")

# --- 4. MESSAGGIO DI START ---
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Ciao! Benvenuto nell'Archivio Hidros. Apri l'app per scegliere un match.")

if __name__ == "__main__":
    print("Bot Hidros online con auto-pulizia...")
    bot.infinity_polling()
