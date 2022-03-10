from bot import app, LOGGER
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from pyrogram.errors import QueryIdInvalid

thumb = "https://res.cloudinary.com/animezz-hub/image/upload/v1642851366/moviezzhub/thumb/IMG_20220122_170453_198_h6hflm.jpg"

@app.on_inline_query()
async def inline_search(_, event: InlineQuery):
    answers = list()
    LOGGER.info(event.query)
    if event.query == "":
        answers.append(
            InlineQueryResultArticle(
                title="Search Your Desired File Here",
                input_message_content=InputTextMessageContent(
                    "You can search your files anywhere anytime using inline method\n\nUse Search Button Below"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Search",
                                switch_inline_query_current_chat=""
                            )
                        ]
                    ]
                )
            )
        )
    else:
        key = event.query
        gdrive = GoogleDriveHelper()
        file_title, desc, drive_url, index_url, view_link = gdrive.drive_list_inline(key, isRecursive=False, itemType="both")
        if file_title:
            for title in file_title:
                # Limit number of search to less than 50
                if file_title.index(title) < 50:
                    answers.append(
                        InlineQueryResultArticle(
                            title=title,
                            description=desc[file_title.index(title)],
                            thumb_url=thumb,
                            input_message_content=InputTextMessageContent(
                                message_text=f"Title : {title}\n{desc[file_title.index(title)]}",
                                disable_web_page_preview=True
                            ),
                        reply_markup=InlineKeyboardMarkup([
                            [
                                InlineKeyboardButton("View Link", url=view_link[file_title.index(title)]),
                                InlineKeyboardButton("Drive Link", url=drive_url[file_title.index(title)])
                            ],
                            [
                               InlineKeyboardButton("Index Link", url=index_url[file_title.index(title)]),
                               InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")
                            ],
                        ])
                    )
                )
        else:
            answers.append(
                InlineQueryResultArticle(
                    title=f"No Result Found for {key}",
                    description="Try with another search key",
                    input_message_content=InputTextMessageContent(
                        message_text="No Result Found For Your Search Key\nTry with another search"
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")]
                    ])
                )
            )
    try:
        await event.answer(
            results=answers,
            cache_time=0
        )
    except QueryIdInvalid:
        LOGGER.info(f"QueryIdInvalid: {event.query}")

#@app.on_message(filters.command("sayonara"))
async def quit_group(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text="Sayonara",
        reply_to_message_id=update.message_id
    )
    await bot.leave_chat(
        chat_id=update.chat.id
    )

