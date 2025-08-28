import os

def func():
    current_dir = os.path.dirname(__file__)  # Используйте file для получения имени текущего файла
    print(current_dir)

if __name__ == "__main__":  # Правильная проверка главного модуля
    func()