def fun1(that, other):
    that[1] = 99
    other[1] = 99

if __name__ == '__main__':
    ages = (4, 5, 6)
    grades = [10, 11]
    fun1(ages, grades)
    print(ages, grades)