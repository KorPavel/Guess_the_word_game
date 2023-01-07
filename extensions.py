import os
import requests
from random import randint, choice
from config import API_CATS_URL, YUMOR_URL


def read_words() -> dict:
    """ Функция получает слова с их значениями из файла 'ugadayka_words.txt'.
    Если такого файла не окажется, функция создаст в той же папке, что и
    основная программа новый файл с одним словом. Вам нужно будет придумывать
    новые слова для пополнения словаря. Новые слова будут доступны при запуске
    нового сеанса игры. """
    if os.path.exists('ugadayka_words.txt'):
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
    word = choice(words)
    help_word = words_dct[word]
    return word, help_word


def get_random_number() -> int:
    """ Функция возвращает случайное целое число от 1 до 100 """
    return randint(1, 100)


def get_pict(list_url) -> str:
    try:
        sor = requests.get(choice(list_url)).text
        sp = [el.replace('src=\"', '').strip('\"') for el in sor.split()
              if el.startswith('src=\"https://') and '.jp' in el]
        pict = choice(sp)
        return pict
    except:
        return game_win_cat()


def game_win_cat() -> str:
    """ Функция отправляет пользователю случайную фотку с котиком за выигрыш в игре """
    cat_response = requests.get(API_CATS_URL)
    if cat_response.status_code == 200:
        return cat_response.json()['file']
    return ''


def get_anekdot() -> str:
    """ Функция отправляет пользователю случайный анекдот """
    yumor_response = requests.get(YUMOR_URL)
    if yumor_response.status_code == 200:
        return yumor_response.text[12:-2]
    return ''
