from telebot import TeleBot

# config
TOKEN = '5882702531:AAHwszdpImeYiKXP4jDx2vbhPfeHys6XxSk'
ADMINS = [
    '1215864830'
]

# setup
app = TeleBot(TOKEN)

def check_message(type, message):
    print("\n\n\n\n==============\n\n\n")
    print(type, message)

    # Allow admins to send any message
    if message.from_user.id in ADMINS:
        return

    # Check if the sender is a group admin
    chat_member = app.get_chat_member(message.chat.id, message.from_user.id)
    print("==================> User data:", chat_member)
    if chat_member.status in ['creator', 'administrator']:
        return
    if chat_member.status == 'left' and chat_member.user.username == 'GroupAnonymousBot':
        return

    # Check for restricted content and delete the message
    if any(keyword in message.text for keyword in ['@', 't.me', 'http://', 'https://', '.com', '.ir']):
        print("Found restricted content in message text")
        app.delete_message(message.chat.id, message.message_id)
        
        # Send a warning message after deleting the restricted message
        app.send_message(
            message.chat.id, 
            f"{message.from_user.first_name}⚠️ហាមផ្ញើរលីងចូលក្នុងក្រុម!"
        )

# Handle edited messages
@app.edited_message_handler(func=lambda message: True)
def edit_message(message):
    check_message("edit", message)

# Handle new messages
@app.message_handler(func=lambda message: True)
def new_message(message):
    check_message("new", message)

# Keep the bot running
if __name__ == '__main__':
    app.infinity_polling()
