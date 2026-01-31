import telebot
from telebot import types

# Incolla il tuo token tra le virgolette
API_TOKEN = 'IL_TUO_TOKEN_QUI'
bot = telebot.TeleBot(API_TOKEN)

# URL della tua Web App (GitHub Pages o altro)
WEB_APP_URL = 'https://tuosito.com'

# Dizionario per la pulizia della chat (chat_id: message_id)
last_messages = {}

# 1. RECUPERO FILE_ID (Trascina un video qui per avere il codice)
@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    bot.reply_to(message, f"✅ FILE_ID RICEVUTO:\n\n`{file_id}`", parse_mode='Markdown')

# 2. GESTIONE INVIO VIDEO DALLA WEB APP + CANCELLAZIONE VECCHIO
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    chat_id = message.chat.id
    file_id_ricevuto = message.web_app_data.data # Riceve l'ID dal tuo JS
    
    # Cancella l'ultimo video inviato per tenere pulito
    if chat_id in last_messages:
        try:
            bot.delete_message(chat_id, last_messages[chat_id])
        except Exception:
            pass

    # Crea il tasto "Torna all'archivio"
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Torna all'archivio 🗄️", web_app=types.WebAppInfo(url=WEB_APP_URL))
    markup.add(btn)
    
    try:
        # Invia il video in formato MP4 con anteprima
        sent_message = bot.send_video(
            chat_id, 
            file_id_ricevuto, 
            caption="Ecco il contenuto richiesto! 🏐",
            reply_markup=markup
        )
        # Salva l'ID per cancellarlo alla prossima richiesta
        last_messages[chat_id] = sent_message.message_id
    except Exception as e:
        bot.send_message(chat_id, "Errore: ID video non valido nel file JS.")

# 3. MESSAGGIO DI START PULITO
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Ciao! Benvenuto nell'Archivio Hidros. Apri l'app per scegliere un match.")

if __name__ == "__main__":
    print("Bot Hidros online con auto-pulizia...")
    bot.infinity_polling()
