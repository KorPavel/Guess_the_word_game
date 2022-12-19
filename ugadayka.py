
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


def words_updates() -> None:
    """ Функция добавляет новые слова в словарь и записывает его в файл 'ugadayka_words.txt' """
    dct = read_words()
    while True:
        a = input('Введите новое слово: ').upper()
        if any([' ' in a, '-' in a, '$' in a]):
            print('Здесь должно быть введено только ОДНО слово и без дефисов!')
            continue
        elif a == '':
            break
        b = input('Введите подсказку: ').capitalize()
        dct.setdefault(a, b)
        with open('ugadayka_words.txt', 'w', encoding='utf-8') as f:
            for k, v in dct.items():
                f.write(k+'$'+v+'\n')
        print(f'Слово {a!r} успешно записано в словарь. Теперь в словаре {len(dct)} '
              f'слов{["", "о", "а", "а", "а", "", "", "", "", ""][len(dct)%10]}.')
        ch = input('Хотите добавить ещё слово? [д/н] ')
        if ch.upper() != 'Н':
            continue
        break


def get_word() -> str:
    """ Функция выбора случайного слова """
    word = __import__('random').choice(words)
    return word


def game_reset() -> (str, str):
    """ Функция сброса списков """
    print('Обнуляем список слов...')
    words_list_copy = words_list.copy()
    guessed_words = []
    return words_list_copy, guessed_words


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


def letter_input(guessed_letters: list, word: str) -> str:
    """ Функция проверки введенного символа """
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    while True:
        letter = input('Введите букву или слово: ')
        letter = letter.upper()
        if letter == '==':
            exit()
        elif len(letter) == 1 and letter not in alphabet: # set(letter) <= set(alphabet):
            print('Перейдите на русскую раскладку.')
        elif len(letter) == 1 and letter in guessed_letters:
            print(f'Будьте внимательны! Букву \033[1;31m{letter}\033[0m Вы уже называли.')
        elif len(letter) > 1 and len(letter) != len(word):
            print('Будьте внимательны! Введено несколько букв.')
        elif letter == '':
            print('Вы пока ничего не ввели.')
        elif len(letter) == len(word) and letter[0] not in alphabet:
            print("Если Вы хотите ввести слово целиком, перейдите на русскую раскладку.")
        else:
            break
    return letter


def game_over(wrd: str) -> None:
    """ Функция вывода сообщения о проигрыше """
    print(f'\n\033[1;30;41m К сожалению, попытки закончились, '
          f'и Вы не угадали слово {wrd} \033[0m\n')


def game_win() -> None:
    """ Функция вывода сообщения о выигрыше """
    print(f'\n\033[1;30;42m Верно! Слово угадано! \033[0m\n')


def display_stats(word_completion: list, lives: str, guessed_letters: list,
                  help_word: str, sp: list) -> None:
    """ Функция отображения статуса игры """
    quiz_word = ' '.join(word_completion)  # Перевод загаданного слова из списка в строку
    guessed_letters.sort()  # Сортировка названых букв
    u_letters = ' '.join(guessed_letters)  # Перевод названых букв из списка в строку
    polka = '\033[35m░░\033[0m' * (len(word_completion) + 3) + '\033[35m░\033[0m'
    print(f"\n{polka}       \033[32mВаши попытки:\033[0m")
    print(f'\033[35m░░\033[0m  {quiz_word}  \033[35m░░\033[0m     {lives}')
    print(f'{polka} \033[32m Ваши победы:\033[0m {sp[0]} из {sp[1]} слов{["", "а"][sp[1]%10 == 1]}.')
    print(f'\033[1;36m ПОДСКАЗКА: \033[0m{help_word.capitalize()!r}')
    print(f'\033[33m ИСПОЛЬЗОВАННЫЕ БУКВЫ:\033[0m {u_letters}')


def play_game(word: str, words_dict: dict, guessed_words: list, loose_game: bool) -> (list, bool):
    """ Функция, осуществляющая игровую сессию """
    word_completion = list('_' * len(word))  # Создание списка для загаданного слова с '_' вместо неотгаданных букв
    help_word = words_dict[word]  # Получение подсказки
    guessed_letters = []
    tries = 6
    lives = display_lives(tries)
    print('Давайте играть в угадайку слов!')
    while not loose_game and tries > 0:  # Основной цикл игровой сессии
        display_stats(word_completion, lives, guessed_letters, help_word, [len(guessed_words), len(words_dict)])

        if '_' not in word_completion:  # Проверка, угадано ли слово
            guessed_words.append(word)  # Добавление угаданного слова к списку угаданных слов
            words.remove(word)  # Удаление угаданного слова из списка слов
            display_stats(word_completion, lives, guessed_letters, help_word, [len(guessed_words), len(words_dict)])
            game_win()
            return guessed_words, loose_game

        ltr = letter_input(guessed_letters, word)  # Ввод буквы или слова

        if len(ltr) == 1:
            if ltr in word:  # Если буква угадана
                guessed_letters.append(ltr)  # Добавление угаданной буквы к списку использованных букв
                for i in range(len(word)):  # Подстановка угаданной буквы в загаданное слово
                    if word[i] == ltr:
                        word_completion[i] = ltr
                print('\033[32m Есть такая буква! \033[0m\U0001F44D')
            else:  # Если буква не угадана
                guessed_letters.append(ltr)
                tries -= 1
                lives = display_lives(tries)
                print('\033[31m Нет такой буквы в этом слове! \033[0m\U0001F44E')
        elif len(ltr) == len(word):
            if ltr == word:
                word_completion = list(word)
                print('Ура! Вы угадали слово!')
            else:
                print('Неверно! Вы ошиблись. Загадано другое слово')
                tries -= 1
                lives = display_lives(tries)

        if tries == 0:  # Если кончились попытки
            print('\U0001F4A9')
            loose_game = True
            display_stats(word_completion, lives, guessed_letters, help_word, [len(guessed_words), len(words_dict)])
            game_over(word)
            return guessed_words, loose_game


guessed_words = []  # Пустой список угаданных слов
loose_game = False  # Переменная проигрыша (для сброса списков)
check = "Д"
# Основной цикл игры
while check != "Н":
    if not words:  # Сброс, если закончились слова в списке
        words, guessed_words = game_reset()
        print('\U0001F389 \033[32m Поздравляем! Вы угадали все слова!\033[0m \U0001F3C6 \U0001F37E')
    elif loose_game:  # Сброс, если игрок проиграл
        words, guessed_words = game_reset()
        print('Ваши попытки закончились, Вы проиграли. :(((')

    word = get_word()
    guessed_words, loose_game = play_game(word, words_dct, guessed_words, loose_game)  # Запуск игровой сессии
    check = input('Пополнить словарь новым словом [слово],\n'
                  'продолжать играть или выйти?[д/н]: ').upper()  # Проверка окончания игры

    if check == 'СЛОВО':
        words_updates()

print('Спасибо за игру!')