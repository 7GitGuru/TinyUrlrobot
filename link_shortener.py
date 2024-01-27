import aiogram
from pyshorteners import Shortener

bot = aiogram.Bot(token='')
dp = aiogram.Dispatcher(bot)

shortener = Shortener()


# Function to shorten links
def shorten_link(original_url: str) -> str:
    try:
        # Ensure the URL starts with http:// or https://
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url

        shortened_url = shortener.tinyurl.short(original_url)
        return shortened_url
    except Exception as e:
        return f" {str(e)}"


# Regular expression pattern for URL detection
url_pattern = (r'\b(?:https?://)?'  # http:// or https:// (optional)
               r'(?:www\.)?'  # www. (optional)
               r'[^ \n]*'  # Domain and path
               r'\.[^ \n]{2,4}'  # TLD
               r'[^ \n]*\b')  # Path and query string (optional)


# /start
@dp.message_handler(commands=['start'])
async def start(message: aiogram.types.Message):
    start_text = (
        "Welcome to TinyURLrobot! 🤖\n"
        "I'm here to help you shorten your URLs quickly and easily.\n\n"
        "Owner: @Cod3rX\n"  # Replace @username with your actual username
        "Source: [GitHub](https://github.com/7GitGuru/Url-Shortener-Bot)"
    )
    await message.reply(start_text, parse_mode='Markdown', disable_web_page_preview=True)



# /help
@dp.message_handler(commands=['help'])
async def send_help(message: aiogram.types.Message):
    help_text = (
        "This bot is designed to make your long URLs short and sweet. Here's how to use it:\n\n"
        "<b>Direct Message</b>:\nSend any URL directly to me. Formats like <i>google.com</i> or <i>https://google.com</i> (all are accepted). I'll reply with the shortened URL.\n\n"
        "<b>Mention Mode</b>:\nIn any chat, tag me like this\n<code>@tinyURLrobot google.com</code>\nI'll reply with the shortened URL.\n\n"
        "Use these methods to shorten your links effortlessly!"
    )
    await message.reply(help_text, parse_mode='HTML', disable_web_page_preview=True)


# Message handler for links sent directly to the bot
@dp.message_handler(regexp=url_pattern)
async def process_direct_link(message: aiogram.types.Message):
    original_url = message.text
    shortened_url = shorten_link(original_url)
    response_message = (f"Shortened URL: {shortened_url}\n\n"
                        f"Made with ❤️ by [TinyURLrobot](t.me/tinyURLrobot) | Owner: [$𝙱𝚘𝚑𝚍𝚊𝚗](t.me/Cod3rX)")
    await message.reply(response_message, parse_mode='Markdown', disable_web_page_preview=True)


# Message handler for links after bot mention
@dp.message_handler(lambda message: message.entities and message.entities[0].type == 'mention')
async def process_mention(message: aiogram.types.Message):
    user_id = message.from_user.id
    original_url = None

    # Check if the mention is followed by a link
    if len(message.entities) > 1 and message.entities[1].type == 'url':
        original_url = message.text[message.entities[1].offset:message.entities[1].offset + message.entities[1].length]

    if original_url:
        shortened_url = shorten_link(original_url)
        response_message = (f"Shortened URL: {shortened_url}\n\n"
                            f"Made with ❤️ by [TinyURLrobot](t.me/tinyURLrobot) | Owner: [$𝙱𝚘𝚑𝚍𝚊𝚗](t.me/Cod3rX)")
        await message.reply(response_message, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await message.reply("❗️Please include a valid URL")


# Inline
@dp.inline_handler()
async def process_inline_query(inline_query: aiogram.types.InlineQuery):
    original_url = inline_query.query
    shortened_url = shorten_link(original_url)

    result = aiogram.types.InlineQueryResultArticle(
        id=inline_query.id,
        title="Shorten Link",
        input_message_content=aiogram.types.InputTextMessageContent(
            (f"Shortened URL: {shortened_url}\n\n"
             f"Made with ❤️ by [TinyURLrobot](t.me/tinyURLrobot) | Owner: [$𝙱𝚘𝚑𝚍𝚊𝚗](t.me/Cod3rX)"),
            parse_mode='Markdown', disable_web_page_preview=True
        )
    )

    await bot.answer_inline_query(inline_query.id, results=[result])


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
