import glob
import os
import zipfile


def unzipping(): #разархивирование скачанного архива
    for i in os.scandir('zipfiles/'):
        path_to_zip_file = i
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall('unzipped/')
            print(f'{i} разархивирован')


def clear_zipfiles():  #очистка директории от распакованных архивов
    files = glob.glob('zipfiles/*.zip', recursive=True)

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
        print(f'Файл {f} удален')