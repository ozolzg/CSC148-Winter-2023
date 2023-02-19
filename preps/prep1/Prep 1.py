# 2
n = 14
n2 = n
n = 15
print(n, n2)

# 1 줄 끝나면 n = 14
# 2 줄 끝나면 n = 14, n2 = 14
# 3줄 끝나면 n = 15 n2 = 14

# 4
s = 'hello'
s2 = s
s = s[2:]
print(s, s2)

# 7
x = [1, 2, 3]
y = x
y[1] = 100
print(x, y)

# 13
one = [0, 1, 2, 3, 4, 5, 6, 7]
two = one
one = one[1:5]
print(one, two)

# 14
a = [1, 2, 3, 4, 2, 9, 6]
b = [1, 2, 3, 4, 2, 9, 6]
a.remove(2)
print(a, b)

# 15
temp = 18
L = [9, temp, 27]
temp = 99
print(L)

# 17
nested_list = [[1, 2], [3, 4]]
second_list = nested_list[1]
second_list[1] = -1
first_element = nested_list[0][0]
first_element = -1
print(nested_list[0][0], nested_list[1][1])