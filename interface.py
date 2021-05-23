import json
import eel
from classes import MultiThreadSimulator

# Объявляем переменную simulator глобально
simulator = None


@eel.expose
def get_active_thread_py():
    """Получение всех активных потоков"""
    # Получаем список активных потоков
    data = simulator.get_active_thread()
    # Отправляем результат в JSON формате
    return json.dumps(data)


@eel.expose
def get_program_log_py():
    """Получение лога программы"""
    # Получаем лог класса
    data = simulator.log
    # Отправляем результат в JSON формате
    return json.dumps(data, ensure_ascii=False)


@eel.expose
def execute_program_py():
    """Запуск моделирования"""
    global simulator
    # Инициализируем и запускаем  MultiThreadSimulator
    simulator = MultiThreadSimulator()
