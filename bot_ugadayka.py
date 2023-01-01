# Игра "Угадай число или слово"
import requests
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from time import sleep

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN: str = 'BOT TOKEN HERE'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)

# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 6

# Словарь, в котором будут храниться словари-состояния пользователей
users: dict = {}

yes_list: list = ['Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть', '+', 'Yes', 'Y', 'Lf', 'Ok']
no_list: list = ['Нет', 'Не', 'Не хочу', 'No', '-', 'Ytn', 'N']
alphabet: str = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://aws.random.cat/meow'
cat_response: requests.Response
cat_link: str


def display_lives(tries) -> str:
    """ Функция выбора графического отображения оставшихся попыток """
    stages = ["\U0001f90D \U0001f90D \U0001f90D \U0001f90D \U0001f90D \U0001f90D",
              "\U0001f9E1 \U0001f90D \U0001f90D \U0001f90D \U0001f90D \U0001f90D",
              "\U0001f9E1 \U0001f9E1 \U0001f90D \U0001f90D \U0001f90D \U0001f90D",
              "\U0001f9E1 \U0001f9E1 \U0001f9E1 \U0001f90D \U0001f90D \U0001f90D",
              "\U0001f9E1 \U0001f9E1 \U0001f9E1 \U0001f9E1 \U0001f90D \U0001f90D",
              "\U0001f9E1 \U0001f9E1 \U0001f9E1 \U0001f9E1 \U0001f9E1 \U0001f90D",
              "\U0001f9E1 \U0001f9E1 \U0001f9E1 \U0001f9E1 \U0001f9E1 \U0001f9E1"]
    return stages[tries]


def read_words() -> dict:
    """ Функция получает слова с их значениями из файла 'ugadayka_words.txt'.
    Если такого файла не окажется, функция создаст в той же папке, что и
    основная программа новый файл с одним словом. Вам нужно будет придумывать
    новые слова для пополнения словаря. Новые слова будут доступны при запуске
    нового сеанса игры. """
    if __import__('os.path').path.exists('ugadayka_words.txt'):
        with open('ugadayka_words.txt', encoding='utf-8') as f:
            words_dict = {}
            for row in f.readlines():
                k, v = row.split('$')
                words_dict.setdefault(k, v.strip())
    else:
        with open('ugadayka_words.txt', 'w', encoding='utf-8') as f:
            f.write('ПОЛДЕНЬ$12:00\n')
        words_dict = {'ПОЛДЕНЬ': '12:00'}
    return words_dict


words_dct = read_words()
words_list = list(words_dct.keys())
words = words_list.copy()


def get_random_word() -> tuple[str, str]:
    """ Выбор случайного слова. Подсказка к слову прилагается """
    word = __import__('random').choice(words)
    help_word = words_dct[word]
    return word, help_word


def get_random_number() -> int:
    """ Функция возвращает случайное целое число от 1 до 100 """
    return __import__('random').randint(1, 100)


def game_win_grls() -> str:
    mega = 'https://kykyryzo.ru/devushki-v-mini-bikini/'
    try:
        sor = requests.get(mega).text
        sp = [el.replace('src=\"', '').strip('\"') for el in sor.split()
              if el.startswith('src="https://img-fotki.yandex.ru')]
        pict = __import__('random').choice(sp)
        return pict
    except:
        return game_win_cat()


def game_win_cat() -> str:
    """ Функция отправляет пользователю случайную фотку с котиком """
    cat_response = requests.get(API_CATS_URL)
    if cat_response.status_code == 200:
        return cat_response.json()['file']
    return ''


def get_anekdot() -> str:
    """ Функция отправляет пользователю случайный анекдот """
    url = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'
    yumor_response = requests.get(url)
    if yumor_response.status_code == 200:
        return yumor_response.text[12:-2]
    return ''


async def process_start_command(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/start" """
    await message.answer(
        'Привет!\nДавай сыграем в игру "Угадай число или слово"?\n\n'
        'Чтобы получить правила игры и список доступных команд - отправьте команду /help')
    # Если пользователь только запустил бота и его нет в словаре users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'secret_word': None,
                                       'help_word': None,
                                       'result_word': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}


async def process_help_command(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/help" """
    await message.answer(
        f'<b>Правила игры</b>:\n\nЯ загадываю ЧИСЛО от 1 до 100 и СЛОВО. Выберите для себя, '
        f'что Вы будете отгадывать, число или слово. И Вам нужно это отгадать.\n'
        f'У вас есть <b>{ATTEMPTS}</b> попыток.\nВ любом случае, при выигрыше Вы получите '
        f'<b>ПРИЗ</b>!!!\n\n<b>Доступные команды</b>:\n'
        f'/help - правила игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n/? - получить подсказку по загаданному слову\n\n'
        f'<i>Давай сыграем?</i>', parse_mode="html")


async def process_stat_command(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/stat" """
    await message.answer(f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
                         f'Игр выиграно: {users[message.from_user.id]["wins"]}')


async def process_hint_command(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/?" """
    await message.answer(f'Подсказка по загаданному слову:\n'
                         f'{users[message.from_user.id]["help_word"]}\n')


async def process_cancel_command(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/cancel" """
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть снова - '
                             'напишите об этом')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. Может, сыграем разок?')


async def process_positive_answer(message: Message):
    """ Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру """
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        users[message.from_user.id]['secret_word'], users[message.from_user.id]['help_word'] = get_random_word()
        users[message.from_user.id]['result_word'] = '_'*len(users[message.from_user.id]['secret_word'])
        await message.answer(f'<b>Ура!</b>\n\nЯ загадал число от 1 до 100\n'
                             f'и вот такое слово <b>"{" ".join(list(users[message.from_user.id]["result_word"]))}"</b> '
                             f'из {len(users[message.from_user.id]["secret_word"])} букв.\n'
                             f'Попробуйте отгадать ЧИСЛО или СЛОВО.\n'
                             f'<i>Ваши попытки:</i>\n{display_lives(users[message.from_user.id]["attempts"])}',
                             parse_mode="html")
    else:
        await message.answer(
            'Пока мы играем в игру я могу реагировать только на числа от 1 до '
            '100, русские буквы и команды /cancel, /stat и /?')
        __import__('pprint').pprint(users)


async def process_negative_answer(message: Message):
    """ Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру """
    if not users[message.from_user.id]['in_game']:
        await message.answer('<i>Жаль</i> \U0001F641\n\nЕсли захотите поиграть - '
                             'просто напишите об этом', parse_mode='html')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, числа от 1 до 100 или русские буквы')


async def process_numbers_answer(message: Message):
    """ Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100 """
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(f'<i><b>БРАВО!!!</b></i> Вы отгадали моё число!\nВ качестве приза '
                                 f'вот Вам интересная картинка:', parse_mode='html')
            requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={message.from_user.id}&photo={game_win_grls()}')
            await message.answer('Может, сыграем ещё?')
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer(f'Моё число МЕНЬШЕ!\n{display_lives(users[message.from_user.id]["attempts"])}')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer(f'Моё число БОЛЬШЕ!\n{display_lives(users[message.from_user.id]["attempts"])}')

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(
                f'К сожалению, у вас больше не осталось попыток. Вы проиграли \U0001F641\n\n'
                f'Моё число было <b>{users[message.from_user.id]["secret_number"]}</b>\n\nНе расстраивайтесь!\n'
                f'Вам обязательно повезёт в следующий раз.\n'
                f'А вот Вам мой новый анекдот:\n\n<i>{get_anekdot()}</i>', parse_mode='html')
            sleep(10)
            await message.answer('Может сыграем ещё разок?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Мы ещё не играем. Хотите сыграть?')


async def process_letters_answer(message: Message):
    """ Этот хэндлер будет срабатывать на отправку пользователем русских букв """
    ltr = message.text.upper()
    if users[message.from_user.id]['in_game']:
        if len(ltr) == 1 and ltr in users[message.from_user.id]['secret_word']:
            result_lst = list(users[message.from_user.id]['result_word'])
            for i in range(len(users[message.from_user.id]['secret_word'])):
                if users[message.from_user.id]['secret_word'][i] == ltr:
                    result_lst[i] = ltr
            users[message.from_user.id]['result_word'] = ''.join(result_lst)
            await message.answer(f'Ура!!! Буква "<b>{ltr}</b>" в этом слове ЕСТЬ!\n'
                                 f'<b>"{" ".join(list(users[message.from_user.id]["result_word"]))}"</b>\n'
                                 f'{display_lives(users[message.from_user.id]["attempts"])}', parse_mode='html')
        else:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer(f'Буквы "<b>{ltr}</b>" этом слове НЕТ!\n'
                                 f'<b>"{" ".join(list(users[message.from_user.id]["result_word"]))}"</b>\n'
                                 f'{display_lives(users[message.from_user.id]["attempts"])}', parse_mode='html')

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(
                f'К сожалению, у вас больше не осталось попыток. Вы проиграли \U0001F641\n\n'
                f'Моё слово было "<b>{users[message.from_user.id]["secret_word"]}</b>"\n\n'
                f'Не расстраивайтесь!\nВам обязательно повезёт в следующий раз.\nА вот Вам '
                f'мой новый анекдот:\n\n<i>{get_anekdot()}</i>', parse_mode='html')
            sleep(10)
            await message.answer(f'Давайте сыграем ещё?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1

        if '_' not in users[message.from_user.id]["result_word"]:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(f'<i><b>БРАВО!!!</b></i> Вы отгадали моё слово!\nВ качестве приза '
                                 f'вот Вам интересная картинка:', parse_mode='html')
            requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={message.from_user.id}&photo={game_win_grls()}')
            await message.answer('Может, сыграем ещё?')
    else:
        await message.answer('Мы ещё не играем. Хотите сыграть?')


async def process_other_text_answers(message: Message):
    """ Этот хэндлер будет срабатывать на остальные текстовые сообщения """
    if users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, числа от 1 до 100 или русские буквы')
    else:
        await message.answer('Я довольно ограниченный бот, давайте просто сыграем в игру?')


# Регистрируем хэндлеры
dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_help_command, commands='help')
dp.register_message_handler(process_stat_command, commands='stat')
dp.register_message_handler(process_cancel_command, commands='cancel')
dp.register_message_handler(process_hint_command, commands='?')
dp.register_message_handler(process_positive_answer, Text(equals=yes_list, ignore_case=True))
dp.register_message_handler(process_negative_answer, Text(equals=no_list, ignore_case=True))
dp.register_message_handler(process_numbers_answer, lambda x: x.text.isdigit() and 1 <= int(x.text) <= 100)
dp.register_message_handler(process_letters_answer, lambda x: x.text.isalpha() and x.text in alphabet)
dp.register_message_handler(process_other_text_answers)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)