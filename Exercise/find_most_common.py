#find the most common element in a list 

from collections import Counter

list = ["Cup", "Cup", "Cup", "Coffee", "Coffee", "Tea"]

l1 = Counter(list)
result = l1.most_common()
print(result)
result2 = l1.most_common(1)
print(result2)

result3 = Counter("elephantinzoo").most_common(2)
print(result3)