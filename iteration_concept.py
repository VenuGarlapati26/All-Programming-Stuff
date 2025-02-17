mystr=("banana")
myit=iter(mystr)
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))


print("\n".join(map(next, [iter("apple")]*len("apple"))))