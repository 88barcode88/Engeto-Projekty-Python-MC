sequence = [1, 21, 5, 3, 5, 8, 321, 1, 2, 2, 32, 6, 9, 1, 4, 6, 3, 1, 2]
counts = dict()

for item in sequence:
    counts[item] = 1
else:
    counts[item] += 1

sorted_keys = sorted(counts.keys())
for key in sorted_keys:
    print(f"key: {key}, value: {counts[key]}")
