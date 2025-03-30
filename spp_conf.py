from dotenv import set_key, load_dotenv
import os

env_file = '.env'
load_dotenv()

# Проверка на существование .env файла, если его нет - создаём
if not os.path.exists(env_file):
    with open(env_file, 'w') as file:
        pass

# Функция для добавления переменной окружения, если она еще не существует
def add_env_variable(key, value):
    if os.getenv(key) is None:  # Проверка, если переменная ещё не существует
        set_key(env_file, key, value)

# Добавляем переменные окружения, если они ещё не существуют
add_env_variable('speed', '0.20')
add_env_variable('background-min', '8, 177, 70')
add_env_variable('background-max', '0, 100, 0')
add_env_variable('screen-w', '600')
add_env_variable('screen-h', '600')
add_env_variable('sft', 'data/RussoOne-Regular.ttf')

