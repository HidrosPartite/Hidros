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

# --- 1. TEST DI RISPOSTA (Funziona ovunque) ---
@bot.message_handler(func=lambda message: message.text and message.text.lower() == 'ciao')
def test_messaggio(message):
    bot.reply_to(message, "👋 Ti sento forte e chiaro! Se mi mandi un video (qui o nel gruppo) ti darò l'ID.")

# --- 2. RECUPERO FILE_ID (Ottimizzato per Gruppi e Privata) ---
@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    file_id = None
    
    # Se è un video normale
    if message.video:
        file_id = message.video.file_id
    # Se è un video inviato come file (documento)
    elif message.document and message.document.mime_type and message.document.mime_type.startswith('video'):
        file_id = message.document.file_id

    if file_id:
        # Messaggio formattato in HTML per evitare errori con caratteri speciali
        risposta = (
            f"✅ <b>FILE_ID GENERATO</b>\n"
            f"Provenienza: <i>{message.chat.title if message.chat.type != 'private' else 'Chat Privata'}</i>\n\n"
            f"<code>{file_id}</code>\n\n"
            f"Punta l'ID e copialo per il tuo file partite.js"
        )
        bot.reply_to(message, risposta, parse_mode='HTML')
    else:
        # Risponde con errore solo in chat privata per non disturbare nel gruppo
        if message.chat.type == 'private':
            bot.reply_to(message, "❌ Questo file non sembra un video. Riprova.")

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
        bot.send_message(chat_id, "⚠️ Errore: L'ID video nel database non è valido.")

# --- 4. MESSAGGIO DI START ---
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Ciao! Benvenuto nell'Archivio Hidros. Apri la Web App per iniziare.")

if __name__ == "__main__":
    print("Bot Hidros online (Pronto per Gruppi e Privata)...")
    bot.infinity_polling()
