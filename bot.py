#!/usr/bin/env python3
"""
GUI Meme Tipping Bot - Telegram Bot for rewarding memes with GUI tokens
"""

import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
import asyncio

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
GUI_TOKEN_ADDRESS = "0x1234567890abcdef"  # GUI token contract address

# Database simulation (in production use proper database)
user_data = {}
meme_data = {}
leaderboard = {}

class GUIMemeBot:
    def __init__(self):
        self.user_balances = {}
        self.meme_scores = {}
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send welcome message when /start is issued."""
        welcome_text = """
🐕 Welcome to GUI Meme Tipping Bot! 🐕

Use this bot to reward quality memes with GUI tokens!

Commands:
/tip <amount> - Tip a meme with GUI tokens
/balance - Check your GUI balance
/leaderboard - View top meme creators
/help - Show all commands

Let's make memes great again! 🚀
        """
        await update.message.reply_text(welcome_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send help message."""
        help_text = """
🤖 GUI Meme Tipping Bot Commands:

📱 Basic Commands:
/start - Welcome message
/help - This help message
/balance - Check your GUI balance
/leaderboard - Top meme creators

💰 Tipping Commands:
/tip <amount> - Reply to a meme to tip GUI tokens
/tip 10 - Tip 10 GUI tokens to meme creator

🏆 Features:
- Instant GUI token transfers
- Automatic leaderboard tracking
- Daily meme contests
- Community engagement rewards

Example: Reply to any meme with "/tip 5" to send 5 GUI tokens!
        """
        await update.message.reply_text(help_text)
    
    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check user's GUI balance."""
        user_id = update.effective_user.id
        username = update.effective_user.username or update.effective_user.first_name
        
        # Simulate balance (in production, fetch from blockchain)
        balance = self.user_balances.get(user_id, 100)  # Default 100 GUI
        
        balance_text = f"""
💰 @{username}'s GUI Balance:
Available: {balance} GUI

💡 Tip memes to earn more GUI tokens!
        """
        await update.message.reply_text(balance_text)
    
    async def leaderboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show top meme creators."""
        # Simulate leaderboard data
        leaderboard_data = [
            {"user": "MemeMaster69", "score": 450, "tips": 89},
            {"user": "DogeLover", "score": 320, "tips": 67},
            {"user": "GUIWhale", "score": 280, "tips": 45},
            {"user": "MemeQueen", "score": 250, "tips": 52},
            {"user": "CryptoComedian", "score": 200, "tips": 38}
        ]
        
        leaderboard_text = "🏆 Top Meme Creators:\n\n"
        for i, entry in enumerate(leaderboard_data, 1):
            leaderboard_text += f"{i}. {entry['user']} - {entry['score']} GUI earned ({entry['tips']} tips)\n"
        
        await update.message.reply_text(leaderboard_text)
    
    async def tip_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle tipping memes with GUI tokens."""
        if not update.message.reply_to_message:
            await update.message.reply_text("❗ Please reply to a meme message to tip!")
            return
        
        try:
            amount = int(context.args[0]) if context.args else 0
            if amount <= 0:
                await update.message.reply_text("❗ Please enter a valid amount (e.g., /tip 5)")
                return
            
            tipper = update.effective_user
            receiver = update.message.reply_to_message.from_user
            
            # Simulate transaction (in production, use blockchain)
            transaction_text = f"""
✅ Tip Successful!

💰 {tipper.first_name} tipped {amount} GUI to {receiver.first_name}
🎉 Meme creator rewarded!

Transaction: 0xabc123...xyz789
        """
            
            # Create keyboard for sharing
            keyboard = [[InlineKeyboardButton("🔄 Share Tip", switch_inline_query="Check out this tipped meme!")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(transaction_text, reply_markup=reply_markup)
            
            # Update leaderboard
            receiver_id = receiver.id
            if receiver_id not in self.meme_scores:
                self.meme_scores[receiver_id] = 0
            self.meme_scores[receiver_id] += amount
            
        except (IndexError, ValueError):
            await update.message.reply_text("❗ Usage: /tip <amount>\nExample: /tip 5")
    
    async def handle_meme(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming memes (images)."""
        if update.message.photo:
            user = update.effective_user
            
            # Welcome message for meme sharing
            welcome_msg = f"""
🎭 Great meme, @{user.username or user.first_name}!

💡 Community can tip you GUI tokens:
Reply with "/tip <amount>" to reward this meme!

🏆 Current rewards: {self.meme_scores.get(user.id, 0)} GUI earned
            """
            
            await update.message.reply_text(welcome_msg)
    
    async def daily_contest(self, context: ContextTypes.DEFAULT_TYPE):
        """Send daily meme contest announcement."""
        contest_text = """
🎮 Daily Meme Contest Started!

🏆 Prize Pool: 100 GUI tokens
⏰ Ends in 24 hours
📱 Submit your best memes now!

Use /submit_meme to participate!
        """
        # In production, send to all registered groups
        pass

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    bot = GUIMemeBot()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("balance", bot.balance))
    application.add_handler(CommandHandler("leaderboard", bot.leaderboard))
    application.add_handler(CommandHandler("tip", bot.tip_command))
    application.add_handler(MessageHandler(filters.PHOTO, bot.handle_meme))
    
    # Start the Bot
    logger.info("Starting GUI Meme Tipping Bot...")
    application.run_polling()

if __name__ == '__main__':
    main()