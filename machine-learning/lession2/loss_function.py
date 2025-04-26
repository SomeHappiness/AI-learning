# 方差代价函数也被称为损失函数
# 平方误差越小 函数约接近真像 平方误差是一个开口向上的一元二次函数
# 函数是我们对事物认知的数学描述
# 梯度下降法
import tensorflow as ten
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
# 设置权重参数
w = 0.1

# 使用最终权重建模
y_pre = w * xs

es = (ys - y_pre) ** 2
sum_e = np.sum(es)
sum_e = (1 / 100) * sum_e
print(sum_e)

ws = np.arange(0, 3, 0.1)
es = []
for w in ws:
    y_pre = w * xs
    e = (1 / 100) * np.sum((ys - y_pre) ** 2)
    es.append(e)

# 绘制title
plt.title("Cost Funcition", fontsize=12)
# 绘制x坐标
plt.xlabel("w")
# 绘制y坐标
plt.ylabel("e")
# 预测函数曲线
plt.plot(ws, es)
# 展示函数
plt.show()

w_min = np.sum(xs * ys) / np.sum(xs * xs)
print("e最小点w:" + str(w_min))
y_pre = w_min * xs
# 绘制title
plt.title("Size-Toxicity Funcition", fontsize=12)
# 绘制x坐标
plt.xlabel("Bean Size")
# 绘制y坐标
plt.ylabel("Toxicity")
# 绘制数据
plt.scatter(xs, ys)
plt.plot(xs, y_pre)
plt.show()
