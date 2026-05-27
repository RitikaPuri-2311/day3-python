
# TOPIC: Lists
# Covers: methods, comprehensions, nested lists, slicing,
#         shallow vs deep copy, list vs tuple

import copy


# 1. Creating Lists

empty   = []
nums    = [1, 2, 3, 4, 5]
mixed   = [1, "hello", 3.14, True, None]
nested  = [[1, 2], [3, 4], [5, 6]]

# list() constructor
from_range  = list(range(1, 11))        # [1, 2, 3, ..., 10]
from_string = list("hello")             # ['h', 'e', 'l', 'l', 'o']
from_tuple  = list((1, 2, 3))           # [1, 2, 3]


# 2.List Methods

fruits = ["apple", "banana", "cherry"]

# append — add ONE item to the end  O(1)
fruits.append("date")
print(fruits)   # ['apple', 'banana', 'cherry', 'date']

# extend — add ALL items from iterable to the end  O(k)
fruits.extend(["elderberry", "fig"])
print(fruits)   # ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig']

# insert — insert at specific index  O(n)
fruits.insert(1, "avocado")   # insert at index 1
print(fruits)   #['apple', 'avocado', 'banana', 'cherry', 'date', 'elderberry', 'fig']

# remove — removes FIRST occurrence by VALUE, raises ValueError if absent  O(n)
fruits.remove("banana")
print(fruits)  # ['apple', 'avocado', 'cherry', 'date', 'elderberry', 'fig']

# pop — remove & return item by INDEX (default: last)  O(1) for last, O(n) otherwise
last  = fruits.pop()       # removes last
first = fruits.pop(0)      # removes first
print(last, first) # fig apple
print(fruits)      # ['avocado', 'cherry', 'date', 'elderberry']

# index — find index of first occurrence, raises ValueError if absent  O(n)
nums = [10, 20, 30, 20, 40]
print(nums.index(20))       # 1  (first occurrence)

# count — count occurrences  O(n)
print(nums.count(20))       # 2

# sort — IN-PLACE sort (modifies list, returns None)  O(n log n)
letters = ["banana", "apple", "cherry", "date"]
letters.sort()
print(letters)              # alphabetical
letters.sort(reverse=True)
print(letters)              # reverse alphabetical
letters.sort(key=len)       # sort by length
print(letters)

# reverse — IN-PLACE reverse  O(n)
nums = [1, 2, 3, 4, 5]
nums.reverse()
print(nums)                 # [5, 4, 3, 2, 1]

# copy — shallow copy  O(n)
original = [1, 2, 3]
copied   = original.copy()
copied.append(99)
print(original)             # [1, 2, 3] — unaffected
print(copied)               # [1, 2, 3, 99]

# clear — remove all items  O(n)
temp = [1, 2, 3]
temp.clear()
print(temp)                 # []



# 3. Slicing  — list[start:stop:step]
#    start inclusive, stop exclusive, step default 1

nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(nums[2:5])        # [2, 3, 4]       — indices 2,3,4
print(nums[:4])         # [0, 1, 2, 3]    — from beginning
print(nums[6:])         # [6, 7, 8, 9]    — to end
print(nums[::2])        # [0, 2, 4, 6, 8] — every 2nd element
print(nums[1::2])       # [1, 3, 5, 7, 9] — every 2nd starting at 1
print(nums[::-1])       # [9,...,0]        — reversed 
print(nums[7:2:-1])     # [7, 6, 5, 4, 3] — reversed slice

# Slice assignment
nums[2:5] = [20, 30, 40]
print(nums)             # [0, 1, 20, 30, 40, 5, 6, 7, 8, 9]

# Delete a slice
del nums[2:5]
print(nums)             # [0, 1, 5, 6, 7, 8, 9]



# 4. List Comprehensions — [expression for item in iterable if condition]
#    Faster and more readable than equivalent for loop

squares  = [x**2 for x in range(10)]
print(squares)

evens    = [x for x in range(20) if x % 2 == 0]
print(evens)

# Transformation + filtering together
words    = ["hello", "world", "python", "rocks", "hi"]
long_upper = [w.upper() for w in words if len(w) > 3]
print(long_upper)       # ['HELLO', 'WORLD', 'PYTHON', 'ROCKS']

# Nested comprehension — flatten 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat   = [num for row in matrix for num in row]
print(flat)             # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 2D comprehension — create matrix
grid = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(grid)             # [[1,2,3],[2,4,6],[3,6,9]]

# With function call
import os
py_files = [f for f in ["a.py", "b.txt", "c.py", "d.md"] if f.endswith(".py")]
print(py_files)




# 3x3 matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

# Access: matrix[row][col]
print(matrix[1][2])     # 6  (row 1, col 2)

# Traverse
for row in matrix:
    for val in row:
        print(val, end=" ")
    print()

# Transpose (swap rows and cols)
transposed = [[row[i] for row in matrix] for i in range(3)]
print(transposed)       # [[1,4,7],[2,5,8],[3,6,9]]
# Pythonic equivalent:
transposed2 = list(map(list, zip(*matrix)))
print(transposed2)



# 6. Shallow vs Deep Copy
#
#   Shallow copy: copies the outer list, but INNER objects are still shared.
#   Deep copy:    recursively copies everything — fully independent.


# Shallow copy — problem with mutable inner objects
original = [[1, 2, 3], [4, 5, 6]]
shallow  = original.copy()         # or list(original) or original[:]

shallow[0].append(99)               # modifying inner list
print(original)   # [[1, 2, 99], [4, 5, 6]]  ← AFFECTED — same inner objects
print(shallow)    # [[1, 2, 99], [4, 5, 6]]

# Deep copy — fully independent
original = [[1, 2, 3], [4, 5, 6]]
deep     = copy.deepcopy(original)

deep[0].append(99)
print(original)   # [[1, 2, 3], [4, 5, 6]]  ← NOT affected
print(deep)       # [[1, 2, 99], [4, 5, 6]]

# Rule of thumb:
#   Flat list of immutables → .copy() or [:] is fine
#   List containing lists/dicts/objects → use copy.deepcopy()



# 7. List vs Tuple — when to use which
#
#   LIST:  mutable — use when collection will CHANGE (add/remove items)
#   TUPLE: immutable — use when collection is FIXED (coordinates, RGB, DB row)
#
#   Tuples are:
#     • faster to create and iterate
#     • hashable (can be dict keys / set members) if contents are hashable
#     • convey intent: "this should not change"


# Tuple — fixed, hashable
point      = (3.0, 4.0)
rgb_red    = (255, 0, 0)
db_record  = ("Alice", 30, "alice@example.com")

# Can be used as dict key
color_names = {(255, 0, 0): "red", (0, 255, 0): "green"}
print(color_names[(255, 0, 0)])     # red

# List — dynamic
shopping_cart = ["apple", "milk"]
shopping_cart.append("bread")
shopping_cart.remove("milk")

# Unpacking works on both
x, y     = point
name, age, email = db_record

print(f"Point: ({x}, {y}), Name: {name}, Age: {age}")



# 8. Useful Built-ins that work with lists


nums = [3, 1, 4, 1, 5, 9, 2, 6]

print(min(nums))          # 1
print(max(nums))          # 9
print(sum(nums))          # 31
print(len(nums))          # 8
print(sorted(nums))       # new sorted list — does NOT modify original
print(list(reversed(nums)))  # reversed iterator → list

# any / all
print(any(x > 8 for x in nums))   # True (9 > 8)
print(all(x > 0 for x in nums))   # True (all positive)

# zip — iterate two lists together
names  = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"  {name}: {score}")

# enumerate — get index and value
for i, name in enumerate(names, start=1):
    print(f"  {i}. {name}")

print("\nlists.py complete.")