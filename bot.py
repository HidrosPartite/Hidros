import os
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Abilita i log per vedere cosa succede nella bash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# Legge il token dalla variabile d'ambiente impostata nella bash
TOKEN = os.getenv('BOT_TOKEN')
# Inserisci qui l'URL della tua GitHub Page
URL_WEBAPP = "https://hidrospartite.github.io/Hidros/" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Invia il messaggio di benvenuto con il tasto ufficiale"""
    keyboard = [
        [InlineKeyboardButton(
            text="🏐 APRI ARCHIVIO HIDROS", 
            web_app=WebAppInfo(url=URL_WEBAPP)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<b>Benvenuto nell'Archivio Hidros!</b>\n\n"
        "Clicca il tasto grigio qui sotto per vedere i video.\n"
        "<i>Se apri l'app da link esterni, l'invio video non funzionerà.</i>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def web_app_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestisce i dati inviati dalla Web App (tg.sendData)"""
    # Recupera l'ID del video inviato dal tuo JavaScript
    data = update.effective_message.web_app_data.data
    
    # Stampa nella bash per debug (grazie al flag -u lo vedi subito)
    print(f"✅ Video richiesto dall'app: {data}")
    
    # Invia la risposta all'utente
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"🎬 <b>Invio video in corso...</b>\nID richiesto: <code>{data}</code>",
        parse_mode='HTML'
    )
    
    # Qui potresti aggiungere la logica: if data == "partita1": send_video...

def main():
    """Avvia il bot"""
    if not TOKEN:
        print("❌ ERRORE: BOT_TOKEN non trovato nelle variabili d'ambiente!")
        return

    application = Application.builder().token(TOKEN).build()

    # Gestore per il comando /start
    application.add_handler(CommandHandler("start", start))

    # GESTORE CRUCIALE: Riceve i dati dalla Web App
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data_handler))

    print("🚀 Bot avviato correttamente! Premi CTRL+C per fermarlo.")
    application.run_polling()

if __name__ == '__main__':
    main()
