# Media Handler Module for SessionGenerator Bot
# Copyright (c) 2023 WOODcraft
import os
import asyncio
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from SessionGenerator import Opleech
from SessionGenerator.utils import add_served_user


@Opleech.on_message(filters.photo & filters.private)
async def handle_photo(_, message: Message):
    """Handle incoming photos from all devices"""
    try:
        # Get photo info
        photo = message.photo[-1]  # Get the largest size
        file_id = photo.file_id
        file_size = photo.file_size
        width = photo.width
        height = photo.height
        
        # Create download directory if it doesn't exist
        download_dir = "downloads"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{message.from_user.id}_{timestamp}.jpg"
        filepath = os.path.join(download_dir, filename)
        
        # Download the photo
        await message.download(filepath)
        
        # Send confirmation
        await message.reply_text(
            f"✅ **Fotoğraf başarıyla alındı!**\n\n"
            f"📁 **Dosya Adı:** `{filename}`\n"
            f"📏 **Boyut:** {width}x{height}\n"
            f"💾 **Dosya Boyutu:** {file_size} bytes\n"
            f"📱 **Cihaz:** {message.from_user.first_name}\n"
            f"⏰ **Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            quote=True
        )
        
        # Add user to database
        await add_served_user(message.from_user.id)
        
    except Exception as e:
        await message.reply_text(
            f"❌ **Fotoğraf işlenirken hata oluştu:**\n`{str(e)}`",
            quote=True
        )


@Opleech.on_message(filters.video & filters.private)
async def handle_video(_, message: Message):
    """Handle incoming videos from all devices"""
    try:
        # Get video info
        video = message.video
        file_id = video.file_id
        file_size = video.file_size
        duration = video.duration
        width = video.width
        height = video.height
        
        # Create download directory if it doesn't exist
        download_dir = "downloads"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"video_{message.from_user.id}_{timestamp}.mp4"
        filepath = os.path.join(download_dir, filename)
        
        # Download the video
        await message.download(filepath)
        
        # Send confirmation
        await message.reply_text(
            f"✅ **Video başarıyla alındı!**\n\n"
            f"📁 **Dosya Adı:** `{filename}`\n"
            f"📏 **Boyut:** {width}x{height}\n"
            f"⏱ **Süre:** {duration} saniye\n"
            f"💾 **Dosya Boyutu:** {file_size} bytes\n"
            f"📱 **Cihaz:** {message.from_user.first_name}\n"
            f"⏰ **Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            quote=True
        )
        
        # Add user to database
        await add_served_user(message.from_user.id)
        
    except Exception as e:
        await message.reply_text(
            f"❌ **Video işlenirken hata oluştu:**\n`{str(e)}`",
            quote=True
        )


@Opleech.on_message(filters.command("media") & filters.private)
async def media_help(_, message: Message):
    """Show help for media handling"""
    help_text = """
📱 **Medya Alma Yardımı**

Bu bot aşağıdaki medya türlerini destekler:

📸 **Fotoğraflar:** 
• JPG, PNG, GIF formatları
• Tüm cihazlardan gönderilebilir
• Otomatik olarak indirilir ve kaydedilir

🎥 **Videolar:**
• MP4, AVI, MOV formatları
• Maksimum 50MB boyut
• Süre sınırı yok

📋 **Kullanım:**
• Fotoğraf gönder → Otomatik işlenir
• Video gönder → Otomatik işlenir
• `/media` → Bu yardım mesajını göster

⚠️ **Not:** 
• Sadece özel mesajlarda çalışır
• Dosyalar `downloads/` klasörüne kaydedilir
• Her dosya benzersiz isimle kaydedilir
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 Fotoğraf Gönder", switch_inline_query_current_chat="photo")],
        [InlineKeyboardButton("🎥 Video Gönder", switch_inline_query_current_chat="video")],
        [InlineKeyboardButton("❓ Yardım", callback_data="help")]
    ])
    
    await message.reply_text(help_text, reply_markup=keyboard)


@Opleech.on_message(filters.command("downloads") & filters.user(OWNER_ID))
async def list_downloads(_, message: Message):
    """List all downloaded files (owner only)"""
    try:
        download_dir = "downloads"
        if not os.path.exists(download_dir):
            await message.reply_text("📁 Henüz indirilmiş dosya bulunmuyor.")
            return
        
        files = os.listdir(download_dir)
        if not files:
            await message.reply_text("📁 Henüz indirilmiş dosya bulunmuyor.")
            return
        
        file_list = "📁 **İndirilen Dosyalar:**\n\n"
        for i, filename in enumerate(files[:20], 1):  # Show first 20 files
            filepath = os.path.join(download_dir, filename)
            file_size = os.path.getsize(filepath)
            file_list += f"{i}. `{filename}` ({file_size} bytes)\n"
        
        if len(files) > 20:
            file_list += f"\n... ve {len(files) - 20} dosya daha"
        
        await message.reply_text(file_list)
        
    except Exception as e:
        await message.reply_text(f"❌ **Hata:** `{str(e)}`")