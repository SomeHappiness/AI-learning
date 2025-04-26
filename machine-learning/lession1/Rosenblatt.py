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

# 设置权重参数
w = 0.5
# 学习率
alpha = 0.05
for j in range(100):
    for i in range(100):
        x = xs[i]
        y = ys[i]
        y_pre = w * x
        # 误差
        e = y - y_pre
        # 更新权重
        w = w + alpha * e * x
print(w)
# 使用最终权重建模
y_pre = w * xs
# 预测函数曲线
plt.plot(xs, y_pre)

# 展示函数
plt.show()
