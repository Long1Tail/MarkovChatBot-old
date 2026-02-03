from config import TOKEN
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from generation import generate

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class MarkovBot():
    def __init__(self, token):
        self.token = token
        self.app = ApplicationBuilder().token(token).build()
        self.data2 = {}
        self.data1 = {}
        self.app.add_handler(CommandHandler('start', self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.read_message))
        self.app.add_handler(CommandHandler('generate', self.generate))
        self.app.run_polling()



    def add_handler(self, handler):
        self.app.add_handler(handler)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Привет. Я бот для генерации фраз. Чем больше ты со мной общаешься, тем умн"
                                            "ее я становлюсь. Ну ка, попробуй что-нибудь сгенерировать!")

    async def generate(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=generate(int(context.args[0]), self.data1, self.data2))
        print(context.args)

    async def read_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        await self.parse(update.message.text)

    async def parse(self, text: str):
        text.replace('\n', ' ')
        for i in ',./?<>"\':;][}{=+-_)(*&^%$#@!№1234567890«':
            text = text.replace(i, '')
        while text.count('  '):
            text = text.replace('  ', ' ')
        text = text.lower()
        text = text.split()
        for i in range(len(text) - 2):
            pare = [text[i], text[i + 1]]
            if ' '.join(pare) not in self.data1.keys():
                self.data1[' '.join(pare)] = []
            self.data1[' '.join(pare)].append(text[i + 2])
        for i in range(len(text) - 1):
            if text[i] not in self.data2.keys():
                self.data2[text[i]] = []
            self.data2[text[i]].append(text[i + 1])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Привет. Я бот для генерации фраз. Чем больше ты со мной общаешься, тем умнее"
                                        " я становлюсь. Ну ка, попробуй что-нибудь сгенерировать!")


async def read_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)


if __name__ == '__main__':
    app = MarkovBot(TOKEN)
