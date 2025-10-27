# SessionGenerator Bot

A Telegram bot for generating string sessions with media handling capabilities.

## Features

- **String Session Generation**: Generate Pyrogram and Telethon string sessions
- **Media Handling**: Receive and process photos/videos from all devices
- **Multi-Device Support**: Works with all Telegram clients and devices
- **Secure**: Environment-based configuration

## Media Features

### Photo Support
- ✅ JPG, PNG, GIF formats
- ✅ All device types (Android, iOS, Desktop, Web)
- ✅ Automatic download and storage
- ✅ File size and dimension info

### Video Support  
- ✅ MP4, AVI, MOV formats
- ✅ Up to 50MB file size
- ✅ Duration and quality info
- ✅ Cross-platform compatibility

## Commands

- `/start` - Start the bot
- `/media` - Show media handling help
- `/downloads` - List downloaded files (owner only)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables in `.env`:
```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=your_user_id
MONGO_DB_URI=your_mongo_uri
```

3. Run the bot:
```bash
python main.py
```

## Media Usage

1. Send a photo or video to the bot in private chat
2. Bot will automatically download and process the media
3. You'll receive confirmation with file details
4. Files are saved in `downloads/` directory

## Security

- Environment-based configuration
- Owner-only commands
- Safe file handling
- Input validation
