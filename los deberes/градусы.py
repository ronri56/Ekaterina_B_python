

def is_number(a):
    try:
        float(a)
        return True
    except ValueError:
        return False


temperature = input('Введите температуру в градусах Цельсия или Фаренгейта (прим. 12C или 100F): ')

scale = temperature[:-1]
degrees = temperature[-1]

if degrees in ['c', 'C', 'с', 'С', 'f', 'F'] and is_number(scale) == True:
    scale = float(scale)

    if degrees in ['f', 'F', 'ф', 'Ф']:
        temp_c = (scale - 32) * 5 / 9
        print(temp_c, 'C')

    elif degrees in ['c', 'C', 'с', 'С']:
        temp_f = (scale * 9 / 5) + 32
        print(temp_f, 'F')

else:
    print('Ввод некорректный. Попробуйте еще раз')