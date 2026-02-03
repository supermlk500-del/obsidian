def fibonacci(n):
    if n<=1:
        return n
    return fibonacci(n-1)+fibonacci(n-2)
print(fibonacci(3))

def fibonacci_dynamic(n):
    if n<=1:
        return n

    dp=[0]*(n+1)
    dp[1]=1

    for i in range(2,n+1):
        dp[i]=dp[i-1]+dp[i-2]
    return dp[n]
print(fibonacci_dynamic(3))
