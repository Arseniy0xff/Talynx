import os
import subprocess
from tqdm import tqdm

def list_ui_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.ui')]

def main():
    directory = 'ui_ui'
    directory_out = 'ui_py'
    os.makedirs(directory_out, exist_ok=True)

    ui_files = list_ui_files(directory)
    if not ui_files:
        print("В папке 'ui' нет файлов .ui.")
        return

    print("Найденные файлы .ui:")
    for idx, fname in enumerate(ui_files, start=1):
        print(f"\t{idx} - {fname}")

    tokens = input("Введите номера файлов для конвертации через пробел: ").split()
    if not tokens:
        print("Не введено ни одного номера.")
        return

    # Собираем корректные индексы
    valid_indices = []
    for token in tokens:
        try:
            i = int(token) - 1
            if 0 <= i < len(ui_files):
                valid_indices.append(i)
            else:
                print(f"Номер {token} вне диапазона, пропускаем")
        except ValueError:
            print(f"Неверный ввод '{token}', пропускаем")

    # Конвертация с отображением прогресса
    for i in tqdm(valid_indices, desc="Конвертация файлов", unit="файл"):
        src = os.path.join(directory, ui_files[i])
        dst = os.path.join(directory_out, ui_files[i].replace('.ui', '.py'))
        try:
            subprocess.run(['pyuic6', '-x', src, '-o', dst], check=True)
            tqdm.write(f"Успешно: {ui_files[i]} → {dst}")
        except subprocess.CalledProcessError:
            tqdm.write(f"Ошибка конвертации {ui_files[i]}")

if __name__ == "__main__":
    main()
