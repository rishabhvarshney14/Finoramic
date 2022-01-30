# 3 Sum - https://www.interviewbit.com/problems/3-sum/

# Time Complexity => O(N^2) (iterating over array + two pointers) + O(NlogN) (sorting)
class Solution:
    def threeSumClosest(self, A, B):
        A.sort()
        n = len(A)

        # if there is only three elements in the array return its sum because it is the only possible value
        if n == 3:
            return sum(A)

        res = None
        for i, ele in enumerate(A[:-2]):
            left = i+1
            right = n-1
            while left < right:
                if res == None:
                    res = A[left] + A[right] + ele
                elif abs(B - (A[left] + A[right] + ele)) < abs(B - res):
                    res = A[left] + A[right] + ele
                    left += 1
                elif A[left] + A[right] + ele > B:
                    right -= 1
                else:
                    left += 1
            
        return res