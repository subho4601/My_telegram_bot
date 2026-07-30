import os logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# ===================== CONFIGURATION =====================
BOT_TOKEN = os.environ.get("BOT_TOKEN")


ADMIN_ID = 5603706623

# आपका असली VIP ग्रुप लिंक
VIP_LINK = "https://t.me/teli35y8"               

# आपका PhonePe QR Code Link (सेट कर दिया गया है)
QR_IMAGE_URL = "https://i.ibb.co/3s3Xz9J/2098.png"   

ADMIN_USERNAME = "YourAdminUsername"             # यहाँ अपना टेलीग्राम यूज़रनेम (बिना @ के) डालें
UPI_ID = "SUMITA DAS"                            # QR कोड के अनुसार नाम/UPI

WAITING_SCREENSHOT = 1

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ===================== USER FLOW HANDLERS =====================

# 1. Start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 1 Day VIP Plan - ₹100 🔥", callback_data='plan_1')],
        [InlineKeyboardButton("⚡ 2 Days VIP Plan - ₹180 ⚡", callback_data='plan_2')],
        [InlineKeyboardButton("👑 7 Days VIP Plan - ₹500 👑", callback_data='plan_7')]
    ]
    
    welcome_msg = (
        "✨ <b>────────────────────</b> ✨\n"
        "🎉 <b>WELCOME TO VIP PREMIUM BOT</b> 🎉\n"
        "✨ <b>────────────────────</b> ✨\n\n"
        "💎 <b>कृपया नीचे दिए गए बटन में से अपना प्लान चुनें:</b> 💎"
    )
    
    await update.message.reply_text(
        welcome_msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
    return ConversationHandler.END

# 2. Plan Selection Handler
async def plan_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan_info = query.data.split("_")[1]
    days = "1" if plan_info == "1" else ("2" if plan_info == "2" else "7")
    price = "100" if plan_info == "1" else ("180" if plan_info == "2" else "500")

    caption_text = (
        f"💳 <b>─── PAYMENT DETAILS ───</b> 💳\n\n"
        f"⭐ <b>Selected Plan:</b> 🌟 {days} Day(s) VIP 🌟\n"
        f"💰 <b>Total Amount:</b> 💎 ₹{price} 💎\n"
        f"📲 <b>Name:</b> <code>{UPI_ID}</code>\n\n"
        f"📋 <b>ज़रूरी निर्देश (Instructions):</b>\n"
        f"🔹 1️⃣ ऊपर दिए गए QR कोड पर <b>₹{price}</b> का भुगतान करें। 💸\n"
        f"🔹 2️⃣ भुगतान के बाद <b>स्क्रीनशॉट (Photo)</b> सीधे इस चैट में भेजें। 📸\n\n"
        f"⚠️ <i>नोट: प्लान और टाइमलाइन की पुष्टि एडमिन द्वारा फ़ोन/चैट पर बातचीत के बाद की जाएगी।</i> 📞"
    )

    try:
        await query.message.reply_photo(
            photo=QR_IMAGE_URL,
            caption=caption_text,
            parse_mode='HTML'
        )
    except Exception:
        await query.message.reply_text(caption_text, parse_mode='HTML')

    return WAITING_SCREENSHOT

# 3. Receive Screenshot Handler
async def receive_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo_file_id = update.message.photo[-1].file_id

    user_confirm_msg = (
        "⏳ <b>─── SCREENSHOT RECEIVED ───</b> ⏳\n\n"
        "✅ <b>आपका पेमेंट स्क्रीनशॉट प्राप्त हो गया है!</b>\n"
        "🔍 एडमिन वेरिफिकेशन के बाद आपसे संपर्क करेंगे और एक्सेस प्रदान करेंगे।\n\n"
        "🤝 कृपया थोड़ा इंतज़ार करें..."
    )
    
    await update.message.reply_text(user_confirm_msg, parse_mode='HTML')

    admin_keyboard = [
        [
            InlineKeyboardButton("✅ Accept & Send Link", callback_data=f"accept_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ]

    admin_msg = (
        f"📥 <b>─── NEW PAYMENT RECEIVED ───</b> 📥\n\n"
        f"👤 <b>Name:</b> {user.full_name}\n"
        f"🔗 <b>Username:</b> @{user.username if user.username else 'None'}\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>\n\n"
        f"👇 <b>नीचे दिए गए बटन से एक्शन लें:</b>"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_file_id,
        caption=admin_msg,
        reply_markup=InlineKeyboardMarkup(admin_keyboard),
        parse_mode='HTML'
    )

    return ConversationHandler.END

# 4. Admin Accept / Reject Actions
async def admin_action_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    action = data[0]
    target_user_id = int(data[1])

    if action == "accept":
        await query.edit_message_caption(
            caption=query.message.caption + "\n\n✅ <b>ACCEPTED & LINK SENT</b> 🚀",
            parse_mode='HTML'
        )

        user_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Join VIP Group Now 🚀", url=VIP_LINK)],
            [InlineKeyboardButton("💬 Chat with Admin 💬", url=f"https://t.me/{ADMIN_USERNAME}")]
        ])
        
        accept_user_msg = (
            "🎉 <b>─── PAYMENT ACCEPTED ───</b> 🎉\n\n"
            "✅ <b>आपका पेमेंट स्वीकार कर लिया गया है!</b>\n"
            "👇 नीचे दिए गए बटन पर क्लिक करके तुरंत VIP ग्रुप जॉइन करें।\n"
            "ग्रुप में आने के बाद एडमिन आपसे बात करके आगे की प्रक्रिया पूरी करेंगे।"
        )

        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=accept_user_msg,
                reply_markup=user_buttons,
                parse_mode='HTML'
            )
        except Exception:
            await query.message.reply_text("⚠️ यूजर को मैसेज नहीं भेजा जा सका।")

    elif action == "reject":
        await query.edit_message_caption(
            caption=query.message.caption + "\n\n❌ <b>REJECTED</b>",
            parse_mode='HTML'
        )

        support_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Contact Admin 💬", url=f"https://t.me/{ADMIN_USERNAME}")]
        ])

        reject_user_msg = (
            "❌ <b>─── PAYMENT REJECTED ───</b> ❌\n\n"
            "आपका पेमेंट वेरीफाई नहीं हो सका।\n"
            "कृपया सही स्क्रीनशॉट दोबारा भेजें या नीचे दिए बटन पर क्लिक करके एडमिन से संपर्क करें।"
        )

        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=reject_user_msg,
                reply_markup=support_button,
                parse_mode='HTML'
            )
        except Exception:
            pass

# ===================== MAIN APPLICATION =====================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(plan_selected, pattern='^plan_')
        ],
        states={
            WAITING_SCREENSHOT: [MessageHandler(filters.PHOTO, receive_screenshot)]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(admin_action_callback, pattern='^(accept|reject)_'))

    print("Bot is running smoothly...")
    app.run_polling()

if __name__ == '__main__':
    main()
