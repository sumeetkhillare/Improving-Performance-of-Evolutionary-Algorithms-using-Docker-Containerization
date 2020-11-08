try:
    print('enter space seprated numbers to sort')
    inp = list(map(int,input().split()))
    inp.sort()
    print(inp)
except EOFError:
    pass     
