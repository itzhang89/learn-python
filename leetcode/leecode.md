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

```
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

```
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