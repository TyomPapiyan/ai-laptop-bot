import os
import concurrent.futures

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from agent import WebIntelligenceAgent

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

agent = WebIntelligenceAgent()

executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)


# 🧠 КНОПКИ
def get_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Restart", callback_data="restart"),
            InlineKeyboardButton("🛑 Stop", callback_data="end"),
        ]
    ])


# 🤖 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["active"] = True
    context.user_data["history"] = []

    await update.message.reply_text(
        "🤖 Web Intelligence Agent is ready.\n\n"
        "Send a query below 👇",
        reply_markup=get_keyboard()
    )


# 📌 HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Just send a message:\n"
        "• best laptop for programming under 1000\n\n"
        "Use buttons below 👇",
        reply_markup=get_keyboard()
    )


# 🔘 BUTTON HANDLER
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "end":
        context.user_data["active"] = False
        await query.edit_message_text(
            "🛑 Bot stopped.",
            reply_markup=get_keyboard()
        )

    elif data == "restart":
        context.user_data["active"] = True
        context.user_data["history"] = []

        await query.edit_message_text(
            "🔄 Restarted. Bot is active again.",
            reply_markup=get_keyboard()
        )


# 💬 CHAT HANDLER
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ❌ if disabled
    if not context.user_data.get("active", True):
        await update.message.reply_text(
            "⚠️ Bot is stopped. Press Restart button.",
            reply_markup=get_keyboard()
        )
        return

    query_text = update.message.text

    await update.message.reply_text("🔎 Searching...")

    try:
        print("\n========================")
        print("USER QUERY:", query_text)
        print("DEBUG: BEFORE AGENT")

        future = executor.submit(agent.run, query_text)
        result = future.result()

        print("DEBUG: AFTER AGENT")
        print("DEBUG RESULT:", result)
        print("========================\n")

        # 📦 FORMAT OUTPUT
        if isinstance(result, dict):

            if "ai_reasoning" in result:
                text = result["ai_reasoning"]

            elif "top_results" in result:
                top = result["top_results"]

                text = "🏆 Top results:\n\n"

                for i, item in enumerate(top[:5], 1):
                    text += f"{i}. {item.get('name')}\n"
                    text += f"   💰 {item.get('price')}\n"
                    text += f"   🧠 {item.get('ram')}\n\n"

            elif "error" in result:
                text = f"❌ {result['error']}"

            else:
                text = str(result)

        else:
            text = str(result)

        await update.message.reply_text(
            text[:4000],
            reply_markup=get_keyboard()
        )

    except Exception as e:
        print("BOT ERROR:", e)
        await update.message.reply_text(
            f"❌ Error:\n{e}",
            reply_markup=get_keyboard()
        )


# 🚀 APP
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

# 🔘 buttons
app.add_handler(CallbackQueryHandler(button_handler))

# 💬 messages
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("🤖 Telegram bot started...")

app.run_polling()