import matplotlib.pyplot as plt

# 数据
threads = [1, 2, 4, 8, 16, 32]
speedup = [1.0, 1.555, 2.38, 2.975, 3.39, 3.585]
efficiency = [1.0, 0.7775, 0.595, 0.371875, 0.211875, 0.11203125]

# 创建 1行2列的子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 子图1：Speedup vs Threads
ax1.plot(threads, speedup, marker='o', color='blue', label='Speedup')
ax1.set_xscale('log', base=2)
ax1.set_xlabel('Threads')
ax1.set_ylabel('Speedup')
ax1.set_title('Speedup vs Threads')
ax1.grid(True)

# 子图2：Efficiency vs Threads
ax2.plot(threads, efficiency, marker='s', color='green', label='Efficiency')
ax2.set_xscale('log', base=2)
ax2.set_xlabel('Threads')
ax2.set_ylabel('Efficiency')
ax2.set_title('Efficiency vs Threads')
ax2.grid(True)

# 总标题
fig.suptitle('Strong Scaling Results (OPENMP): Speedup and Efficiency', fontsize=16)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # 给总标题留空间
plt.savefig("OPENMP_difference.png")
plt.show()

