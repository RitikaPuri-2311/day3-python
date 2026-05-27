# TOPIC: Sorting & Searching
# Covers: sorted() vs .sort(), key=, lambda keys, multi-key sort,
#         bisect module, linear vs binary search complexity

import bisect
import time
import random


# 1. sorted() vs list.sort()
#
#   sorted(iterable, key=..., reverse=False)
#     → returns a NEW list, works on ANY iterable, original unchanged
#
#   list.sort(key=..., reverse=False)
#     → modifies list IN-PLACE, returns None, only works on lists
#
#   Both use Timsort: O(n log n) time, O(n) space, STABLE sort
#   (equal elements keep their original relative order)

nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

# sorted — non-destructive
sorted_nums = sorted(nums)
print(sorted_nums)  # [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
print(nums)         # [3, 1, 4, 1, 5, 9, 2, 6, 5, 3] — unchanged

# .sort — in-place
nums.sort()
print(nums)         # [1, 1, 2, 3, 3, 4, 5, 5, 6, 9] — changed

# sorted works on any iterable (tuple, set, generator, string)
print(sorted("hello"))          # ['e', 'h', 'l', 'l', 'o']
print(sorted({3, 1, 4, 1, 5})) # [1, 3, 4, 5]  (deduped by set first)
print(sorted((5, 2, 8, 1)))     # [1, 2, 5, 8]

# Reverse sort
print(sorted(nums, reverse=True))


# 2. key= parameter — the heart of custom sorting
#
#   key is a callable applied to each element BEFORE comparison.
#   Python sorts by the RETURN VALUE of key, not the element itself.
#   The key function is called ONCE per element (efficient).

words = ["banana", "apple", "fig", "cherry", "date", "elderberry"]

# Sort by length
by_length = sorted(words, key=len)
print(by_length)        # ['fig', 'date', 'apple', 'banana', 'cherry', 'elderberry']

# Sort by last character
by_last = sorted(words, key=lambda w: w[-1])
print(by_last)

# Sort case-insensitively
mixed_case = ["Banana", "apple", "Cherry", "date"]
print(sorted(mixed_case))                        # uppercase before lowercase
print(sorted(mixed_case, key=str.lower))         # true alphabetical

# Sort by string length, then alphabetically (stable sort preserves secondary)
print(sorted(words, key=lambda w: (len(w), w)))  # length first, then alpha


# 3. Sorting Objects / Dicts

people = [
    {"name": "Charlie", "age": 30, "score": 85},
    {"name": "Alice",   "age": 25, "score": 92},
    {"name": "Bob",     "age": 25, "score": 88},
    {"name": "Diana",   "age": 28, "score": 85},
]

# Sort dicts by single field
by_age   = sorted(people, key=lambda p: p["age"])
by_score = sorted(people, key=lambda p: p["score"], reverse=True)
print([p["name"] for p in by_age])      # youngest first
print([p["name"] for p in by_score])    # highest score first

# Multi-key sort: primary = age, secondary = name (for ties)
by_age_name = sorted(people, key=lambda p: (p["age"], p["name"]))
for p in by_age_name:
    print(f"  {p['name']}: age={p['age']}, score={p['score']}")

# Sort by DESCENDING score, then ASCENDING name for ties
# Use negation for numeric descending: -p["score"]
complex_sort = sorted(
    people,
    key=lambda p: (-p["score"], p["name"])
)
for p in complex_sort:
    print(f"  {p['name']}: {p['score']}")


# Sorting dataclass / namedtuple instances
from collections import namedtuple
Student = namedtuple("Student", ["name", "gpa", "year"])
students = [
    Student("Alice", 3.9, 3),
    Student("Bob",   3.7, 2),
    Student("Carol", 3.9, 2),
    Student("Dan",   3.5, 4),
]

# Sort by gpa descending, then year ascending
sorted_students = sorted(students, key=lambda s: (-s.gpa, s.year))
for s in sorted_students:
    print(f"  {s.name}: GPA={s.gpa}, year={s.year}")


# 4. operator module — faster than lambda for attribute/key access

from operator import itemgetter, attrgetter

# itemgetter for dicts (faster than lambda)
by_score_op = sorted(people, key=itemgetter("score"), reverse=True)
print([p["name"] for p in by_score_op])

# Multiple keys with itemgetter
by_age_score = sorted(people, key=itemgetter("age", "score"))
print([p["name"] for p in by_age_score])

# attrgetter for objects/namedtuples
by_gpa = sorted(students, key=attrgetter("gpa"), reverse=True)
print([s.name for s in by_gpa])


# 5. Linear Search vs Binary Search
#
#   Linear Search: check every element  →  O(n)
#   Binary Search: divide sorted list   →  O(log n)
#     Requirement: list must be SORTED

def linear_search(lst: list, target) -> int:
    """Return index of target, or -1 if not found. O(n)."""
    for i, val in enumerate(lst):
        if val == target:
            return i
    return -1

def binary_search(lst: list, target) -> int:
    """Return index of target in SORTED list, or -1. O(log n)."""
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            lo = mid + 1        # target is in right half
        else:
            hi = mid - 1        # target is in left half
    return -1

data = sorted(random.sample(range(1_000_000), 100_000))

# Performance comparison
target = data[50_000]   # guaranteed to exist

start = time.perf_counter()
for _ in range(100):
    linear_search(data, target)
linear_time = time.perf_counter() - start

start = time.perf_counter()
for _ in range(100):
    binary_search(data, target)
binary_time = time.perf_counter() - start

print(f"\nLinear search (100 runs): {linear_time*1000:.2f}ms")
print(f"Binary search (100 runs): {binary_time*1000:.2f}ms")
print(f"Binary is ~{linear_time/binary_time:.0f}x faster")


# 6. bisect — binary search in the standard library
#   bisect.bisect_left(a, x)  → index where x would be inserted (left of equal)
#   bisect.bisect_right(a, x) → index where x would be inserted (right of equal)
#   bisect.insort(a, x)       → insert x into a maintaining sorted order  O(n)
#
#   Finding the position is O(log n), but insort is O(n) due to list shift.

sorted_list = [1, 3, 5, 7, 9, 11, 13, 15]

# Find insertion point
pos_left  = bisect.bisect_left(sorted_list, 7)    # 3  (before existing 7)
pos_right = bisect.bisect_right(sorted_list, 7)   # 4  (after existing 7)
print(f"\nbisect_left(7):  {pos_left}")
print(f"bisect_right(7): {pos_right}")

# Check if element exists
def contains_binary(sorted_lst, target) -> bool:
    idx = bisect.bisect_left(sorted_lst, target)
    return idx < len(sorted_lst) and sorted_lst[idx] == target

print(contains_binary(sorted_list, 7))    # True
print(contains_binary(sorted_list, 6))    # False

# Insert while maintaining sort order
bisect.insort(sorted_list, 6)
bisect.insort(sorted_list, 10)
print(sorted_list)    # [1, 3, 5, 6, 7, 9, 10, 11, 13, 15]

# Grade boundaries — classic bisect use case
breakpoints = [60, 70, 80, 90]
grades      = ["F", "D", "C", "B", "A"]

def letter_grade(score):
    return grades[bisect.bisect(breakpoints, score)]

for score in [45, 62, 75, 88, 95]:
    print(f"  {score} → {letter_grade(score)}")

# Count elements in a range [lo, hi] using bisect — O(log n)
data = sorted([1, 1, 2, 3, 3, 3, 4, 5, 5, 6, 7, 7, 8])
lo, hi = 3, 6
count = bisect.bisect_right(data, hi) - bisect.bisect_left(data, lo)
print(f"\nElements in [{lo}, {hi}]: {count}")  # 3+3+4+5+5+6 → 6 elements

