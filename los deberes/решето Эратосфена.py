
try:
    n = int(input('Введите N: '))

    if n < 1:
        print('Введите натуральное число.')
    else:
        a = [i for i in range(n + 1)]
        a[1] = 0

        i = 2
        while i ** 2 <= n:
            if a[i] != 0:
                j = i ** 2
                while j <= n:
                    a[j] = 0
                    j += i
            i += 1

        for i in range(2, n + 1):
            if a[i] != 0:
                print(a[i])

except ValueError:
    print('Необходимо ввести целое число.')

