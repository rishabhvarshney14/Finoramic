# Anagrams - https://www.interviewbit.com/problems/anagrams/

# Worst Time Complexity - O(N * N * D)
# where, N = length of the array
#        D = maximum lenght of the string present in the array

# Approach
# Compare every word with each other and check if they are anagram or not
# I stored the index of all the words that are anagram of some words that we have seen so that we do not have to calculate for that word

class Solution:
    def anagrams(self, A):
        n = len(A)
        result = []
        visited = set()

        # Iterate over the array
        for i, word1 in enumerate(A):
            # if the given word is already an anagram than we do not have to recompute
            # Simply skip this word
            if i in visited:
                continue

            # add a new list in result with the index of this word as only element
            result.append([i+1])

            # Create a dictionary that stores the occurance of chars in this word
            counter = dict()
            for char in word1:
                if char not in counter:
                    counter[char] = 0
                counter[char] += 1
            
            # Now iterate over the array from the next index
            for j in range(i+1, n):
                # again we skip if this word is already an anagram of another word
                if j in visited:
                    continue
                word2 = A[j]

                # create a dicitionary that stores the occurance of chars in this word
                temp = dict()
                for char in word2:
                    if char not in temp:
                        temp[char] = 0
                    temp[char] += 1

                # Compare the original word with this word
                flag = False
                for char in word2:
                    if char not in counter or counter[char] != temp[char]:
                        flag = True
                        break
                
                # if both words are anagram add the index in result and visited
                if not flag:
                    visited.add(j)
                    result[-1].append(j+1)
        
        return result
