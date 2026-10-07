import time, random
print('Сейчас сыграем в угадайку! Комьютер загадывает число, а вы пытаетесь его отгадать')


computer = random.randint(1,100)
print("Компьютер загадывает число, подождите")

for i in range (1,6):
    print(".")
    time.sleep(1)

user = int(input('Теперь угадывайте! Введите число от 1 до 100: ', ))

if user == computer:
    print("Ура, вы выиграли!")
else:
    print("Вы проиграли:(")

