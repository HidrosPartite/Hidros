import telebot
import os

# Prende il token dalle impostazioni di Render
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    if "match_" in message.text:
        match_id = message.text.split("match_")[1]
        
        if match_id == "1":
            bot.send_message(message.chat.id, "🎬 **Match: Hidros vs Vero Volley**\nPreparo il video...")
        elif match_id == "2":
            bot.send_message(message.chat.id, "🎬 **Match: Hidros vs Lube**\nPreparo il video...")
        else:
            bot.send_message(message.chat.id, "Partita non trovata.")
    else:
        bot.send_message(message.chat.id, "Ciao! Apri l'app per scegliere un match.")

if __name__ == "__main__":
    print("Bot avviato correttamente...")
    bot.infinity_polling()
