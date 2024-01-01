#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


from pyrogram import filters
from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from script import Script

from helpers.progress import PRGRS
from helpers.tools import clean_up
from helpers.download import download_file, DATA
from helpers.ffmpeg import extract_audio, extract_subtitle


@trojanz.on_callback_query()
async def cb_handler(client, query):

    if query.data == "start_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("‹ المساعدة ›", callback_data="help_data"),
                InlineKeyboardButton("‹ عن البوت ›", callback_data="about_data")],
            [InlineKeyboardButton("‹ السورس ›", url="https://t.me/H_M_Dr")]
        ])

        await query.message.edit_text(
            Script.START_MSG.format(query.from_user.mention),
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return


    elif query.data == "help_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("‹ خلف ›", callback_data="start_data"),
                InlineKeyboardButton("‹ عن البوت ›", callback_data="about_data")],
            [InlineKeyboardButton("‹ السورس ›", url="https://t.me/H_M_Dr")]
        ])

        await query.message.edit_text(
            Script.HELP_MSG,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return


    elif query.data == "about_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("‹ خلف ›", callback_data="help_data"),
                InlineKeyboardButton("‹ بدء البوت ›", callback_data="start_data")],
            [InlineKeyboardButton("‹ السورس ›", url="https://t.me/H_M_Dr")]
        ])

        await query.message.edit_text(
            Script.ABOUT_MSG,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return


    elif query.data == "download_file":
        await query.answer()
        await query.message.delete()
        await download_file(client, query.message)


    elif query.data == "progress_msg":
        try:
            msg = "تفاصيل التقدم...\n\nمكتمل : {current}\nالحجم الإجمالي : {total}\nسرعة : {speed}\nتقدم : {progress:.2f}%\n و : {eta}"
            await query.answer(
                msg.format(
                    **PRGRS[f"{query.message.chat.id}_{query.message.message_id}"]
                ),
                show_alert=True
            )
        except:
            await query.answer(
                "جارٍ معالجة ملفك...",
                show_alert=True
            )


    elif query.data == "الغاء": 
        await query.message.delete()  
        await query.answer(
                "ألغيت...",
                show_alert=True
            ) 


    elif query.data.startswith('صوتي'):
        await query.answer()
        try:
            stream_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]
            await extract_audio(client, query.message, data)
        except:
            await query.message.edit_text("**التفاصيل غير موجودة**")   


    elif query.data.startswith('العنوان الفرعي'):
        await query.answer()
        try:
            stream_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]
            await extract_subtitle(client, query.message, data)
        except:
            await query.message.edit_text("**التفاصيل غير موجودة**")  


    elif query.data.startswith('الغاء'):
        try:
            query_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)] 
            await clean_up(data['موقع'])  
            await query.message.edit_text("**ألغيت...**")
            await query.answer(
                "Cancelled...",
                show_alert=True
            ) 
        except:
            await query.answer() 
            await query.message.edit_text("**التفاصيل غير موجودة**")        
