#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


import time

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

from helpers.tools import clean_up
from helpers.progress import progress_func

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def upload_audio(client, message, file_loc):

    msg = await message.edit_text(
        text="**جارٍ تحميل البث المستخرج...**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Progress", callback_data="progress_msg")]])
    )

    title = None
    artist = None
    thumb = None
    duration = 0

    metadata = extractMetadata(createParser(file_loc))
    if metadata and metadata.has("title"):
        title = metadata.get("title")
    if metadata and metadata.has("artist"):
        artist = metadata.get("artist")
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds

    c_time = time.time()    

    try:
        await client.send_audio(
            chat_id=message.chat.id,
            audio=file_loc,
            thumb=thumb,
            caption="**@H_M_Dr**",
            title=title,
            performer=artist,
            duration=duration,
            progress=progress_func,
            progress_args=(
                "**جارٍ تحميل البث المستخرج...**",
                msg,
                c_time
            )
        )
    except Exception as e:
        print(e)     
        await msg.edit_text("**حدث بعض الخطأ. راجع المطور لمزيد من المعلومات.**")   
        return

    await msg.delete()
    await clean_up(file_loc)    


async def upload_subtitle(client, message, file_loc):

    msg = await message.edit_text(
        text="**جارٍ تحميل العنوان الفرعي المستخرج...**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Progress", callback_data="progress_msg")]])
    )

    c_time = time.time() 

    try:
        await client.send_document(
            chat_id=message.chat.id,
            document=file_loc,
            caption="**@H_M_Dr**",
            progress=progress_func,
            progress_args=(
                "**جارٍ تحميل العنوان الفرعي المستخرج...**",
                msg,
                c_time
            )
        )
    except Exception as e:
        print(e)     
        await msg.edit_text("**حدث بعض الخطأ. راجع المطور لمزيد من المعلومات.**")   
        return

    await msg.delete()
    await clean_up(file_loc)        
