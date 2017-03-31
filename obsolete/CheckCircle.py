#!/usr/bin/env python
# encoding=utf-8

"""
You are given an array of positive and negative integers. If a number n at an index is positive, then move forward n steps. Conversely, if it's negative (-n), move backward n steps. Assume the first element of the array is forward next to the last element, and the last element is backward next to the first element. Determine if there is a loop in this array. A loop starts and ends at a particular index with more than 1 element along the loop. The loop must be "forward" or "backward'.

"""


class CheckCircle:
    def findCircle(self, nums):
        """
        Type nums: List[int]
        Rtype :boolean
        """

        n, j = len(nums), 1
        i = 0
        while i < n:
            if nums[i] == nums[j]:
                return True
            else:
                i += nums[i]
                j += nums[j]
                i = self.resNagtive(i, n)
                j = self.resNagtive(j, n)


    def resNagtive(self, num, n):
        if num < 0:
            return int(n + num)
        else:
            return num


if __name__ == "__main__":
    check = CheckCircle()
    nums = [1, 2, 4, 3, 2]
    check.findCircle(nums)