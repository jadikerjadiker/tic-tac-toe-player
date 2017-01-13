import timeit

'''
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
'''

#1
print(timeit.timeit(stmt = """\
a = random.choice([-1, 1])
if a==1:
    ans =  1
else:
    ans =  0
""", setup = "import random"))

#2
print(timeit.timeit(stmt = """\
a = random.choice([-1, 1])
ans = (a+1)//2
""", setup = "import random"))

#Result: 1~=2