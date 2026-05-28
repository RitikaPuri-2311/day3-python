list1 = [1, 2 , 3, 4]
list2 = [2, 4, 6, 8]

result = sorted(list1 + list2)  #method 1
print(result)                 

import heapq    

result2 = list(heapq.merge(list1, list2))   #method 2
print(result2)


from itertools import chain

result3 = sorted(chain(list1, list2))    #method 3
print(result3)

