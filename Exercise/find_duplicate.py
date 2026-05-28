# find duplicates in list and tuple
from collections import Counter

list1 = [2, 4, 6, 8, 2, 4]
list2 = ["Tiger", "Lion", "Tiger", "Elephant", "Giraffe", "Giraffe"]

tuple1 = (2, 4, 6, 8, 2, 4)
tuple2 = ("Tiger", "Lion", "Tiger", "Elephant", "Giraffe", "Giraffe")


def find_duplicates(iter):
    result = []
    for element, count in Counter(iter).items():
        if count > 1:
            result.append(element)

    return result


# print(Counter(list1).items())
print(find_duplicates(list1))
print(find_duplicates(tuple1))
print(find_duplicates(list2))
print(find_duplicates(tuple2))
