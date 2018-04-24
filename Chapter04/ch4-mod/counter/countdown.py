def count_down(max):
    numbers = [i for i in range(max)]
    for num in numbers[::-1]:
        print(num, end=', ')
