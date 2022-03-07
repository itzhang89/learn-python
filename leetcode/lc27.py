from typing import List


class Solution:
    def removeElement1(self, nums: List[int], val: int) -> int:
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

    def removeElement2(self, nums: List[int], val: int) -> int:
        slow, fast = 0, 0
        while fast < len(nums):
            if nums[fast] != val:
                nums[slow] = nums[fast]
                slow += 1
            fast += 1
        return slow


if __name__ == '__main__':
    nums = [3, 2, 2, 3]
    assert Solution().removeElement1(nums, 3) == 2
    nums = [3, 2, 2, 3]
    assert Solution().removeElement2(nums, 3) == 2

    nums = [0, 1, 2, 2, 3, 0, 4, 2]
    assert Solution().removeElement1(nums, 2) == 5
    nums = [0, 1, 2, 2, 3, 0, 4, 2]
    assert Solution().removeElement2(nums, 2) == 5

    nums = [1]
    assert Solution().removeElement1(nums, 1) == 0
    nums = [1]
    assert Solution().removeElement2(nums, 1) == 0
