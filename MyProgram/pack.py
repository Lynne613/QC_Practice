# https://segmentfault.com/a/1190000038454657
from dwave.system import LeapHybridSampler
from math import log2, floor
import dimod

# 0-1 背包問題原型
W = 70
N = 7
c = [35, 85, 30, 50, 70, 80, 55]
w = [12, 27, 11, 17, 20, 10, 15]

# 其他變量
A = max(c)
M = floor(log2(W))
k = [2**i for i in range(M)] + [W + 1 - 2**M]

# BQM
bqm = dimod.AdjVectorBQM(dimod.Vartype.BINARY)

# x 項
for i in range(N):
    bqm.set_linear('x' + str(i), A * (w[i]**2) - c[i])

# x-x 項
for i in range(N):
    for j in range(i + 1, N):
        key = ('x' + str(i), 'x' + str(j))
        bqm.quadratic[key] = 2 * A * w[i] * w[j]

# x-y 項
for i in range(N):
    for j in range(M + 1):
        key = ('x' + str(i), 'y' + str(j))
        bqm.quadratic[key] = -2 * A * w[i] * k[j]

# y 項
for i in range(M + 1):
    bqm.set_linear('y' + str(i), A * (k[i]**2))

# y-y 項
for i in range(M + 1):
    for j in range(i + 1, M + 1):
        key = ('y' + str(i), 'y' + str(j))
        bqm.quadratic[key] = 2 * A * k[i] * k[j]

# 求解
sampler = LeapHybridSampler()
sampleset = sampler.sample(bqm)
sample = sampleset.first.sample
energy = sampleset.first.energy

# 被選中的物品
selected = []
for varname, value in sample.items():
    if value and varname.startswith('x'): # x*
        selected.append(int(varname[1:]))
selected = sorted(selected)

weight_sum = 0
cost_sum = 0
for i in selected:
    weight_sum += w[i]
    cost_sum += c[i]


print('energy:', energy)
print('selected item:', selected)
print('weight:', weight_sum)
print('cost:', cost_sum)