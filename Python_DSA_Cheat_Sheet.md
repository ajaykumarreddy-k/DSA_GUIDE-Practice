# 🐍 The Ultimate Python DSA Cheat Sheet

If you know the contents of this file, you are mathematically immune to forgetting Python basics during an interview. This cheat sheet takes you from literal syntax to building complex Data Structure nodes.

---

## 1. 🧱 The Absolute Basics

### Variables & Data Types
```python
# No type declaration needed
x = 10                  # int
y = 3.14                # float
name = "DSA"            # str
is_true = True          # bool

# Multiple assignment
a, b, c = 1, 2, 3

# Swapping without temp variable
a, b = b, a
```

### Conditionals (If/Else)
```python
if x > 5:
    print("Greater")
elif x == 5:
    print("Equal")
else:
    print("Smaller")

# Inline If-Else (Ternary)
status = "Even" if x % 2 == 0 else "Odd"
```

### Loops
```python
# Iterating a specific number of times
for i in range(5):        # 0, 1, 2, 3, 4
    pass

for i in range(1, 6):     # 1, 2, 3, 4, 5
    pass

for i in range(5, 0, -1): # 5, 4, 3, 2, 1 (reverse)
    pass

# While loop
count = 0
while count < 5:
    count += 1
```

---

## 2. 📦 Core Built-In Data Structures

### Lists (Arrays) `O(1) Access`
```python
arr = [1, 2, 3]

arr.append(4)           # O(1) - [1, 2, 3, 4]
arr.insert(0, 0)        # O(N) - [0, 1, 2, 3, 4]
arr.pop()               # O(1) - removes last element
arr.pop(0)              # O(N) - removes first element
arr.sort()              # O(N log N) - Ascending
arr.sort(reverse=True)  # O(N log N) - Descending

# Slicing: arr[start : stop : step]
sub = arr[1:3]          # Elements at index 1 and 2
rev = arr[::-1]         # Reverse the list
```

### Dictionaries (Hash Maps) `O(1) Lookup`
```python
hash_map = {"a": 1, "b": 2}

hash_map["c"] = 3             # Insert/Update O(1)
val = hash_map.get("a", 0)    # Fetch with default fallback 0 if not found
del hash_map["b"]             # Delete O(1)

# Iteration
for key, value in hash_map.items():
    print(key, value)
```

### Sets `O(1) Lookup/Unique`
```python
my_set = set([1, 2, 2, 3])    # {1, 2, 3}

my_set.add(4)                 # O(1)
my_set.remove(4)              # O(1) - throws error if not found
my_set.discard(5)             # O(1) - NO error if not found
```

### Tuples (Immutable Lists)
```python
# Cannot be changed once created (good for dictionary keys!)
point = (10, 20)
x, y = point
```

---

## 3. ⚡ Pythonic Fast-Tricks

### List/Dict Comprehensions
```python
# Create an array of squares from 0 to 9
squares = [x**2 for x in range(10)]

# Filter just evens
evens = [x for x in range(10) if x % 2 == 0]

# Dict comprehension
square_dict = {x: x**2 for x in range(5)}
```

### Important Functions
```python
# Enumerate: Get index and value simultaneously
for index, val in enumerate(["a", "b", "c"]):
    print(index, val)

# Zip: Iterate two arrays at the same time
arr1, arr2 = [1, 2], [3, 4]
for a, b in zip(arr1, arr2):
    print(a, b)

# Infinity (For min/max finding)
max_val = float('inf')
min_val = float('-inf')
```

---

## 4. 🚀 Advanced DSA Node & Structure Creation

*These are the exact classes you'll use in every standard DSA interview problem.*

### 🔗 1. Singly Linked List Node
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val     # Value of the node
        self.next = next   # Pointer to the next node

# Usage:
head = ListNode(1)
head.next = ListNode(2)
```

### 🌲 2. Binary Tree Node
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Usage:
root = TreeNode(10)
root.left = TreeNode(5)
root.right = TreeNode(15)
```

### 📚 3. Stacks & Queues (Optimal approach)
```python
# Stack (Last In First Out)
stack = []
stack.append(1)   # Push
val = stack.pop() # Pop

# Queue (First In First Out) --> DO NOT use lists to pop(0)! Use deque!
from collections import deque

queue = deque()
queue.append(1)       # Enqueue (Add to right)
val = queue.popleft() # Dequeue (Remove from left in O(1) time)
```

### 🕸️ 4. Graph Representation (Adjacency List)
```python
from collections import defaultdict

# An adjacency list is best represented as a dictionary of lists.
# defaultdict avoids KeyErrors!
graph = defaultdict(list)

# Usage: Add edges between nodes 0 and 1
graph[0].append(1)
graph[1].append(0)  # If undirected graph
```

### 🏔️ 5. Heaps (Priority Queue)
By default, Python's `heapq` is a **MIN-HEAP**.

```python
import heapq

min_heap = []
heapq.heappush(min_heap, 5)
heapq.heappush(min_heap, 1)

smallest = heapq.heappop(min_heap) # Returns 1

# Max-Heap Trick: Multiply by -1 before pushing, and multiply by -1 when popping!
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -10)
largest = -heapq.heappop(max_heap) # Pops -10, converts back to 10
```

---

## 5. 🔧 Functions & Lambda

```python
# Basic function with default argument
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# *args: Accept any number of positional arguments
def sum_all(*args):
    return sum(args)

# **kwargs: Accept any number of keyword arguments  
def print_info(**kwargs):
    for key, val in kwargs.items():
        print(f"{key}: {val}")

# Lambda (anonymous, one-line function)
square = lambda x: x ** 2

# Sorting with a custom key
words = ["banana", "apple", "cherry"]
words.sort(key=lambda x: len(x))   # Sort by string length

# Sorting a list of tuples by 2nd element
pairs = [(1, 3), (2, 1), (4, 2)]
pairs.sort(key=lambda x: x[1])     # -> [(2, 1), (4, 2), (1, 3)]
```

---

## 6. 📝 Essential String Methods

```python
s = "  Hello, World!  "

s.strip()          # "Hello, World!"   - Remove leading/trailing whitespace
s.lower()          # "  hello, world!  "
s.upper()          # "  HELLO, WORLD!  "
s.replace("World", "Python")  # "  Hello, Python!  "
s.split(", ")      # ['  Hello', 'World!  ']  - Split by delimiter
",".join(["a","b","c"])  # "a,b,c"  - Join list into string

s.startswith("Hello")  # False (has leading spaces)
s.strip().startswith("Hello")  # True
s.find("World")    # 8  - Returns index or -1 if not found
s.count("l")       # 3  - Count occurrences

# Character checks (very useful for interview string problems)
"abc".isalpha()    # True  - all alphabetic characters
"123".isdigit()    # True  - all digits
"abc123".isalnum() # True  - letters and digits

# String -> List -> String (only way to "modify" a string)
s = "hello"
s_list = list(s)      # ['h', 'e', 'l', 'l', 'o']
s_list[0] = 'H'
result = "".join(s_list)  # 'Hello'

# Counter - frequency map (SUPER useful!)
from collections import Counter
freq = Counter("banana")   # Counter({'a': 3, 'n': 2, 'b': 1})
freq['a']                  # 3
```

---

## 7. 🛡️ Error Handling (Try/Except)

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except (ValueError, TypeError) as e:
    print(f"Error: {e}")
else:
    print("Success!")   # Runs only if NO exception
finally:
    print("Always runs")  # Runs no matter what
```

---

## 8. 🏆 Must-Know Algorithm Templates

### Template 1: Two Pointers (for sorted arrays / strings)
```python
def two_pointer_template(arr):
    left, right = 0, len(arr) - 1
    
    while left < right:
        # CONDITION: adjust pointers based on your problem
        if arr[left] + arr[right] == target:
            return [left, right]   # Found!
        elif arr[left] + arr[right] < target:
            left += 1              # Need bigger sum
        else:
            right -= 1             # Need smaller sum
```

### Template 2: Sliding Window (for subarray/substring problems)
```python
def sliding_window_template(arr, k):
    # Fixed-size window of size k
    window_sum = sum(arr[:k])      # Sum of first window
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Slide: add new, remove old
        max_sum = max(max_sum, window_sum)
        
    return max_sum
```

### Template 3: DFS on Trees (3 traversals in one pattern)
```python
def dfs(node):
    if not node:
        return
    # print(node.val)  <- PUT HERE for Pre-order
    dfs(node.left)
    # print(node.val)  <- PUT HERE for In-order
    dfs(node.right)
    # print(node.val)  <- PUT HERE for Post-order
```

### Template 4: Binary Search (universal form)
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2  # No integer overflow risk in Python
        
        if arr[mid] == target:
            return mid             # Found!
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1  # Not found
```

---

## 💡 Top 3 "Gotchas" to Remember
1. **Never use `.pop(0)` on a list** if you need a Queue. It takes `O(N)` time. Always use `collections.deque` and `.popleft()`.
2. **Strings in Python are immutable.** You cannot do `s[0] = 'a'`. You have to build a new string or convert it to a list first: `s_list = list(s)`, then `s_list[0] = 'a'`, then `"".join(s_list)`.
3. **Copying a List:** Doing `arr2 = arr1` does NOT copy the list, it just references the exact same memory! Use `arr2 = arr1.copy()` or `arr2 = list(arr1)` or `arr2 = arr1[:]`.
