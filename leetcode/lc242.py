from collections import Counter


class Solution:
    def isAnagram1(self, s: str, t: str) -> bool:
        s_dict, t_dict = {}, {}
        for e in s:
            s_dict[e] = s_dict.get(e, 0) + 1
        for e in t:
            t_dict[e] = t_dict.get(e, 0) + 1
        return t_dict == s_dict

    def isAnagram2(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)

    # 简洁的写法
    def isAnagram3(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return Counter(s) == Counter(t)


if __name__ == '__main__':
    s = "anagram"
    t = "nagaram"
    assert Solution().isAnagram1(s, t) == True
    assert Solution().isAnagram2(s, t) == True
    s = "rat"
    t = "car"
    assert Solution().isAnagram1(s, t) == False
    assert Solution().isAnagram2(s, t) == False
    s = "a"
    t = "ab"
    assert Solution().isAnagram1(s, t) == False
    assert Solution().isAnagram2(s, t) == False
