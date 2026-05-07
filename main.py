import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TELEGRAM_BOT_TOKEN, ADMIN_USER_ID, CHANNEL_USERNAME
from database import init_db, get_affiliate_link, set_affiliate_link, get_user, save_user, update_user_status

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id, message.from_user.username)
    update_user_status(message.chat.id, "started")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("👉 Continuar", callback_data="step_channel"))
    bot.send_message(
        message.chat.id,
        "👋 Bem-vindo! Eu sou seu assistente de jogos 🎮\nAqui você encontra bônus, dicas e explicações sobre jogos como Lucky Tiger e slots.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "step_channel")
def step_channel(call):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("👉 Entrar no canal", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"))
    markup.add(InlineKeyboardButton("✅ Já entrei", callback_data="verify_channel"))
    bot.send_photo(
        call.message.chat.id,
        "https://i.ibb.co/cKMV0y9Y/CANAL-DO-TELEGRAM-Perfil.png",
        caption="📢 Para liberar o acesso completo, entre no canal.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "verify_channel")
def verify_channel(call):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, call.from_user.id)
        if member.status in['member', 'administrator', 'creator']:
            update_user_status(call.from_user.id, "verified")
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🎁 Se cadastrar com Bônus da 1win", callback_data="send_affiliate"))
            bot.send_photo(
                call.message.chat.id,
                "https://i.ibb.co/jkNjM8P9/SOFTWINBR-6.jpg",
                caption="🎉 Acesso liberado!",
                reply_markup=markup
            )
        else:
            bot.answer_callback_query(call.id, "Você precisa entrar no canal primeiro!", show_alert=True)
    except Exception:
        bot.answer_callback_query(call.id, "Erro. Certifique-se de que o bot é admin no canal.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "send_affiliate")
def send_affiliate_callback(call):
    send_play_message(call.message.chat.id)

@bot.message_handler(commands=['startplay'])
def startplay_command(message):
    user = get_user(message.chat.id)
    if user and user.get("status") == "verified":
        send_play_message(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Por favor, inicie pelo /start e entre no canal.")

def send_play_message(chat_id):
    link = get_affiliate_link()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("👉 Jogar agora", url=link))
    bot.send_message(
        chat_id,
        "🔥 Quer testar na prática?\n\nAcesse aqui e use o código SOFTWINBR",
        reply_markup=markup
    )

@bot.message_handler(commands=['setlink'])
def set_link(message):
    if message.from_user.id == ADMIN_USER_ID:
        try:
            new_link = message.text.split(" ", 1)[1]
            set_affiliate_link(new_link)
            bot.reply_to(message, f"Link alterado para: {new_link}")
        except IndexError:
            bot.reply_to(message, "Envie no formato: /setlink https://seu-novo-link.com")
    else:
        bot.reply_to(message, "Acesso negado.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user = get_user(message.chat.id)
    if user and user.get("status") == "verified":
        bot.send_message(message.chat.id, "Para jogar, use o comando /startplay ou clique nos botões das mensagens anteriores.")
    else:
        bot.send_message(message.chat.id, "Use /start e entre no canal para acessar os bônus.")

if __name__ == "__main__":
    bot.infinity_polling()