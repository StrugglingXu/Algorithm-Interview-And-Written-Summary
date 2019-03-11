'''
Given a 32-bit signed integer, reverse digits of an integer.

Example 1:

Input: 123
Output: 321
Example 2:

Input: -123
Output: -321
Example 3:

Input: 120
Output: 21
Note:
Assume we are dealing with an environment which could only store integers within the 32-bit
signed integer range: [−2^31,  2^31 − 1]. For the purpose of this problem, assume that your function returns 0
when the reversed integer overflows.
'''
class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if (x >= 0):
            res = int(str(x)[::-1])
            return res if res < (2**31 -1) and res > (-2)**31 else 0
        else:
            res = int("-" + (str(x)[1:][::-1]))
            return res if res < (2**31 - 1) and res > (-2)**31 else 0