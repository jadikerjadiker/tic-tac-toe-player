def foo(first, second, third = None, fourth = 1):
    print(first)
    print(second)
    print(third)
    print(fourth)
    
a = [1, 3]
b = {"third": 4}
foo(*a, **b)