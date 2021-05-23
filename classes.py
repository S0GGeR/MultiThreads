import queue
import random
import threading
import datetime


class MultiThreadSimulator:
    def __init__(self):
        # Список для логирования данных
        self.log = []
        # Словарь (хэш-таблица), в которой будут храниться все наши потоки
        self.tasks = {}
        # Объект, необходимый для активации критической сессии (заблокировать выполнение блока кода)
        self.lock = threading.Lock()
        # Добавление задачи 'А' в словарь, инициализации потока
        self.tasks.update({'A': threading.Thread(target=self.task_a, args=(2 ** 21,), name='A')})
        # Запуск потока 'А'
        self.tasks['A'].start()
        # Очередь, для задач
        self.pipeline = queue.Queue(maxsize=10)

    def task_a(self, array_len):
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о запуске потока 'A'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "A" была запущена')
        # Инициализируем списки m1 и m2 для последующего их заполнения
        m1, m2 = [], []
        # Заполняем списки m1, m2 в цикле
        for i in range(0, array_len):
            # Список m1 - заполняется текущим индексом i
            m1.append(i)
            # Список m2 - заполняется иднексом i взятому по модулю два (i mod 2) и округленному до булева значения
            m2.append(bool(i % 2))
            # Задачи 'B', 'C', 'D' добавляются в словарь задач и инициализируются соответствующие потоки
        self.tasks.update({'B': threading.Thread(target=self.task_b, args=(m1, m2), name='B')})
        self.tasks.update({'C': threading.Thread(target=self.task_c, args=(m1, m2), name='C')})
        self.tasks.update({'D': threading.Thread(target=self.task_d, args=(m1, m2), name='D')})
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о вызове потоков 'B', 'C', 'D'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "А" запустила задачи "B", "C" и "D"')
        # Запускаются потоки 'B', 'C', 'D'
        self.tasks['B'].start()
        self.tasks['C'].start()
        self.tasks['D'].start()
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в переменную log инфомрацию о том, что поток 'A' завершён
            self.log.append(f'{datetime.datetime.now().time()}: Задача "A" была завершена')

    def task_b(self, m1, m2):
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о запуске потока 'B'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "B" была запущена')
        # Умножаем каждый элемент списка m1 на случайные integer заданного размере
        m1 = [number * random.randint(0, 2 ** 4) for number in m1]
        # Выполняем логичское умножение каждый элемент списка m2 на случайные boolean
        m2 = [boolean and bool(random.getrandbits(1)) for boolean in m2]
        # Проверяем завершена ли задача 'C'
        if not self.tasks['C'].is_alive():
            # Достаем из очереди списки полученные в результате выполнения задачи 'C'
            m3, m4 = self.pipeline.get()
            # Добавление задач 'E', 'F' в словарь, инициализации потока
            self.tasks.update({'E': threading.Thread(target=self.task_e, args=(m1, m2, m3, m4), name='E')})
            self.tasks.update({'F': threading.Thread(target=self.task_f, args=(m1, m2, m3, m4), name='F')})
            # Активируем критическую сессию
            with self.lock:
                # Добавляем в список log информацию о вызове потоков 'E', 'F'
                self.log.append(f'{datetime.datetime.now().time()}: Задача "B" запустила задачи "E", "F"')
            # Запускаем потоки 'E', 'F'
            self.tasks['E'].start()
            self.tasks['F'].start()
        else:
            # Так как задача 'B' завершается первой, то добавим списки m1, m2 в очередь
            self.pipeline.put((m1, m2))
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в переменную log инфомрацию о том, что поток 'B' завершён
            self.log.append(f'{datetime.datetime.now().time()}: Задача "B" была завершена')

    def task_c(self, m1, m2):
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о запуске потока 'C'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "C" была запущена')
        # Умножаем каждый элемент списка m1 на случайные integer заданного размере
        m1 = [number * random.randint(0, 2 ** 4) for number in m1]
        # Выполняем логичское умножение каждый элемент списка m2 на случайные boolean
        m2 = [boolean and bool(random.getrandbits(1)) for boolean in m2]
        # Проверяем завершена ли задача 'B'
        if not self.tasks['B'].is_alive():
            # Достаем из очереди списки полученные в результате выполнения задачи 'B'
            m3, m4 = self.pipeline.get()
            # Добавление задач 'E', 'F' в словарь, инициализации потока
            self.tasks.update({'E': threading.Thread(target=self.task_e, args=(m1, m2, m3, m4), name='E')})
            self.tasks.update({'F': threading.Thread(target=self.task_f, args=(m1, m2, m3, m4), name='F')})
            # Активируем критическую сессию
            with self.lock:
                # Добавляем в список log информацию о вызове потоков 'E', 'F'
                self.log.append(f'{datetime.datetime.now().time()}: Задача "C" запустила задачи "E", "F"')
            # Запускаем потоки 'E', 'F'
            self.tasks['E'].start()
            self.tasks['F'].start()
        else:
            # Так как задача 'C' завершается первой, то добавим списки m1, m2 в очередь
            self.pipeline.put((m1, m2))
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в переменную log инфомрацию о том, что поток 'C' завершён
            self.log.append(f'{datetime.datetime.now().time()}: Задача "C" была завершена')

    def task_d(self, m1, m2):
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о запуске потока 'D'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "D" была запущена')
        # Умножаем каждый элемент списка m1 на случайные integer заданного размере
        m1 = [number * random.randint(0, 2 ** 4) for number in m1]
        # Выполняем логичское умножение каждый элемент списка m2 на случайные boolean
        m2 = [boolean and bool(random.getrandbits(1)) for boolean in m2]
        # Добавление задачи 'H' в словарь, инициализация потока
        self.tasks.update({'H': threading.Thread(target=self.task_h, args=(m1, m2), name='H')})
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о вызове потока 'H'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "D" запустила задачу "H"')
        # Запускаем задачу 'E'
        self.tasks['H'].start()
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в переменную log инфомрацию о том, что поток 'D' завершён
            self.log.append(f'{datetime.datetime.now().time()}: Задача "D" была завершена')

    def task_e(self, m1, m2, m3, m4):
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о запуске потока 'E'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "E" была запущена')
        # Умножаем каждый элемент списков m1 + m2 е на случайные integer заданного размере
        m1 = [number * random.randint(0, 2 ** 4) for number in m1 + m3]
        # Выполняем логичское умножение каждый элемент списков m2 + m4 увеличенного вдвое на случайные boolean
        m2 = [boolean and bool(random.getrandbits(1)) for boolean in m2 + m4]
        # Проверяем завершены ли потоки 'H' и 'G'
        if not self.tasks['H'].is_alive() and not self.tasks['G'].is_alive():
            # Достаем из очереди списки полученные в результате выполнения задач 'K' и 'G'
            m3, m4 = self.pipeline.get()
            m5, m6 = self.pipeline.get()
            # Добавление задачи 'K' в словарь, инициализация потока
            self.tasks.update({'K': threading.Thread(target=self.task_k, args=(m1, m2, m3, m4, m5, m6), name='K')})
            # Активируем критическую сессию
            with self.lock:
                # Добавляем в список log информацию о вызове потока 'K'
                self.log.append(f'{datetime.datetime.now().time()}: Задача "E" запустила задачу "K"')
            # Запускаем задачу 'K'
            self.tasks['K'].start()
        else:
            # Так как задача 'E'  не завершается первой, то добавим списки m1, m2 в очередь
            self.pipeline.put((m1, m2))
        with self.lock:
            # Добавляем в переменную log инфомрацию о том, что поток 'E' завершён
            self.log.append(f'{datetime.datetime.now().time()}: Задача "E" была завершена')

    def task_f(self, m1, m2, m3, m4):
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о запуске потока 'F'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "F" была запущена')
        # Умножаем каждый элемент списка m1 на случайные integer заданного размере
        # Не используем m3, дабы сохранить дительность выполнения равное единице
        m1 = [number * random.randint(0, 2 ** 4) for number in m1]
        # Выполняем логичское умножение каждый элемент списка m4 на случайные boolean
        # Не используем m2, дабы сохранить дительность выполнения равное единице
        m2 = [boolean and bool(random.getrandbits(1)) for boolean in m4]
        # Добавление задачи 'G' в словарь, инициализация потока
        self.tasks.update({'G': threading.Thread(target=self.task_g, args=(m1, m2), name='G')})
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о вызове потока 'G'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "F" запустила задачу "G"')
        # Запускаем задачу 'G'
        self.tasks['G'].start()
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в переменную log инфомрацию о том, что поток 'F' завершён
            self.log.append(f'{datetime.datetime.now().time()}: Задача "F" была завершена')

    def task_g(self, m1, m2):
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о запуске потока 'G'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "G" была запущена')
        # Умножаем каждый элемент списка m1  на случайные integer заданного размере
        m1 = [number * random.randint(0, 2 ** 4) for number in m1]
        # Выполняем логичское умножение каждый элемент списка m2  на случайные boolean
        m2 = [boolean and bool(random.getrandbits(1)) for boolean in m2]
        # Проверяем завершены ли потоки 'E' и 'H'
        if not self.tasks['E'].is_alive() and not self.tasks['H'].is_alive():
            # Достаем из очереди списки полученные в результате выполнения задач 'H' и 'E'
            m3, m4 = self.pipeline.get()
            m5, m6 = self.pipeline.get()
            # Добавление задачи 'K' в словарь, инициализация потока
            self.tasks.update({'K': threading.Thread(target=self.task_k, args=(m1, m2, m3, m4, m5, m6), name='K')})
            # Активируем критическую сессию
            with self.lock:
                # Добавляем в список log информацию о вызове потока 'K'
                self.log.append(f'{datetime.datetime.now().time()}: Задача "G" запустила задачу "K"')
            # Запускаем задачу 'K'
            self.tasks['K'].start()
        else:
            # Так как задача 'G' не завершается первой, то добавим списки m1, m2 в очередь
            self.pipeline.put((m1, m2))
        with self.lock:
            # Добавляем в переменную log инфомрацию о том, что поток 'G' завершён
            self.log.append(f'{datetime.datetime.now().time()}: Задача "G" была завершена')

    def task_h(self, m1, m2):
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о запуске потока 'H'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "H" была запущена')
        # Умножаем каждый элемент списка m1 увеличенного вдвое на случайные integer заданного размере
        m1 = [number * random.randint(0, 2 ** 4) for number in m1 * 2]
        # Выполняем логичское умножение каждый элемент списка m2 увеличенного вдвое на случайные boolean
        m2 = [boolean and bool(random.getrandbits(1)) for boolean in m2 * 2]
        # Проверяем завершены ли потоки 'G' и 'E'
        if not self.tasks['G'].is_alive() and not self.tasks['E'].is_alive():
            # Достаем из очереди списки полученные в результате выполнения задач 'G' и 'E'
            m3, m4 = self.pipeline.get()
            m5, m6 = self.pipeline.get()
            # Добавление задачи 'K' в словарь, инициализация потока
            self.tasks.update({'K': threading.Thread(target=self.task_k, args=(m1, m2, m3, m4, m5, m6), name='K')})
            # Активируем критическую сессию
            with self.lock:
                # Добавляем в список log информацию о вызове потока 'K'
                self.log.append(f'{datetime.datetime.now().time()}: Задача "H" запустила задачу "K"')
            # Запускаем задачу 'K'
            self.tasks['K'].start()
        else:
            # Так как задача 'H'  не завершается первой, то добавим списки m1, m2 в очередь
            self.pipeline.put((m1, m2))
        with self.lock:
            # Добавляем в переменную log инфомрацию о том, что поток 'H' завершён
            self.log.append(f'{datetime.datetime.now().time()}: Задача "H" была завершена')

    def task_k(self, m1, m2, m3, m4, m5, m6):
        # Активируем критическую сессию
        with self.lock:
            # Добавляем в список log информацию о запуске потока 'K'
            self.log.append(f'{datetime.datetime.now().time()}: Задача "K" была запущена')
        # Умножаем каждый элемент списка m1 на случайные integer заданного размере
        m1 = [number * random.randint(0, 2 ** 4) for number in m1 + m3 + m5]
        # Выполняем логичское умножение каждый элемент списка m2 на случайные boolean
        m2 = [boolean and bool(random.getrandbits(1)) for boolean in m2 + m4 + m6]
        with self.lock:
            # Добавляем в переменную log инфомрацию о том, что поток 'K' завершён
            self.log.append(f'{datetime.datetime.now().time()}: Задача "K" была завершена')

    def get_active_thread(self):
        return [task.name for task in self.tasks.values() if task.is_alive()]
