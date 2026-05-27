# TOPIC: Dictionaries
# Covers: methods, comprehensions, nested dicts, defaultdict,
#         OrderedDict, Counter, merging dicts

from collections import defaultdict, OrderedDict, Counter

# 1. Creating Dictionaries

empty      = {}
person     = {"name": "Alice", "age": 30, "city": "Delhi"}
from_pairs = dict([("a", 1), ("b", 2), ("c", 3)])
from_keys  = dict.fromkeys(["x", "y", "z"], 0)   # all values = 0
print(from_keys)   # {'x': 0, 'y': 0, 'z': 0}

# Dict literal vs dict() constructor
d1 = {"key": "value"}
d2 = dict(key="value")   # only works for string keys


# 2. Core Dict Methods

user = {"name": "Bob", "age": 25, "email": "bob@example.com"}

# get — safe access with optional default (never raises KeyError)
print(user.get("name"))             # Bob
print(user.get("phone"))            # None
print(user.get("phone", "N/A"))     # N/A

# setdefault — return value if key exists, ELSE insert default and return it
user.setdefault("role", "viewer")
print(user["role"])                 # viewer
user.setdefault("role", "admin")    # key exists — NOT overwritten
print(user["role"])                 # still viewer

# update — merge another dict or keyword args INTO this dict  (mutates)
user.update({"age": 26, "city": "Mumbai"})
user.update(phone="9876543210")
print(user)

# pop — remove and return value by key; optional default if absent
age = user.pop("age")
print(age)                          # 26
na  = user.pop("missing", None)     # no KeyError
print(na)                           # None

# keys / values / items — view objects (live, reflect changes)
for key in user.keys():
    print(key)   # name, email, city, phone, role

for value in user.values():
    print(value) # Bob, bob@example.com, Mumbai, 9876543210, viewer]

for key, value in user.items():     # most useful for iteration
    print(f"  {key}: {value}")

# in operator — checks keys, O(1)
print("name" in user)               # True
print("salary" in user)             # False

# del
del user["phone"]

# len
print(len(user))


# 3. Dict Comprehensions — {key_expr: val_expr for item in iterable if cond}

squares = {x: x**2 for x in range(1, 6)}
print(squares)      # {1:1, 2:4, 3:9, 4:16, 5:25}

# Invert a dict (swap keys and values)
original  = {"a": 1, "b": 2, "c": 3}
inverted  = {v: k for k, v in original.items()}
print(inverted)     # {1:'a', 2:'b', 3:'c'}

# Filter a dict
prices    = {"apple": 50, "banana": 20, "cherry": 120, "date": 80}
expensive = {k: v for k, v in prices.items() if v > 50}
print(expensive)    # {'cherry': 120, 'date': 80}

# Normalize keys to lowercase
raw    = {"Name": "Alice", "AGE": 30, "City": "Delhi"}
clean  = {k.lower(): v for k, v in raw.items()}
print(clean)        # {'name': 'Alice', 'age': 30, 'city': 'Delhi'}


# 4. Nested Dicts

users_db = {
    "u001": {"name": "Alice", "roles": ["admin", "editor"], "active": True},
    "u002": {"name": "Bob",   "roles": ["viewer"],          "active": False},
}

# Access
print(users_db["u001"]["name"])          # Alice
print(users_db["u001"]["roles"][0])      # admin

# Safe access with nested get
role = users_db.get("u003", {}).get("name", "unknown")
print(role)                              # unknown (u003 doesn't exist)

# Updating nested value
users_db["u002"]["active"] = True
users_db["u001"]["roles"].append("viewer")

# Traversing nested dicts
for uid, data in users_db.items():
    roles = ", ".join(data["roles"])
    print(f"  {uid}: {data['name']} | roles: {roles}")


# 5. defaultdict — never get KeyError for missing keys
#    Automatically creates a default value using the factory function

# Regular dict — KeyError on missing key
# d = {}; d["a"] += 1  → KeyError!

# defaultdict(int)  — missing keys default to 0
word_count = defaultdict(int)
sentence = "the cat sat on the mat the cat"
for word in sentence.split():
    word_count[word] += 1                # no KeyError — starts at 0

print(dict(word_count))
# {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}

# defaultdict(list) — missing keys default to []
groups = defaultdict(list)
people = [("engineering", "Alice"), ("marketing", "Bob"),
          ("engineering", "Charlie"), ("marketing", "Diana")]

for dept, name in people:
    groups[dept].append(name)            # no KeyError — starts with []

print(dict(groups))
# {'engineering': ['Alice', 'Charlie'], 'marketing': ['Bob', 'Diana']}

# defaultdict(set) — missing keys default to set()
tags = defaultdict(set)
tags["python"].add("language")
tags["python"].add("backend")
tags["rust"].add("language")
print(dict(tags))


# 6. Counter — count occurrences of elements

text  = "abracadabra"
c     = Counter(text)
print(c)                        # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# most_common(n) — top n most frequent
print(c.most_common(3))         # [('a', 5), ('b', 2), ('r', 2)]

# Counter arithmetic
c1 = Counter("aab")
c2 = Counter("abc")
print(c1 + c2)                  # add counts
print(c1 - c2)                  # subtract (drops negatives)
print(c1 & c2)                  # intersection (min counts)
print(c1 | c2)                  # union (max counts)

# Count words
words   = "the quick brown fox jumps over the lazy dog the fox".split()
wc      = Counter(words)
print(wc.most_common(3))        # top 3 words


# 7. OrderedDict — dict that remembers insertion order

od = OrderedDict()
od["first"]  = 1
od["second"] = 2
od["third"]  = 3

od.move_to_end("first")          # move to end
od.move_to_end("third", last=False)  # move to front

for key, val in od.items():
    print(f"  {key}: {val}")

# OrderedDict equality cares about order, regular dict doesn't
print({"a": 1, "b": 2} == {"b": 2, "a": 1})                          # True
print(OrderedDict([("a",1),("b",2)]) == OrderedDict([("b",2),("a",1)]))  # False


# 8. Merging Dicts

defaults = {"theme": "light", "lang": "en",  "debug": False}
user_cfg  = {"theme": "dark",  "timeout": 30}

# Method 1: {**d1, **d2}  — later keys win  (Python 3.5+)
merged1 = {**defaults, **user_cfg}
print(merged1)

# Method 2: d1 | d2  (Python 3.9+) — cleaner syntax
merged2 = defaults | user_cfg
print(merged2)

# In-place merge:  d1 |= d2  (Python 3.9+)
defaults |= user_cfg
print(defaults)

# Method 3: update (mutates d1)
d1 = {"a": 1, "b": 2}
d2 = {"b": 99, "c": 3}
d1.update(d2)
print(d1)      # {'a': 1, 'b': 99, 'c': 3}

