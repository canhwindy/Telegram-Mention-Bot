from telethon import TelegramClient, events
import config  # Import the config file

# Initialize the Telegram client
client = TelegramClient('bot', config.API_ID, config.API_HASH).start(bot_token=config.BOT_TOKEN)

# Function to mention all members in a group or channel
@client.on(events.NewMessage(pattern=r'(@all|/all)'))
async def mention_all(event):
    if event.is_group or event.is_channel:
        chat = await event.get_input_chat()
        group_id = event.chat_id
        sender = await event.get_sender()

        # Check if the group is in the unrestricted list
        if group_id in config.UNRESTRICTED_GROUPS:
            can_mention = True
        else:
            permissions = await client.get_permissions(chat, sender.id)
            can_mention = permissions.is_admin

        if can_mention:
            members = await client.get_participants(chat)
            mentions = []
            for member in members:
                if not member.bot and member.username:
                    # Use an emoji to hide the username, ensuring they receive the notification
                    mention = f"[🐳](@{member.username})"
                    mentions.append(mention)
                    # Send the message when a certain number of mentions is reached to avoid too long messages
                    if len(mentions) == 5:
                        mention_text = ' '.join(mentions)
                        await client.send_message(chat, mention_text, parse_mode='Markdown')
                        mentions = []
            if mentions:
                mention_text = ' '.join(mentions)
                await client.send_message(chat, mention_text, parse_mode='Markdown')
        else:
            await event.reply("Only admin can do this.")

# Function to handle rude messages by replying with a video
@client.on(events.NewMessage(pattern='bot ngu'))
async def handle_rude_message(event):
    if event.is_group or event.is_channel:
        video_file = config.RUDE_MESSAGE_VIDEO
        await event.reply(file=video_file)

# Function to handle specific keyword by replying with a different video
@client.on(events.NewMessage(pattern='cảnh'))
async def handle_specific_message(event):
    if event.is_group or event.is_channel:
        video_file = config.SPECIFIC_MESSAGE_VIDEO
        await event.reply(file=video_file)

# Start the client
client.start()
client.run_until_disconnected()