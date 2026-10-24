import time, random

again = 1
computer = random.randint(1,51)

while again == 1:
    # print(computer)
    print('Комьютер загадал число, попытайтесь его отгадать')

    user = int(input('Теперь угадывайте! Введите число от 1 до 50: ', ))

    if user == computer:
        print("Ура, вы выиграли!")
        again = int(input('Хотите сыграть еще раз? Если да, введите 1, если нет, введите 0: '))
        if again == 1:
            computer = random.randint(1,51)
            continue
        else:
            break

    elif user > computer:
        print("Вы проиграли:( Загаданное число меньше")
    elif user < computer:
        print("Вы проиграли:( Загаданное число больше")
    
    

    