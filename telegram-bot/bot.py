#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
RustChain Telegram Bot (Enhanced)
Provides wallet balance, miner status, and persistence for users.
"""

import os
import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from core.api import RustChainAPI
from core.database import Database

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Initialize components
api = RustChainAPI(verify_ssl=False) # Node often uses self-signed certs
db = Database()

def _escape_md(text: str) -> str:
    return re.sub(r"([_*`\[])", r"\\\1", str(text))

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    saved_wallet = db.get_default_wallet(user_id)
    
    welcome_text = "👋 *RustChain Explorer Bot*\n\n"
    if saved_wallet:
        welcome_text += f"Welcome back! Your registered wallet is:\n`{_escape_md(saved_wallet)}`"
    else:
        welcome_text += "Use `/register <wallet_id>` to save your wallet for quick access."

    keyboard = [
        [InlineKeyboardButton("💰 Check Balance", callback_data="check_balance")],
        [InlineKeyboardButton("⛏️ Miner Status", callback_data="check_miner")],
        [InlineKeyboardButton("⏱️ Network Info", callback_data="epoch_info")],
        [InlineKeyboardButton("🩺 Node Health", callback_data="health_info")],
    ]
    
    await update.effective_message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.effective_message.reply_text("Usage: `/register <wallet_id>`", parse_mode="Markdown")
        return
    
    wallet_id = context.args[0].strip()
    db.set_default_wallet(update.effective_user.id, wallet_id)
    await update.effective_message.reply_text(
        f"✅ Wallet registered successfully:\n`{_escape_md(wallet_id)}`",
        parse_mode="Markdown"
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    wallet_id = context.args[0] if (hasattr(context, 'args') and context.args) else db.get_default_wallet(user_id)
    
    if not wallet_id:
        await update.effective_message.reply_text("Please provide a wallet ID or `/register` one first.")
        return

    msg = await update.effective_message.reply_text(f"🔍 Fetching balance for `{_escape_md(wallet_id)}`...")
    data = await api.get_balance(wallet_id)
    
    if "error" in data:
        await msg.edit_text(f"❌ Error: {data['error']}")
        return

    balance_val = data.get("balance", data.get("rtc_balance", "0"))
    text = f"💰 *Wallet:* `{_escape_md(wallet_id)}`\n*Balance:* `{_escape_md(balance_val)} RTC`"
    await msg.edit_text(text, parse_mode="Markdown")

async def miner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    miner_id = context.args[0] if (hasattr(context, 'args') and context.args) else db.get_default_wallet(user_id)
    
    if not miner_id:
        await update.effective_message.reply_text("Please provide a miner ID or `/register` one first.")
        return

    msg = await update.effective_message.reply_text(f"⛏️ Checking miner `{_escape_md(miner_id)}`...")
    
    miners = await api.get_miners()
    status = "🔴 Not Attesting"
    if isinstance(miners, list):
        active_ids = [m.get("miner_id") or m.get("wallet_id") for m in miners]
        if miner_id in active_ids:
            status = "🟢 Active"
            
    await msg.edit_text(
        f"⛏️ *Miner Status*\n*ID:* `{_escape_md(miner_id)}`\n*Status:* {status}",
        parse_mode="Markdown"
    )

async def epoch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = await api.get_epoch()
    if "error" in data:
        await update.effective_message.reply_text(f"❌ Error fetching epoch: {data['error']}")
        return
        
    text = (
        f"⏱️ *Network Stats*\n"
        f"• Epoch: `{data.get('epoch', 'N/A')}`\n"
        f"• Slot: `{data.get('slot', 'N/A')}`\n"
        f"• Active Miners: `{data.get('enrolled_miners', 'N/A')}`"
    )
    await update.effective_message.reply_text(text, parse_mode="Markdown")

async def health(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = await api.get_health()
    status = "🟢 Online" if data.get("status") in ("ok", True) else "🔴 Issues detected"
    await update.effective_message.reply_text(
        f"🩺 *Node Health*\nStatus: {status}\nVersion: `{data.get('version', 'unknown')}`",
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_balance":
        await balance(update, context)
    elif query.data == "check_miner":
        await miner(update, context)
    elif query.data == "epoch_info":
        await epoch(update, context)
    elif query.data == "health_info":
        await health(update, context)

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment")
        return

    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("miner", miner))
    app.add_handler(CommandHandler("epoch", epoch))
    app.add_handler(CommandHandler("health", health))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    logger.info("RustChain Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
