import logging
from telegram.ext import CommandHandler, Application
from telegram import ReplyKeyboardMarkup
from random import randrange

ANECDOTS = ['Слово "йепеленеще" может звучать странно, но в обратную сторону это еще нелепей.',
            'Штирлиц сломал руку в трех местах. Больше он в этих местах появляться не собирается.',
            'Изобрел Попов радио, включил — а слушать-то нечего!',
            'Если смотреть на спящего человека 8 часов, то он проснётся.',
            '''Отец шлет сыну телеграмму:
- Как прошел экзамен? Доложи немедленно.
- Экзамен прошел блестяще, профессора в восторге. Просят повторить осенью.''',
            '''Если футболистов начнут судить, то это будет первый в истории случай, когда на суде будут судья,
             прокурор, защитник, полузащитник и нападающий.''',
            '''Чего боятся американские математики больше всего?

                Ракет³''',
            '''Сидят психи у унитаза и рыбачат, заходит врач спрашивает: ну что, клюет?
Вместе отвечают: да клюет
Но один из них говорит: нет, не клюет
Врач говорит: ну вот, уже здоров, выписывать пора
Подходят психи прямо перед выпиской друга и спрашивают: а почему ты сказал что не клюёт?
Он отвечает: я че дурак что ли, рыбные места выдавать.''',
            '''Поймали как-то инопланетяне немца, американца и русского и говорят им:
— Кто первый заберётся на гору - оставим в живых, а двух других пустим на опыты.
Приходят к финишу одновременно американец и немец, смотрят, русского всё нет и нет. Инопланетяне не выдержали и спросили:
— Да где же этот русский?
— Домой ушёл.''',
            '''— Брат, 150км/ч куда ты гонишь?
*160... 180... 200... *
— Тебя любимая бросила, и ты не хочешь больше жить?
*220... 240... 260...*
— Брат,может стоит остановиться, брат?
— Саня, не лезь под руку, дай скорость для взлёта набрать''']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

BOT_TOKEN = '***'

reply_keyboard = [['/menu']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот-планировщик:)"
    )
    await update.message.reply_text(reply_markup=markup)


async def anecdot(update, context):
    random = randrange(0, len(ANECDOTS))
    await update.message.reply_text(ANECDOTS[random])


async def menu(update, context):
    await update.message.reply_text('Команды бота:\n'
                                    '/add_task <name of task> - Добавить задачу.\n'
                                    '/task <number of task> - вывести задачу по номеру\n'
                                    '/all_task - вывести список задач\n'
                                    '/remove <number of task> - удалить задачу\n'
                                    '/anecdot - анекдот')


USER_DATA = []


async def add_task(update, context):
    locality = context.args[0]
    await update.message.reply_text(
        f"Добавлена задача: {locality}")
    USER_DATA.append(locality)


async def all_tasks(update, context):
    user_dt = []
    for i in range(len(USER_DATA)):
        user_dt.append(f'{i+1}) {USER_DATA[i]}')
    if USER_DATA:
        await update.message.reply_text('Ваши задачи:')
        await update.message.reply_text('\n'.join(user_dt))
    else:
        await update.message.reply_text('У вас нет установленных задач')


async def remove_task(update, context):
    try:
        locality = int(context.args[0])
        await update.message.reply_text(f'Задача "{USER_DATA[locality - 1]}" удалена')
        del USER_DATA[locality - 1]
    except Exception:
        await update.message.reply_text('Неправильный номер задачи')


async def number_task(update, context):
    try:
        locality = int(context.args[0])
        try:
            await update.message.reply_text(USER_DATA[locality])
        except IndexError:
            await update.message.reply_text("Такой задачи не существует")
    except Exception:
        await update.message.reply_text('Неправильный номер задачи')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_task", add_task))
    application.add_handler(CommandHandler("all_task", all_tasks))
    application.add_handler(CommandHandler("task", number_task))
    application.add_handler(CommandHandler("remove", remove_task))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("anecdot", anecdot))

    application.run_polling()


if __name__ == '__main__':
    main()