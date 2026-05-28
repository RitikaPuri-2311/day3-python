
def max_sum_subarray(arr, k):
    n = len(arr)

    if n < k:
        return "error: subarray size is larger than array size"

    max_sum = sum(arr[:k])
    window_sum = max_sum

    for j in range(n - k):
        window_sum = window_sum - arr[j] + arr[j + k]
        max_sum = max(max_sum, window_sum)

    return max_sum


array = [10, 20, 30, 40, 50, 60, 100]
k = 5

result = max_sum_subarray(array, k)
print(result)