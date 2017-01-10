import timeit

#1
print(timeit.timeit(stmt = """\
a = [0, 1, 2, 3]
number = 3
a.pop(number)
"""))

#2
print(timeit.timeit(stmt = """\
a = [0, 1, 2, 3]
number = None
if number:
    a.pop(number)
else:
    a.pop()
""", number = 1000000))

#Result: 1~=2