from collections import Counter
list = ["a","A","a","c","m","x","X","c"]
dic = Counter(list)
print(dic)

list1 = ["a", "a", "a", "b", "c", "f", "g", "g", "c", "11", "g", "f", "10", "2"]
print(Counter(list1).most_common(3))
