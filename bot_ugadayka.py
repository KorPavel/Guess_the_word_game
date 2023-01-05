# Игра "Угадай число или слово"
import requests
from config import BOT_TOKEN, ATTEMPTS, users, yes_list, no_list, \
    alphabet, API_URL, display_lives
from config import TEXT_START, TEXT_HELP, TEXT_CANCEL, TEXT_OTHER, TEXT_ELSE, TEXT_NEG
from extensions import get_anekdot, game_win_grls, get_random_number, get_random_word
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.dispatcher.filters import Text
from time import sleep

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher(bot)

# Создаем объект клавиатуры
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# Создаем объекты кнопок
button_1: KeyboardButton = KeyboardButton('\U00002714 Да')
button_2: KeyboardButton = KeyboardButton('\U0000274C Нет')
button_3: KeyboardButton = KeyboardButton('\U0001F914 Подсказка к слову')
button_4: KeyboardButton = KeyboardButton('\U0001F923 Анекдот')

# Добавляем кнопки в клавиатуру методом add
keyboard.add(button_1, button_2)
keyboard.add(button_3, button_4)


async def process_start_command(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/start" """
    await message.answer(TEXT_START, reply_markup=keyboard)
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
    await message.answer(TEXT_HELP)


async def process_stat_command(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/stat" """
    await message.answer(f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
                         f'Игр выиграно: {users[message.from_user.id]["wins"]}')


async def process_hint_command(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/?" """
    await message.answer(f'Подсказка по загаданному слову:\n'
                         f'{users[message.from_user.id]["help_word"]}\n')


async def next_anekdot(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/++" """
    await message.answer(f'А вот ещё анекдот:\n\n<i>{get_anekdot()}</i>')


async def next_pict(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/&&" """
    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={message.from_user.id}&photo={game_win_grls()}')


async def process_cancel_command(message: Message):
    """ Этот хэндлер будет срабатывать на команду "/cancel" """
    if users[message.from_user.id]['in_game']:
        await message.answer(TEXT_CANCEL)
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
        users[message.from_user.id]['result_word'] = '_' * len(users[message.from_user.id]['secret_word'])
        await message.answer(f'<b>Ура!</b>\n\nЯ загадал число от 1 до 100\n'
                             f'и вот такое слово <b>"{" ".join(list(users[message.from_user.id]["result_word"]))}"</b> '
                             f'из {len(users[message.from_user.id]["secret_word"])} букв.\n'
                             f'Попробуйте отгадать ЧИСЛО или СЛОВО.\n'
                             f'<i>Ваши попытки:</i>\n{display_lives(users[message.from_user.id]["attempts"])}')
    else:
        await message.answer(TEXT_OTHER)
        __import__('pprint').pprint(users)


async def process_negative_answer(message: Message):
    """ Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру """
    if not users[message.from_user.id]['in_game']:
        await message.answer(TEXT_NEG)
    else:
        await message.answer(TEXT_OTHER)


async def process_numbers_answer(message: Message):
    """ Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100 """
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(f'<i><b>БРАВО!!!</b></i> Вы отгадали моё число!\nВ качестве приза '
                                 f'вот Вам интересная картинка:')
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
                f'А вот Вам мой новый анекдот:\n\n<i>{get_anekdot()}</i>')
            sleep(5)
            await message.answer('Может сыграем ещё разок?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer(TEXT_ELSE)


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
                                 f'{display_lives(users[message.from_user.id]["attempts"])}')
        else:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer(f'Буквы "<b>{ltr}</b>" этом слове НЕТ!\n'
                                 f'<b>"{" ".join(list(users[message.from_user.id]["result_word"]))}"</b>\n'
                                 f'{display_lives(users[message.from_user.id]["attempts"])}')

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(
                f'К сожалению, у вас больше не осталось попыток. Вы проиграли \U0001F641\n\n'
                f'Моё слово было "<b>{users[message.from_user.id]["secret_word"]}</b>"\n\n'
                f'Не расстраивайтесь!\nВам обязательно повезёт в следующий раз.\nА вот Вам '
                f'мой новый анекдот:\n\n<i>{get_anekdot()}</i>')
            sleep(5)
            await message.answer(f'Давайте сыграем ещё?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1

        if '_' not in users[message.from_user.id]["result_word"]:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(f'<i><b>БРАВО!!!</b></i> Вы отгадали моё слово!\nВ качестве приза '
                                 f'вот Вам интересная картинка:')
            requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={message.from_user.id}&photo={game_win_grls()}')
            await message.answer('Может, сыграем ещё?')
    else:
        await message.answer(TEXT_ELSE)


async def process_other_text_answers(message: Message):
    """ Этот хэндлер будет срабатывать на остальные текстовые сообщения """
    if users[message.from_user.id]['in_game']:
        await message.answer(TEXT_OTHER)
    else:
        await message.answer('Я довольно ограниченный бот, давайте просто сыграем в игру?')


# Регистрируем хэндлеры
dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_help_command, commands='help')
dp.register_message_handler(process_stat_command, commands='stat')
dp.register_message_handler(process_cancel_command, commands='cancel')
dp.register_message_handler(process_hint_command, commands='?')
dp.register_message_handler(next_anekdot, commands='++')
dp.register_message_handler(next_pict, commands='&&')
dp.register_message_handler(process_positive_answer, Text(equals=yes_list, ignore_case=True))
dp.register_message_handler(process_negative_answer, Text(equals=no_list, ignore_case=True))
dp.register_message_handler(process_positive_answer, text='\U00002714 Да')
dp.register_message_handler(process_negative_answer, text='\U0000274C Нет')
dp.register_message_handler(process_hint_command, text='\U0001F914 Подсказка к слову')
dp.register_message_handler(next_anekdot, text='\U0001F923 Анекдот')
dp.register_message_handler(process_numbers_answer, lambda x: x.text.isdigit() and 1 <= int(x.text) <= 100)
dp.register_message_handler(process_letters_answer, lambda x: x.text.isalpha() and x.text in alphabet)
dp.register_message_handler(process_other_text_answers)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
