
from telebot import TeleBot

# Config
TOKEN = '5882702531:AAHwszdpImeYiKXP4jDx2vbhPfeHys6XxSk'
LOG_GROUP_ID = -1002290955861  # Replace with your admin group chat ID

# Restricted keywords
RESTRICTED_KEYWORDS = ['@', 't.me', 'http://', 'https://', '/*','.com', '.ir']

# Initialize the bot
app = TeleBot(TOKEN)

def log_message(message):
    """Send log messages to the log group."""
    try:
        app.send_message(LOG_GROUP_ID, message)
    except Exception as e:
        print(f"Error sending log: {e}")

def is_admin(chat_id, user_id):
    """Check if a user is an admin in the group."""
    try:
        chat_member = app.get_chat_member(chat_id, user_id)
        return chat_member.status in ['administrator', 'creator']
    except Exception as e:
        log_message(f"Error in is_admin: {e}")
        return False

# Check messages for restricted content
@app.message_handler(func=lambda message: message.text is not None)
def check_message(message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name or "User"
        chat_id = message.chat.id

        # Skip if the user is an admin
        if is_admin(chat_id, user_id):
            return

        # Check for restricted content in text
        if any(keyword in message.text for keyword in RESTRICTED_KEYWORDS):
            # Delete the message with the restricted content
            app.delete_message(chat_id, message.message_id)

            # Send a warning message
            warning_text = f"⚠️ {user_name}! ហាមផ្ញើរលីងចូលក្នុងក្រុម!!!"
            app.send_message(chat_id, warning_text)

            log_message(f"Restricted content detected from {user_name} (ID: {user_id}) in group {message.chat.title}.")
    except Exception as e:
        log_message(f"Error in check_message: {e}")

# Forward media to log group
@app.message_handler(content_types=['photo', 'video'])
def forward_videos_and_photos(message):
    try:
        # Forward the photo or video to the log group
        app.forward_message(LOG_GROUP_ID, message.chat.id, message.message_id)
        log_message(f"Media (Photo/Video) forwarded from {message.from_user.first_name or 'User'} (ID: {message.from_user.id}) in group {message.chat.title}.")
    except Exception as e:
        log_message(f"Error in forward_videos_and_photos: {e}")

# Handle edited messages
@app.edited_message_handler(func=lambda message: message.text is not None)
def edit_message(message):
    check_message(message)

# Keep the bot running
if __name__ == '__main__':
    while True:
        try:
            print("Bot is running...")
            app.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            log_message(f"Polling error: {e}")
