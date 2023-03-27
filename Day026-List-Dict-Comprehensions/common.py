def get_nums(filename):
    with open(filename) as file:
        return [int(n.strip()) for n in file.readlines()]


nums1, nums2 = [get_nums(f) for f in ['file1.txt', 'file2.txt']]
print([n for n in nums1 if n in nums2])
