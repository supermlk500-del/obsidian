class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        # 初始化左右指针，分别指向数组的头和尾
        left = 0
        right = len(numbers) - 1
        
        # 只要两个指针没有相遇，就一直找
        while left < right:
            current_sum = numbers[left] + numbers[right]
            
            if current_sum == target:
                # 找到了！因为题目要求下标从 1 开始，所以要 +1
                return [left + 1, right + 1]
            
            elif current_sum < target:
                # 现在的和比目标值小，说明需要更大的数，左指针向右移
                left += 1
                
            else:
                # 现在的和比目标值大，说明需要更小的数，右指针向左移
                right -= 1
                
        # 理论上题目保证有解，不会走到这里，但写上是个好习惯
        return [-1, -1]
