import numpy as np
from matplotlib import pyplot as plt


#### 罗森布拉特感知器模型
def get_beans(counts):
    xs = np.random.rand(counts)
    xs = np.sort(xs)
    ys = [1.2 * x + np.random.rand() / 10 for x in xs]
    return xs, ys


# 使用numpy仓库获取豆豆

xs, ys = get_beans(100)
# 绘制title
plt.title("Size-Toxicity Funcition", fontsize=12)
# 绘制x坐标
plt.xlabel("Bean Size")
# 绘制y坐标
plt.ylabel("Toxicity")
# 绘制数据
plt.scatter(xs, ys)

w = 0.5
alpha = 0.05
for j in range(1000):
    for i in range(100):
        x = xs[i]
        y = ys[i]
        y_pre = w * x
        e = y - y_pre
        w = w + alpha * e * x
        print(w)

print(w)
y_pre = w * xs
plt.plot(xs, y_pre)

plt.show()
