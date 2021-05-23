from interface import *


# Если этот файл является основным, то
if __name__ == '__main__':
    # Инициализируем и запускаем интерфейс
    eel.init('')
    eel.start('index.html', size=(1280, 720))