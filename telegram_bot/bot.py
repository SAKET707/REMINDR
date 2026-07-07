from telegram.ext import (
    Application,
    CommandHandler,
)

from config import BOT_TOKEN
from handlers import start


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    print("REMINDR Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()