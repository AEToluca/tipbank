import Deque

def maxSubarrayWithRotation(array: list[int], k: int) -> int:
    n = len(array)
    if k > n: #If the subarray size k is larger than the array, return 0
        return 0

    #Fill the deqeue with first k elements and calculate the sum
    dq = Deque()
    sum = 0
    for i in range(k):
        dq.insertFront(array[i])
        sum += array[i]
    max_sum = sum

    #Calcualte sum of each rotation
    for i in range(1, n):
        sum -= dq.removeFront()
        new = array[(i+k-1) % n]
        dq.insertBack(new)
        sum += new
        max_sum = max(max, sum)
    return max

def main():
    k = int(input())
    int_list = input()
    array = [int(x) for x in int_list.split(', ')]
    # Your code goes here
    # Remember to use the deque you implemented!
    result = maxSubarrayWithRotation(array, k)
    print(result)
    
if __name__ == "__main__":
    main()