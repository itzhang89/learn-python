from typing import List


class Solution:
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


if __name__ == '__main__':
    nums = [3, 2, 2, 3]
    assert Solution().removeElement(nums, 3) == 2

    nums = [0, 1, 2, 2, 3, 0, 4, 2]
    assert Solution().removeElement(nums, 2) == 5

    nums = [1]
    assert Solution().removeElement(nums, 1) == 0
