'''
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Note that an empty string is also considered valid.

Example 1:

Input: "()"
Output: true
Example 2:

Input: "()[]{}"
Output: true
Example 3:

Input: "(]"
Output: false
Example 4:

Input: "([)]"
Output: false
Example 5:

Input: "{[]}"
Output: true
'''
# 解题方案
# 思路 1 ******- 时间复杂度: O(N^2)******- 空间复杂度: O(N)******
#
# The replace() method returns a copy of the string where old substring is replaced with the new substring. The original string is unchanged.

class Solution:
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        while '[]' in s or '()' in s or '{}' in s:
            s = s.replace('[]','').replace('()','').replace('{}','')
        return len(s) == 0
# 思路 2 ******- 时间复杂度: O(N)******- 空间复杂度: O(N)******
#
# 因为一共只有三种状况"(" -> ")", "[" -> "]", "{" -> "}".
#
# 一遇到左括号就入栈，右括号出栈，这样来寻找对应
#
# 需要检查几件事：
#
# 出现右括号时stack里还有没有东西
# 出stack时是否对应
# 最终stack是否为空
class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        leftP = '([{'
        rightP = ')]}'
        stack = []
        for char in s:
            if char in leftP:
                stack.append(char)
            if char in rightP:
                if not stack:
                    return False
                tmp = stack.pop()
                if char == ')' and tmp != '(':
                    return False
                if char == ']' and tmp != '[':
                    return False
                if char == '}' and tmp != '{':
                    return False
        return stack == []