import requests, os, dotenv


dotenv.load_dotenv()


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


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN: str = os.getenv('BOT_TOKEN')

# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 6

# Словарь, в котором будут храниться словари-состояния пользователей
users: dict = {}

yes_list: list = ['Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть', '+', 'Yes', 'Y', 'Lf', 'Ok']
no_list: list = ['Нет', 'Не', 'Не хочу', 'No', '-', 'Ytn', 'N']
alphabet: str = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
cat_response: requests.Response
cat_link: str

API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://aws.random.cat/meow'
# API_GRLS_URL: str = 'https://zagony.ru/admin_new/foto/2022-8-12/1660291926/devushki-v-bikini-74-foto_'
MEGA1_URL: str = 'https://uprostim.com/110-foto-krasivyh-lits-devushek/'
MEGA2_URL: str = 'https://uprostim.com/160-foto-krasivyh-devushek-18-let/'
YUMOR_URL: str = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'

TEXT_START = 'Привет!\nДавай сыграем в игру "Угадай число или слово"?\n\n' \
             'Чтобы получить правила игры и список доступных команд - отправьте команду /help'
TEXT_HELP = f'<b>Правила игры</b>:\n\nЯ загадываю ЧИСЛО от 1 до 100 и СЛОВО. Выберите для себя, ' \
            f'что Вы будете отгадывать, число или слово. И Вам нужно это отгадать.\n' \
            f'У вас есть <b>{ATTEMPTS}</b> попыток.\nВ любом случае, при выигрыше Вы получите ' \
            f'<b>ПРИЗ</b>!!!\n\n<b>Доступные команды</b>:\n' \
            f'/help - правила игры и список команд\n/cancel - выйти из игры\n' \
            f'/stat - посмотреть статистику\n/? - получить подсказку по загаданному слову\n\n' \
            f'<i>Давай сыграем?</i>'
TEXT_CANCEL = 'Вы вышли из игры. Если захотите сыграть снова - напишите об этом'
TEXT_OTHER = 'Пока мы играем в игру я могу реагировать только на числа от 1 до 100, ' \
             'русские буквы и команды /cancel, /stat и /?'
TEXT_ELSE = 'Мы ещё не играем. Хотите сыграть?'
TEXT_NEG = '<i>Жаль</i> \U0001F641\n\nЕсли захотите поиграть - просто напишите об этом'
