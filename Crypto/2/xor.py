from operator import xor


# def logical_xor(str1, str2):
#     return bool(str1) ^ bool(str2)

# def bytes_xor(a, b):
#     return bytes(x ^ y for x, y in zip(a, b))

N = input()
M = input()

arr1 = bytes(N, 'utf-8')
arr2 = bytes(M, 'utf-8')
result = []

for i in range(len(arr1)):
    if arr1[i] != arr2[i]:
        count += 1
    result[i] = arr1 ^ arr2
print(count)
print(result)