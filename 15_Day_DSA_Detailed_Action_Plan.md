# 15-Day DSA Detailed Action Plan (Python Version)
This document expands on the Zero-to-Hero schedule by setting a daily goal, assigning specific practice problems for you to try independently, and providing the verified solution code specifically in **Python**.

## Day 1: Syntax & Basic Logic
**Daily Goal:** Finish 3 Fundamental Math/Logic Questions
**Study Material Reference:** `Placement material / Durgasoft python book .pdf` & `100 python interview questions .pdf`

### Practice Problems

**1. Problem: Factorial of a Number**
- *Reference Idea:* Setup loop structures based on `100 python interview questions .pdf`
- *Task:* Write a program to find the factorial of a given positive integer `N`.
- *Try it yourself first!*

**Verification Solution:**
```python
def factorial(n):
    fact = 1
    for i in range(1, n + 1):
        fact *= i
    return fact

# Test the function
if __name__ == "__main__":
    print("Factorial:", factorial(5))
```

**2. Problem: Check Prime Number**
- *Task:* Return `True` if the number is prime, else `False`.
**Verification Solution:**
```python
def is_prime(n):
    if n <= 1: 
        return False
    # Only need to check up to the square root of n
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

**3. Problem: Fibonacci Series (with memoization)**
- *Task:* Print the first `N` Fibonacci numbers efficiently.
**Verification Solution:**
```python
def fibonacci(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]

# Print first 10 Fibonacci numbers
for i in range(10):
    print(fibonacci(i), end=" ")  # 0 1 1 2 3 5 8 13 21 34
```

---

## Day 2: Array (Lists) Foundations
**Daily Goal:** Finish 3 Array Manipulation Questions
**Study Material Reference:** `Placement material / C arrays q_a with explana.pdf` (Focus on the logic, apply it in Python Lists)

### Practice Problems

**1. Problem: Find Maximum & Minimum Element in an Array**
- *Task:* Traverse the list and find both min and max efficiently.
**Verification Solution:**
```python
def find_min_max(arr):
    if not arr: 
        return None, None
    # Python has builtins, but doing it manually trains your logic:
    max_el = float('-inf')
    min_el = float('inf')
    
    for num in arr:
        if num > max_el: max_el = num
        if num < min_el: min_el = num
        
    return min_el, max_el

# Or use standard python: min(arr), max(arr)
```

**2. Problem: Move all Zeros to the End**
- *Task:* In-place shift all `0`s to the end while maintaining the order of non-zero elements.
**Verification Solution:**
```python
def move_zeroes(nums):
    non_zero_index = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            # Swap non-zero elements to the front
            nums[non_zero_index], nums[i] = nums[i], nums[non_zero_index]
            non_zero_index += 1
```

**3. Problem: Two Sum**
- *Task:* Given a list `nums` and a `target`, return indices of the two numbers that add up to `target`.
**Verification Solution:**
```python
def two_sum(nums, target):
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Example: two_sum([2, 7, 11, 15], 9) -> [0, 1]
```

---

## Day 3: Searching & Sorting
**Daily Goal:** Finish 2 Core Search/Sort Implementations
**Study Material Reference:** `Placement material / Algorithm notes for professionals(257pgs).pdf` (Chapters on Search/Sort)

### Practice Problems

**1. Problem: Iterative Binary Search**
- *Task:* Search for a `target` element in a **sorted list** and return its index. Return `-1` if not found.
**Verification Solution:**
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1
```

**2. Problem: Check if Array is Sorted**
- *Task:* Return `True` if array elements are strictly non-decreasing.
**Verification Solution:**
```python
def is_sorted(arr):
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            return False
    return True

# Pythonic one-liner: 
# return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))
```

---

## Day 4: Strings & Pointers
**Daily Goal:** Finish 2 String Manipulation Questions
**Study Material Reference:** `Placement material / Cracking the Coding Interview.pdf` (Chapter 1: Arrays and Strings) & `100 python interview questions .pdf`

### Practice Problems

**1. Problem: Is Unique (CTCI Q 1.1)**
- *Reference:* `Placement material / Cracking the Coding Interview.pdf / Chapter 1 / Q 1.1`
- *Task:* Implement an algorithm to determine if a string has all unique characters.
**Verification Solution:**
```python
def is_unique(s):
    char_set = set()
    for char in s:
        if char in char_set:
            return False
        char_set.add(char)
    return True

# Pythonic approach: return len(set(s)) == len(s)
```

**2. Problem: Valid Palindrome (Ignoring special characters)**
- *Task:* Check if a string is a palindrome.
**Verification Solution:**
```python
def is_palindrome(s):
    # Using two pointers
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

# Pythonic approach: return s == s[::-1]
```

---

## Day 5: Linked Lists (Singly)
**Daily Goal:** Implement 2 Core Functions 
**Study Material Reference:** `Placement material / DSA Handwritten guide(Beginner to Advanced).pdf`

### Practice Problems

**1. Problem: Reverse a Singly Linked List**
- *Task:* Given the `head` of a singly linked list, reverse the list and return its object.
**Verification Solution:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev, curr = None, head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev
```

**2. Problem: Find Middle of a Linked List**
- *Task:* Return the middle node. If two middle nodes exist, return the second one.
**Verification Solution:**
```python
def find_middle(head):
    slow = fast = head
    # Fast moves 2x speed — when fast reaches end, slow is at middle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

---

## Day 6: Linked Lists (Advanced)
**Daily Goal:** Finish 2 Logic Questions
**Study Material:** `Placement material / Cracking the Coding Interview.pdf` (Chapter 2: Linked Lists)

### Practice Problems

**1. Problem: Return Kth to Last (CTCI 2.2)**
- *Reference:* `Cracking the Coding Interview.pdf / Chapter 2 / Q 2.2`
- *Task:* Find the Kth to last element of a singly linked list using the two-pointer technique.
**Verification Solution:**
```python
def kth_to_last(head, k):
    p1 = p2 = head
    
    # Move p1 ahead by k steps
    for _ in range(k):
        if not p1: return None # List is too short
        p1 = p1.next
        
    # Move both pointers until p1 reaches the end
    while p1:
        p1 = p1.next
        p2 = p2.next
        
    return p2
```

**2. Problem: Detect Cycle in Linked List (Floyd's Algorithm)**
- *Task:* Return `True` if the linked list has a cycle.
**Verification Solution:**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # Moves 1 step
        fast = fast.next.next   # Moves 2 steps
        if slow == fast:        # They meet inside the cycle!
            return True
    return False
```

---

## Day 7: Stacks & Queues
**Daily Goal:** Finish 2 Practical Stack Questions
**Study Material:** `Placement material / DSA Handwritten guide(Beginner to Advanced).pdf` 

### Practice Problems

**1. Problem: Valid Parentheses**
- *Task:* Given `{`, `}`, `(`, `)`, `[`, `]`, determine if the string is structurally valid.
**Verification Solution:**
```python
def is_valid(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping:
            # Pop topmost element if stack isn't empty, else dummy char
            top_element = stack.pop() if stack else '#'
            
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
            
    return not stack
```

**2. Problem: Implement a Queue using Two Stacks**
- *Task:* Simulate a queue (FIFO) using two Python lists (acting as stacks).
**Verification Solution:**
```python
class MyQueue:
    def __init__(self):
        self.stack_in = []   # For pushing elements
        self.stack_out = []  # For popping elements

    def push(self, x):
        self.stack_in.append(x)

    def pop(self):
        self._move_if_needed()
        return self.stack_out.pop()

    def peek(self):
        self._move_if_needed()
        return self.stack_out[-1]

    def _move_if_needed(self):
        if not self.stack_out:  # Only refill when out-stack is empty
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
```

---

## Day 8: Deep Revision
**Goal:** 0 New Questions. Redo anything you struggled with from Days 1-7 in Python. Understand Python slicing and dictionary overhead.

---

## Day 9: Trees (Basics)
**Daily Goal:** Implement 2 Tree Traversals
**Study Material:** `Placement material / DSA Handwritten guide(Beginner to Advanced).pdf`

### Practice Problems

**1. Problem: Binary Tree Inorder Traversal**
- *Task:* Left -> Node -> Right recursively.
**Verification Solution:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root):
    res = []
    
    def inorder(node):
        if not node: return
        inorder(node.left)
        res.append(node.val)
        inorder(node.right)
        
    inorder(root)
    return res
```

**2. Problem: Maximum Depth of Binary Tree**
- *Task:* Return its max depth recursively.
**Verification Solution:**
```python
def max_depth(root):
    if not root: 
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

---

## Day 10: Binary Search Trees (BST) & Heaps
**Daily Goal:** 2 BST Properties Questions
**Study Material:** `Placement material / Algorithm notes for professionals(257pgs).pdf` 

### Practice Problems

**1. Problem: Search in a BST**
- *Task:* Find a node in a BST. If properties hold: go left if val < root.val, right if val > root.val.
**Verification Solution:**
```python
def search_bst(root, val):
    if not root or root.val == val:
        return root
        
    if val < root.val:
        return search_bst(root.left, val)
        
    return search_bst(root.right, val)
```

**2. Problem: Kth Largest Element using a Min-Heap**
- *Task:* Find the Kth largest element in an unsorted list.
**Verification Solution:**
```python
import heapq

def find_kth_largest(nums, k):
    # Build a min-heap of size k
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)  # Remove smallest, keeping top-k largest
    return min_heap[0]  # Root of min-heap = Kth largest

# Example: find_kth_largest([3,2,1,5,6,4], 2)  -> 5
```

---

## Day 11: Graphs (Basics)
**Daily Goal:** 1 Traversal Algorithm
**Study Material:** `Placement material / DSA Handwritten guide(Beginner to Advanced).pdf`

### Practice Problems

**1. Problem: Breadth-First Search (BFS) Traversal**
- *Task:* Given an adjacency dictionary list, print BFS order.
**Verification Solution:**
```python
from collections import deque

def bfs(start_node, adj):
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)

    while queue:
        curr = queue.popleft()
        print(curr, end=" ")

        for neighbor in adj.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

---

## Day 12: Graphs (Advanced)
**Daily Goal:** 1 Application Concept
**Study Material:** `Placement material / Algorithm notes for professionals(257pgs).pdf`

### Practice Problems

**1. Problem: Detect Cycle in Undirected Graph (DFS based)**
- *Task:* Check if the graph maintains a cycle somewhere.
**Verification Solution:**
```python
def is_cyclic_util(v, adj, visited, parent):
    visited.add(v)
    
    for neighbor in adj.get(v, []):
        if neighbor not in visited:
            if is_cyclic_util(neighbor, adj, visited, v):
                return True
        # If an adjacent vertex is visited and not parent of current vertex
        elif parent != neighbor:
            return True
            
    return False
```

---

## Day 13: Recursion & Backtracking
**Daily Goal:** 2 Classical Recursion problems
**Study Material:** `Placement material / Cracking the Coding Interview.pdf` (Chapter 8: Recursion and DP)

### Practice Problems

**1. Problem: Triple Step (CTCI 8.1)**
- *Reference:* `Cracking the Coding Interview.pdf / Chapter 8 / Q 8.1`
- *Task:* A child running up stairs can hop 1, 2, or 3 steps. Count possible ways (with memoization).
**Verification Solution:**
```python
def count_ways(n, memo=None):
    if memo is None:
        memo = {}
        
    if n < 0: return 0
    if n == 0: return 1
    
    if n in memo: 
        return memo[n]
        
    memo[n] = count_ways(n-1, memo) + count_ways(n-2, memo) + count_ways(n-3, memo)
    return memo[n]
```

**2. Problem: Subsets / Power Set (Backtracking)**
- *Task:* Given a set of distinct integers, return ALL possible subsets (the power set).
**Verification Solution:**
```python
def subsets(nums):
    result = []
    
    def backtrack(start, current):
        result.append(list(current))  # Add current subset to result
        
        for i in range(start, len(nums)):
            current.append(nums[i])       # Choose
            backtrack(i + 1, current)     # Explore
            current.pop()                 # Un-choose (Backtrack)
    
    backtrack(0, [])
    return result

# Example: subsets([1, 2, 3]) -> [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

---

## Day 14: Dynamic Programming (DP)
**Daily Goal:** 1 DP problem
**Study Material:** `Placement material / Algorithm notes for professionals(257pgs).pdf`

### Practice Problems

**1. Problem: Coin Change (Minimum Coins)**
- *Task:* You are given an integer list `coins` and an integer `amount`. Find fewest number of coins to make amount.
**Verification Solution:**
```python
def coin_change(coins, amount):
    # dp array initialized to infinity
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)
                
    return dp[amount] if dp[amount] != float('inf') else -1
```

---

## Day 15: The Mock Interview Test
**Daily Goal:** 2 General Logic Tests
**Study Material:** `Placement material / 100 python interview questions .pdf` & `cracking interview.pdf`

### Practice Problems

**1. Problem: Maximum Subarray Sum (Kadane's Algorithm)**
- *Task:* Find the contiguous subarray which has the largest sum.
**Verification Solution:**
```python
def max_sub_array(nums):
    current_sum = max_sum = nums[0]
    
    for num in nums[1:]:
        # Start a new contiguous sub-array or append to the current one
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
        
    return max_sum

# Example: max_sub_array([-2,1,-3,4,-1,2,1,-5,4]) -> 6  (subarray [4,-1,2,1])
```

**2. Problem: Merge Two Sorted Lists (Classic Interview Closer)**
- *Task:* Merge two sorted linked lists and return the merged sorted list.
**Verification Solution:**
```python
def merge_two_lists(l1, l2):
    dummy = ListNode(0)  # Dummy head node trick
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # Attach the remaining part
    current.next = l1 if l1 else l2
    return dummy.next
```

---

## 🎯 Summary: Your Daily Question Count Tracker

| Day | Topic | # Questions | Status |
|-----|-------|-------------|--------|
| 1 | Syntax & Logic | 3 | ☐ |
| 2 | Arrays / Lists | 3 | ☐ |
| 3 | Searching & Sorting | 2 | ☐ |
| 4 | Strings & Two-Pointer | 2 | ☐ |
| 5 | Linked Lists (Singly) | 2 | ☐ |
| 6 | Linked Lists (Advanced) | 2 | ☐ |
| 7 | Stacks & Queues | 2 | ☐ |
| 8 | REVISION DAY | — | ☐ |
| 9 | Trees (Basics) | 2 | ☐ |
| 10 | BST & Heaps | 2 | ☐ |
| 11 | Graphs (Basics) | 1 | ☐ |
| 12 | Graphs (Advanced) | 1 | ☐ |
| 13 | Recursion & Backtracking | 2 | ☐ |
| 14 | Dynamic Programming | 1 | ☐ |
| 15 | Mock Interview | 2 | ☐ |
| **TOTAL** | | **27 problems** | |

**CONGRATULATIONS!** You have now built a full 27-problem portfolio covering every core DSA topic in Python! Your next step: focus on speed. Try solving each Day's problems under a timer (20 mins/problem). You are ready to crack it! 🚀
