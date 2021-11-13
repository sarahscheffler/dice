# Goal: Pr[sum of N M-sided dice >= S]
# Surprisingly annoying to do without simulation!
# (And simulation sucks for 900+ dice.)
# https://math.stackexchange.com/questions/3087660/probability-for-rolling-n-dice-to-add-up-to-at-least-a-specific-sum

# We proceed combinatorially.  
# 
# Step 1: What is probability sum is *exactly* s?
#   How many solutions for "1 <= Yj <= M st sum_{i in [N]} Yi = s 
#                   where Y unif int between 1 and M"?
#   Convert to version introduced by Macaroso:
#   This is equiv to "0 <= Xj <= M-1 st sum_{i in [N]} Xi = s-N
#                   where X unif int between 0 and N-1"
#   NumWaysEQ(N, M, s) = \sum_{0 <= k <= (s-N)/M <= N} (-1)^k (N choose k) ((s - 1 - kM) choose (s - N - kM))
#
# Step 2: Sum this number from s=0 to S (later we'll subtract from total ways)
#   NumWaysLT(s <= S, M, N) = \sum_{0 <= s <= S} \sum_{0 <= k <= (s-N)/M <= N} (-1)^k (N choose k) ((s - 1 - kM) choose (s - N - kM))
#                             (rearrange sums with "double convolution")
#                           = \sum_{0 <= k <+ N} \sum_{0 <= s <= S} (-1)^k ((S - s) choose (S-s)) ((s - 1 - kM) choose (s - N - kM))
#                             (can now remove s)
#                           = \sum_{0 <= k <= N} (-1)^k (N choose k) ((S - kM) choose (S - N - kM))
# 
# Step 3: AllWays(M, N) = M^N
# 
# Step 4: Goal = (AllWays - NumWays(s <= S, M, N)) / AllWays

import math
TEST = True

def binom(n, k):
    """Prettier than comb"""
    if n < 0 or k < 0:
        return 0
    return math.comb(n, k)

def AllWays(M, N):
    """Outcomes when rolling N M-sided dice (order matters)"""
    return M**N

def NumWaysLE(S, M, N):
    """Ways to roll some s <= S on N M-sided dice (order matters)"""
    return sum([ ( ((-1)**k) * binom(N, k) * binom((S - k*M), (S - N - k*M)) ) for k in range(0, N+1) ])

def probRollingLE(S, M, N):
    """Probability of rolling at most sum S on N M-sided dice, inclusive"""
    return NumWaysLE(S, M, N) / AllWays(M, N)

def probRollingGE(S, M, N):
    """Probability of rolling at least sum S on N M-sided dice, inclusive"""
    aw = AllWays(M, N)
    nw = NumWaysLE(S-1, M, N)
    return (aw - nw)/aw

print(probRollingGE(18*262, 10, 905))

if TEST:
    def assertWithin(actual, expected, err=0.001):
        assert(actual - err <= expected <= actual + err)
    assertWithin(0, probRollingGE(100, 6, 2))
    assertWithin(1, probRollingGE(0, 6, 2))
    assertWithin(35/36, probRollingGE(3, 6, 2))
    assertWithin(0.4167, probRollingGE(8, 6, 2))
    assertWithin(0.7918, probRollingGE(100, 10, 20))
    assertWithin(0.0664, probRollingGE(60, 20, 4))
    # checked against https://www.omnicalculator.com/statistics/dice

