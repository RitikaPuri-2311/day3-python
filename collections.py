# TOPIC: The collections Module
# Covers: deque, namedtuple, Counter, defaultdict, ChainMap
#         and WHY to use them (complexity advantages)

from collections import deque, namedtuple, Counter, defaultdict, ChainMap
import time


# 1. deque (Double-Ended Queue)
#     append/appendleft  → O(1) 
#     pop/popleft        → O(1) 
#     Great for: queues, sliding windows, BFS, undo history

dq = deque([1, 2, 3, 4, 5])

# Add to both ends
dq.append(6)            # right end  → deque([1,2,3,4,5,6])
dq.appendleft(0)        # left end   → deque([0,1,2,3,4,5,6])
print(dq)

# Remove from both ends
right = dq.pop()        # remove right → 6
left  = dq.popleft()    # remove left  → 0
print(right, left)
print(dq)               # deque([1,2,3,4,5])

# Extend both ends
dq.extend([6, 7])           # from right
dq.extendleft([-2, -1, 0])  # from left (note: reverses order!)
print(dq)

# rotate — shift all elements by n positions
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)                # shift right by 2
print(dq)                   # deque([4, 5, 1, 2, 3])
dq.rotate(-2)               # shift left by 2
print(dq)                   # deque([1, 2, 3, 4, 5])

# maxlen — bounded deque (acts like a sliding window / LRU cache)
recent = deque(maxlen=3)
for i in range(6):
    recent.append(i)
    print(f"  added {i}: {recent}")
# Once full, adding from right drops from left (like a circular buffer)


# Real-world: BFS (Breadth-First Search) queue
def bfs(graph: dict, start: str) -> list:
    """BFS traversal using deque as an efficient queue."""
    visited = []
    queue   = deque([start])
    seen    = {start}

    while queue:
        node = queue.popleft()      # O(1) — key advantage over list.pop(0)
        visited.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return visited

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [], "E": [], "F": [],
}
print("\nBFS from A:", bfs(graph, "A"))   # ['A', 'B', 'C', 'D', 'E', 'F']


# Real-world: sliding window using deque
def sliding_window_max(nums: list, k: int) -> list:
    """Return max of each window of size k using a monotonic deque. O(n)."""
    result = []
    window = deque()    # stores INDICES, front = index of current max

    for i, val in enumerate(nums):
        # remove indices outside the window
        while window and window[0] < i - k + 1:
            window.popleft()
        # remove smaller values from back (they can never be the max)
        while window and nums[window[-1]] < val:
            window.pop()
        window.append(i)
        if i >= k - 1:
            result.append(nums[window[0]])

    return result

print("Sliding window max:", sliding_window_max([1,3,-1,-3,5,3,6,7], k=3))
# [3, 3, 5, 5, 6, 7]


# 2. Counter (already covered in dicts.py — key extras here)

# Counter from any iterable
words = "to be or not to be that is the question to be".split()
c = Counter(words)

print(f"\nCounter: {c}")
print(f"Most common 3: {c.most_common(3)}")
print(f"'to' appears: {c['to']} times")
print(f"'missing' appears: {c['missing']} times")  # 0, not KeyError

# Counter as a multiset — elements() returns each item repeated count times
print(list(c.elements())[:10])

# Update (add more counts) vs subtract (reduce counts)
c.update(["to", "be"])
c.subtract(["to"])
print(c.most_common(3))

# Total count
print(f"Total words: {sum(c.values())}")

# Convert back to regular dict
print(dict(c.most_common(3)))


# 3. defaultdict recap with practical patterns

# Group by — very common pattern
students = [
    {"name": "Alice",   "grade": "A"},
    {"name": "Bob",     "grade": "B"},
    {"name": "Charlie", "grade": "A"},
    {"name": "Diana",   "grade": "C"},
    {"name": "Eve",     "grade": "B"},
]

by_grade = defaultdict(list)
for s in students:
    by_grade[s["grade"]].append(s["name"])

for grade in sorted(by_grade):
    print(f"  Grade {grade}: {by_grade[grade]}")

# Inverted index
docs = {
    "doc1": ["python", "data", "analysis"],
    "doc2": ["python", "web", "flask"],
    "doc3": ["data", "science", "ml"],
}

index = defaultdict(set)
for doc_id, words in docs.items():
    for word in words:
        index[word].add(doc_id)

print(f"\nDocs with 'python': {index['python']}")   # {'doc1', 'doc2'}
print(f"Docs with 'data':   {index['data']}")       # {'doc1', 'doc3'}


# 4. ChainMap — multiple dicts as a single view
#    Lookups search dicts left-to-right; first hit wins.
#    Writes go to the FIRST dict only.
#    Great for: config layering, scope chains

# CLI args > env vars > defaults — classic priority chain
defaults   = {"debug": False, "port": 8000, "host": "localhost", "timeout": 30}
env_vars   = {"port": 9000, "timeout": 60}
cli_args   = {"port": 8080, "debug": True}

config = ChainMap(cli_args, env_vars, defaults)

print(f"\nport    : {config['port']}")      # 8080  (from cli_args — wins)
print(f"timeout : {config['timeout']}")    # 60    (from env_vars — wins)
print(f"host    : {config['host']}")       # localhost (only in defaults)
print(f"debug   : {config['debug']}")      # True  (from cli_args)

# Writes go to the first map only
config["new_key"] = "value"
print(f"cli_args after write: {cli_args}")   # contains new_key
print(f"defaults untouched:   {defaults}")

# Add a new scope (like entering a function scope)
local_scope = config.new_child({"local_var": 42})
print(f"local_var in child scope: {local_scope['local_var']}")
print(f"port still accessible:    {local_scope['port']}")

# Useful: get all unique keys across all dicts
print(f"\nAll config keys: {sorted(config.keys())}")

