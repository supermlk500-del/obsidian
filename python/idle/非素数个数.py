import sys
n = 10 ** 7
prime = []
is_prime = [1] * (n + 1)
is_prime[0] = is_prime[1] = 0
for i in range(2,n + 1):
    if is_prime[i]:prime.append(i)
    for j in prime:
        if i * j > n : break
        is_prime[i * j] = 0
        if i % j == 0:break

a = [0] * (n + 1)
for i in range(2,n + 1):
    a[i] = a[i - 1] + (1 if not is_prime[i] else 0)

for line in sys.stdin:
    input = line.strip()
    l,r = map(int,input.split())
    print(a[r] - a[l-1])
