# TOPIC: Sets & Tuples
# Covers: set operations, frozenset, tuple immutability,
#         namedtuple, when to use each

from collections import namedtuple


# SETS

# 1. Creating Sets
#    Sets: UNORDERED, NO duplicates, O(1) lookup

empty_set  = set()                  # NOT {} — that's an empty dict!
nums       = {1, 2, 3, 4, 5}
from_list  = set([1, 2, 2, 3, 3, 3])   # duplicates removed → {1, 2, 3}
from_str   = set("abracadabra")         # unique chars → {'a','b','r','c','d'}

print(from_list)    # {1, 2, 3}
print(from_str)     # {'a', 'b', 'c', 'd', 'r'} (order not guaranteed)

# Sets only hold HASHABLE items — no lists or dicts inside
valid   = {1, "hello", (1, 2), 3.14}
# invalid = {[1, 2]}  ← TypeError: unhashable type: 'list'


# 2. Set Methods

s = {1, 2, 3}

s.add(4)                    # add one element
s.update([5, 6], {7, 8})    # add multiple (from any iterable)
s.discard(99)               # remove if present — no error if absent
s.remove(1)                 # remove — raises KeyError if absent
popped = s.pop()            # remove & return an arbitrary element

print(s)


# 3. Set Operations  — the real power of sets

a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}

# Union — elements in A OR B (or both)
print(a | b)                    # {1, 2, 3, 4, 5, 6, 7}
print(a.union(b))               # same

# Intersection — elements in BOTH A AND B
print(a & b)                    # {3, 4, 5}
print(a.intersection(b))

# Difference — elements in A but NOT in B
print(a - b)                    # {1, 2}
print(a.difference(b))

# Symmetric Difference — elements in A OR B, but NOT both
print(a ^ b)                    # {1, 2, 6, 7}
print(a.symmetric_difference(b))

# Subset / Superset checks
small = {3, 4}
print(small.issubset(a))        # True  — all of small is in a
print(a.issuperset(small))      # True  — a contains all of small
print(a.isdisjoint({8, 9}))     # True  — no elements in common

# In-place operations (mutate a)
a |= {10}       # a.update({10})
a &= b          # keep only common elements
a -= {3}        # remove elements also in b
a ^= {4, 5}     # toggle


# 4. Practical Use Cases for Sets

# Remove duplicates from a list (order lost!)
names_with_dupes = ["Alice", "Bob", "Alice", "Charlie", "Bob"]
unique_names = list(set(names_with_dupes))
print(sorted(unique_names))     # ['Alice', 'Bob', 'Charlie']

# Fast membership test — O(1) vs list's O(n)
valid_statuses = {"active", "inactive", "pending", "suspended"}
status = "active"
if status in valid_statuses:    # O(1) lookup
    print("valid status")

# Find common elements between two sequences
team_a = {"Alice", "Bob", "Charlie"}
team_b = {"Charlie", "Diana", "Eve"}
both   = team_a & team_b
only_a = team_a - team_b
print(f"In both: {both}")       # {'Charlie'}
print(f"Only A:  {only_a}")     # {'Alice', 'Bob'}


# 5. frozenset — immutable set
#    Like a set but CANNOT be modified after creation.
#    Can be used as a dict key or stored in another set.

fs = frozenset([1, 2, 3, 4])
# fs.add(5)   ← AttributeError: 'frozenset' has no 'add'

# Useful as dict keys
permissions = {
    frozenset({"read"}):              "read-only",
    frozenset({"read", "write"}):     "editor",
    frozenset({"read", "write", "admin"}): "admin",
}
user_perms = frozenset({"read", "write"})
print(permissions.get(user_perms))   # editor

# Nested set (set of frozensets)
graph_edges = {frozenset({1, 2}), frozenset({2, 3}), frozenset({1, 3})}
print(frozenset({1, 2}) in graph_edges)  # True


# TUPLES

# 6. Tuple Basics — immutable, ordered, allows duplicates, hashable

empty   = ()
single  = (42,)             # trailing comma required for single-element!
not_single = (42)           # this is just the int 42, NOT a tuple
coords  = (3.0, 4.0)
rgb     = (255, 128, 0)
record  = ("Alice", 30, "alice@example.com", True)

print(type(single))         # <class 'tuple'>
print(type(not_single))     # <class 'int'>

# Tuples are sequences — same indexing/slicing as lists
print(record[0])            # Alice
print(record[-1])           # True
print(record[1:3])          # (30, 'alice@example.com')

# Immutability
# record[0] = "Bob"  ← TypeError: 'tuple' object does not support item assignment

# But if a tuple CONTAINS a mutable object, that object can still change:
mutable_inside = ([1, 2], [3, 4])
mutable_inside[0].append(99)    # OK — the list changed, tuple ref didn't
print(mutable_inside)           # ([1, 2, 99], [3, 4])


# 7. Tuple Operations

t = (1, 2, 3, 4, 5)

print(len(t))       # 5
print(t.count(3))   # 1
print(t.index(4))   # 3
print(3 in t)       # True
print(t + (6, 7))   # (1, 2, 3, 4, 5, 6, 7)  — creates new tuple
print(t * 2)        # (1, 2, 3, 4, 5, 1, 2, 3, 4, 5)

# Tuple unpacking — very Pythonic
x, y         = (10, 20)
a, b, *rest  = (1, 2, 3, 4, 5)     # extended unpacking
first, *mid, last = (1, 2, 3, 4, 5)

print(a, b, rest)               # 1 2 [3, 4, 5]
print(first, mid, last)         # 1 [2, 3, 4] 5

# Swap variables without temp — Python's tuple packing/unpacking
x, y = 5, 10
x, y = y, x
print(x, y)         # 10 5

# Function returning multiple values (actually returns a tuple)
def min_max(nums):
    return min(nums), max(nums)   # returns (min, max) tuple

lo, hi = min_max([3, 1, 4, 1, 5, 9])
print(lo, hi)       # 1 9


# 8. namedtuple — tuple with field names
#    Like a lightweight class: immutable, memory-efficient, readable

# Define
Point  = namedtuple("Point", ["x", "y"])
Person = namedtuple("Person", ["name", "age", "email"])
Color  = namedtuple("Color", "red green blue")   # space-separated string also works

# Create instances
p = Point(3.0, 4.0)
a = Person("Alice", 30, "alice@example.com")
c = Color(255, 128, 0)

# Access by NAME (readable) or INDEX (tuple-compatible)
print(p.x, p.y)                 # 3.0  4.0
print(p[0], p[1])               # 3.0  4.0

print(a.name, a.age)            # Alice 30
print(f"{c.red}, {c.green}, {c.blue}")  # 255, 128, 0

# Still a proper tuple
print(isinstance(p, tuple))     # True
print(p._asdict())              # OrderedDict([('x', 3.0), ('y', 4.0)])

# _replace — create new instance with some fields changed
b = a._replace(age=31, email="alice@new.com")
print(b)

# Use as dict key (hashable!)
visited = {Point(0, 0): "origin", Point(1, 0): "right"}
print(visited[Point(0, 0)])

# Practical: CSV/DB rows with field names
Row = namedtuple("Row", ["id", "name", "score"])
rows = [Row(1, "Alice", 95), Row(2, "Bob", 87), Row(3, "Carol", 92)]

top = max(rows, key=lambda r: r.score)
print(f"Top scorer: {top.name} with {top.score}")


# 9. When to Use Each — Summary
#
#   LIST   — mutable, ordered, allows duplicates
#            use when: collection changes, need ordering, items can repeat
#            e.g. shopping cart, task queue, results from a query
#
#   TUPLE  — immutable, ordered, allows duplicates, hashable
#            use when: data is fixed, need dict key, function returns multiple values
#            e.g. coordinates, RGB color, function return, DB record row
#
#   SET    — mutable, unordered, NO duplicates, O(1) lookup
#            use when: uniqueness matters, fast membership test, set math needed
#            e.g. unique tags, permission checks, deduplication
#
#   FROZENSET — immutable set
#            use when: need a hashable set (dict key, stored in another set)
#
#   NAMEDTUPLE — immutable tuple with field names
#            use when: structured data, want readability of class without overhead
#            e.g. config records, CSV rows, geometry points

