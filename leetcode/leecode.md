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
    def isAnagram(self, s: str, t: str) -> bool:
        s_dict = {}
        for s_ele in s:
            if s_ele in s_dict:
                s_dict[s_ele] = s_dict[s_ele] + 1
            else:
                s_dict[s_ele] = 1
        t_dict = {}
        for t_ele in t:
            if t_ele in t_dict:
                t_dict[t_ele] = t_dict[t_ele] + 1
            else:
                t_dict[t_ele] = 1

        flag = True
        for k, v in s_dict.items():
            if k in t_dict and t_dict[k] == v:
                t_dict.pop(k)
                continue
            flag = False
            break
        return False if len(t_dict.keys()) != 0 else flag
```

时间复杂度为：2*O(m)+O(n)

#### 解题思路2

1. 将2个输入的字符串进行排序（通过快排O(nlog(n))
2. 比较两个排序后的字符串的大小

```

```
