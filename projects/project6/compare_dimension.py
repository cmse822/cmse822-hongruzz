import matplotlib.pyplot as plt

# 数据
dimension_labels = ["64x64x64", "128x128x128", "256x256x256", "512x512x512"]
final_time = [46.6423, 1.37155, 0.0810416, 0.00586847]
zone_updates = [4.53, 4.76, 4.33, 3.93]

# 创建 1行2列子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 子图1：Final Time vs Dimension
ax1.plot(dimension_labels, final_time, marker='o', color='blue')
ax1.set_xlabel('Problem Size (Grid Dimension)')
ax1.set_ylabel('Final Time')
ax1.set_title('Final Time vs Problem Size (Weak Scaling)')
ax1.grid(True)

# 子图2：Zone Updates per Second vs Dimension
ax2.plot(dimension_labels, zone_updates, marker='s', color='green')
ax2.set_xlabel('Problem Size (Grid Dimension)')
ax2.set_ylabel('Zone Updates per Second (M)')
ax2.set_title('Zone Updates Rate vs Problem Size (Weak Scaling)')
ax2.grid(True)

fig.suptitle('Weak Scaling Results', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("size_difference.png")
plt.show()
