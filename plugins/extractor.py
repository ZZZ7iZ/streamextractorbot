#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


from pyrogram import filters
from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from script import Script


@trojanz.on_message(filters.private & (filters.document | filters.video))
async def confirm_dwnld(client, message):

    if message.from_user.id not in Config.AUTH_USERS:
        return

    media = message
    filetype = media.document or media.video

    if filetype.mime_type.startswith("video/"):
        await message.reply_text(
            "**ماذا تريد مني ان افعل??**",
            quote=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="تحميل ومعالجة", callback_data="download_file")],
                [InlineKeyboardButton(text="الغاء", callback_data="close")]
            ])
        )
    else:
        await message.reply_text(
            "الوسائط غير صالحة",
            quote=True
        )
