import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Abilita i log per vedere gli errori nella bash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8134996939:AAEIXfskFlPh1L9arz8Vt2vFN8y1NWUZyjw"
URL_WEBAPP = "https://hidrospartite.github.io/Hidros/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Invia il tasto per aprire l'archivio"""
    keyboard = [
        [InlineKeyboardButton(
            text="Apri Archivio Hidros 🏐", 
            web_app=WebAppInfo(url=URL_WEBAPP)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Benvenuto nell'Archivio Hidros! Clicca il tasto sotto per vedere i match:", reply_markup=reply_markup)

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Questa funzione gestisce i dati inviati da tg.sendData()"""
    # Recuperiamo l'ID inviato dalla Web App (il currentMatchId o epId)
    video_id = update.effective_message.web_app_data.data
    chat_id = update.effective_chat.id
    
    print(f"DEBUG: Ricevuto ID video dalla Web App: {video_id}")

    # Logica per inviare il video corretto
    # Qui puoi fare un controllo: se l'ID contiene certi prefissi, mandi video diversi
    await context.bot.send_message(
        chat_id=chat_id, 
        text=f"🎬 Sto caricando il contenuto richiesto (ID: {video_id})...\nAttendere un istante."
    )
    
    # ESEMPIO: Se hai i file_id di Telegram o URL diretti:
    # await context.bot.send_video(chat_id=chat_id, video="URL_O_FILE_ID")

def main():
    """Avvia il bot"""
    application = Application.builder().token(TOKEN).build()

    # Comando /start
    application.add_handler(CommandHandler("start", start))

    # GESTORE CRUCIALE: Ascolta TUTTI i dati inviati dalla Web App
    # Questo risolve il problema del "Torna in archivio" che non manda video
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    print("Bot avviato con successo! Premi CTRL+C per fermarlo.")
    application.run_polling()

if __name__ == '__main__':
    main()
