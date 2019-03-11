'''
Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.

Example 1:

Input: 121
Output: true
Example 2:

Input: -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
Example 3:

Input: 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
Follow up:

Coud you solve it without converting the integer to a string?
'''
class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        # The First Method
        # return int(str(abs(x))[::-1]) == x

        # The Second Method
        return Solution.reverse(self, x) == x
    def reverse(self, x):
        rev = 0
        while x > 0:
            end = x % 10
            rev = rev * 10 + end
            x = x // 10

        return rev