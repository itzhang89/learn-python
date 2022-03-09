# 基础知识



## 字符串

### 迭代字符串

1. 通过for in 来实现

   ```python
   for element in string_name:
       print(element, end=' ')
   ```

2. 通过range来实现字符串的index

   ```python
   for element in range(0, len(string_name)):
       print(string_name[element])
   ```

3. 通过 `enumerate()`  函数来实现

   ```python
   for i, v in enumerate(string_name):
       print(v)
   ```

4. 反转迭代字符串

   ```python
   for element in string_name[ : :-1]:
       print(element, end =' ')
   ```

## 比较

2个字典中比较会比较所有的元素是否都相等。

## 初始化数组

1. 通过Ranger来循环

   ```python
   [value for element in range(num)]
   ```

2. 通过Numpy 模块

   ```python
   import numpy as np
   arr = np.empty(10, dtype=object) 
   ```

3. 通过方法来初始化

   ```python
   arr_num = [0] * 5
   print(arr_num)
    
   arr_str = ['P'] * 10
   print(arr_str)
   ```

   

# LeetCode

## 基础题库

### [242. 有效的字母异位词](https://leetcode-cn.com/problems/valid-anagram/)

给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。

注意：若 s 和 t 中每个字符出现的次数都相同，则称 s 和 t 互为字母异位词。

示例 1:

输入: s = "anagram", t = "nagaram"
输出: true
示例 2:

输入: s = "rat", t = "car"
输出: false

**提示:**

- `1 <= s.length, t.length <= 5 * 104`
- `s` 和 `t` 仅包含小写字母

#### 解题思路1

1. 将2个字符串都变成一个字典，并且统计其中的每个字符出现的次数
2. 遍历第一个字典，依次比较相同Key元素的次数，如果相同，则移除第二个字典中的元素，并且继续比较；如果不同，则直接跳出显示失败；
3. 如果遍历第一个字符后，如果发现第二个数组还有多的元素，也判断失败。

```python
    def isAnagram1(self, s: str, t: str) -> bool:
        s_dict, t_dict = {}, {}
        for e in s:
            s_dict[e] = s_dict.get(e, 0) + 1
        for e in t:
            t_dict[e] = t_dict.get(e, 0) + 1
        return t_dict == s_dict
```

时间复杂度为：2*O(m)+O(n)

#### 解题思路2

1. 将2个输入的字符串进行排序（通过快排O(nlog(n))
2. 比较两个排序后的字符串的大小

```python
    def isAnagram1(self, s: str, t: str) -> bool:
        return sorted(t) == sorted(s)
```



## stormzhang算法训练营

### [26. 删除有序数组中的重复项](https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array/)

给你一个 升序排列 的数组 nums ，请你 原地 删除重复出现的元素，使每个元素 只出现一次 ，返回删除后数组的新长度。元素的 相对顺序 应该保持 一致 。

由于在某些语言中不能改变数组的长度，所以必须将结果放在数组nums的第一部分。更规范地说，如果在删除重复项之后有 k 个元素，那么 nums 的前 k 个元素应该保存最终结果。

将最终结果插入 nums 的前 k 个位置后返回 k 。

不要使用额外的空间，你必须在 原地 修改输入数组 并在使用 O(1) 额外空间的条件下完成。

#### 解题思路1

1. 排序后的元素，相同的元素肯定都连在一起
2. 依次的采用2个指针遍历数组
3. 快的数组依次找出不同的元素，然后将元素复制到慢的元素位置

```python
    def removeDuplicates(self, nums: List[int]) -> int:
        slow, fast = 0, 1
        while fast < len(nums):
            if nums[slow] != nums[fast]:
                slow += 1
                nums[slow] = nums[fast]
            fast += 1
        return slow + 1
```



### [27. 移除元素](https://leetcode-cn.com/problems/remove-element/)

给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素，并返回移除后数组的新长度。

不要使用额外的数组空间，你必须仅使用 O(1) 额外空间并 原地 修改输入数组。

元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。

#### 解题思路1

1. 定义2个指针；
2. 第1个指针从头到尾，第2个指针从尾到头索引，当第一个指针碰到val的值时，同第二个指针所在的位置进行交换（交换的时候也需要判断一下）。
3. 当2个指针相遇的时候，推出循环。
4. 返回获得更小的两个指针长度+1

```python
    def removeElement(self, nums: List[int], val: int) -> int:
        i, j = 0, len(nums) - 1
        while i <= j:
            if nums[j] == val:
                j -= 1
                continue
            if nums[i] == val:
                nums[i] = nums[j]
                j -= 1
            i += 1
        return min(i, j) + 1
```

#### 解题思路2

同26题一样，定义2个指针

1. 快指针依次的过滤val的元素
2. 将过滤的元素依次的放入slow的指针中

```
    def removeElement(self, nums: List[int], val: int) -> int:
        slow, fast = 0, 0
        while fast < len(nums):
            if nums[fast] != val:
                nums[slow] = nums[fast]
                slow += 1
            fast += 1
        return slow
```

可以快速的理解，就是前面指针在过滤，将过滤好的元素依次的插入前面的指针中。

### [83. 删除排序链表中的重复元素](https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list/)

```python
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        slow, fast = head, head
        while fast:
            if slow.val != fast.val:
                slow.next = fast
                slow = slow.next
            fast = fast.next
        slow.next = None  # 断开与后面元素的联系
        return head
```

### [283. 移动零](https://leetcode-cn.com/problems/move-zeroes/)

同前面一样，过滤0的元素并且向前移动，到末尾都填充0

```python
    def moveZeroes(self, nums: List[int]) -> None:
        slow, fast = 0, 0
        while fast < len(nums):
            if nums[fast] != 0:
                nums[slow] = nums[fast]
                slow += 1
            fast += 1
        while slow < len(nums):
            nums[slow] = 0
            slow += 1
```

[小而美的算法技巧：前缀和数组 :: labuladong的算法小抄](https://labuladong.gitee.io/algo/2/22/56/)

### [560. 和为 K 的子数组](https://leetcode-cn.com/problems/subarray-sum-equals-k/)

给你一个整数数组 `nums` 和一个整数 `k` ，请你统计并返回该数组中和为 `k` 的连续子数组的个数。

#### 解题思路1

**利用求前缀和** 的思路，计算出前n个元素的和

1. 依次计算2个前缀和之间的差值
2. 判断是否为k。

这种方法的时间复杂度为O(n) + O(n2)，时间上过不去

```python
    def subarraySum(self, nums, k):
        preSumNums = [0] * (len(nums) + 1)
        i, cnt = 0, 0
        while i < len(nums):
            preSumNums[i + 1] = preSumNums[i] + nums[i]

        i = 0
        while i < len(nums):
            j = i
            while j < len(nums):
                if preSumNums[j] == nums[i] + k:
                    cnt += 1
            i += 1
        return cnt
```

#### 解题思路2

将计算 presum[j] - presum[i] = k，通过Hash 来转换。将**前缀和放入到Hash中减少一次嵌套的循环**。

```python
    def subarraySum(self, nums, k):
        preSumNums = [0] * (len(nums) + 1)
        cntDict = {0: 1}
        i, cnt = 0, 0
        while i < len(nums):
            preSumNums[i + 1] = preSumNums[i] + nums[i]
            cnt += cntDict.get(preSumNums[i + 1] - k, 0)
            cntDict[preSumNums[i + 1]] = cntDict.get(preSumNums[i + 1], 0) + 1
            i += 1
        return cnt
```

优化点，就是不重新定义新数组，复用现有nums数组

```python
    def subarraySum(self, nums, k):
        i, cnt = 1, 0
        cntDict = {0: 1}
        cnt += cntDict.get(nums[0] - k, 0)
        cntDict[nums[0]] = cntDict.get(nums[0], 0) + 1
        while i < len(nums):
            nums[i] += nums[i - 1]
            cnt += cntDict.get(nums[i] - k, 0)
            cntDict[nums[i]] = cntDict.get(nums[i], 0) + 1
            i += 1
        return cnt
```

### [304. 二维区域和检索 - 矩阵不可变](https://leetcode-cn.com/problems/range-sum-query-2d-immutable/)

给定一个二维矩阵 matrix，以下类型的多个请求：

计算其子矩形范围内元素的总和，该子矩阵的 左上角 为 (row1, col1) ，右下角 为 (row2, col2) 。
实现 NumMatrix 类：

NumMatrix(int[][] matrix) 给定整数矩阵 matrix 进行初始化
int sumRegion(int row1, int col1, int row2, int col2) 返回 左上角 (row1, col1) 、右下角 (row2, col2) 所描述的子矩阵的元素 总和 。

**几何题目，明确如何定义二维数组**



### [1094. 拼车](https://leetcode-cn.com/problems/car-pooling/)

**构造差分数组** `diff`**，就可以快速进行区间增减的操作**

假设你是一位顺风车司机，车上最初有 capacity 个空座位可以用来载客。由于道路的限制，车 只能 向一个方向行驶（也就是说，不允许掉头或改变方向，你可以将其想象为一个向量）。

这儿有一份乘客行程计划表 trips[][]，其中 trips[i] = [num_passengers, start_location, end_location] 包含了第 i 组乘客的行程信息：

必须接送的乘客数量；
乘客的上车地点；
以及乘客的下车地点。
这些给出的地点位置是从你的 初始 出发位置向前行驶到这些地点所需的距离（它们一定在你的行驶方向上）。

请你根据给出的行程计划表和车子的座位数，来判断你的车是否可以顺利完成接送所有乘客的任务（当且仅当你可以在所有给定的行程中接送所有乘客时，返回 true，否则请返回 false）。

```python
    def carPooling(self, trips, capacity):
        """
        :type trips: List[List[int]]
        :type capacity: int
        :rtype: bool
        """
        diffs = [0] * 1001
        for trip in trips:
            diffs[trip[1]] += trip[0]
            diffs[trip[2]] -= trip[0]
        sum = 0
        for ele in diffs:
            sum += ele
            if sum > capacity:
                return False
        return True
```



### [1109. 航班预订统计](https://leetcode-cn.com/problems/corporate-flight-bookings/)

这里有 n 个航班，它们分别从 1 到 n 进行编号。

有一份航班预订表 bookings ，表中第 i 条预订记录 bookings[i] = [firsti, lasti, seatsi] 意味着在从 firsti 到 lasti （包含 firsti 和 lasti ）的 每个航班 上预订了 seatsi 个座位。

请你返回一个长度为 n 的数组 answer，里面的元素是每个航班预定的座位总数。

```python
    def corpFlightBookings(self, bookings, n):
        """
        :type bookings: List[List[int]]
        :type n: int
        :rtype: List[int]
        """
        answer = [0] * n
        for book in bookings:
            answer[book[0] - 1] += book[2]
            if book[1] < n:
                answer[book[1]] -= book[2]
        for i in range(1, n):
            answer[i] += answer[i - 1]
        return answer
```

