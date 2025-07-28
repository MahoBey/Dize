# Generate Session In Your Telegram premium @Opleech
# Copyright (c) 2023 WOODcraft
import os
import re
import shlex
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import OWNER_ID
from SessionGenerator import Opleech


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@Opleech.on_edited_message(
    filters.command("eval")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
@Opleech.on_message(
    filters.command("eval")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def executor(client: Opleech, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>What do you want to execute?</b>")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = "\n"
    if exc:
        evaluation += exc
    elif stderr:
        evaluation += stderr
    elif stdout:
        evaluation += stdout
    else:
        evaluation += "Success"
    final_output = f"<b>Result :</b>\n<pre language='python'>{evaluation}</pre>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {t2-t1} Seconds",
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"<b>Eval :</b>\n<code>{cmd[0:980]}</code>\n\n<b>Result :</b>\nAttached Document",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2-t1, 3)} Seconds",
                    ),
                    InlineKeyboardButton(
                        text="🗑",
                        callback_data=f"forceclose abc|{message.from_user.id}",
                    ),
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)


@Opleech.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@Opleech.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "Try again later after 2-3 minutes.", show_alert=True
            )
        except:
            return
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return


@Opleech.on_edited_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
@Opleech.on_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>Usage :</b>\n/sh git pull")
    text = message.text.split(None, 1)[1]
    
    try:
        # Use shlex for safe command splitting
        shell = shlex.split(text)
        process = subprocess.Popen(
            shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        try:
            # Add timeout to prevent hanging
            output, error = process.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
            output, error = process.communicate()
            output = b""
            error = b"Command timed out after 30 seconds."
        
        # Decode output safely
        output_str = output.decode("utf-8", errors="replace")
        error_str = error.decode("utf-8", errors="replace")
        
        if error_str:
            output_str = f"STDERR: {error_str}\n\nSTDOUT: {output_str}"
            
    except Exception as err:
        return await edit_or_reply(
            message, text=f"<b>ERROR :</b>\n<pre>{str(err)}</pre>"
        )
    
    if not output_str or output_str.strip() == "":
        output_str = "Command executed successfully with no output."
    
    if len(output_str) > 4096:
        with open("output.txt", "w+", encoding="utf-8") as file:
            file.write(output_str)
        await Opleech.send_document(
            message.chat.id,
            "output.txt",
            reply_to_message_id=message.id,
            caption="<code>Output</code>",
        )
        os.remove("output.txt")
    else:
        await edit_or_reply(message, text=f"<b>OUTPUT :</b>\n<pre>{output_str}</pre>")
