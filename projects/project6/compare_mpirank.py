import matplotlib.pyplot as plt

# 数据
mpi_ranks = [1, 2, 4]
speedup = [1.0, 0.76923, 3.98376]
efficiency = [1.0, 0.384615, 0.99594]

# 创建 1行2列子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 子图1：Speedup vs MPI Ranks
ax1.plot(mpi_ranks, speedup, marker='o', color='blue', label='Speedup')
ax1.set_xscale('log', base=2)
ax1.set_xlabel('MPI Ranks')
ax1.set_ylabel('Speedup')
ax1.set_title('Speedup vs MPI Ranks (OMP_THREADS=4)')
ax1.grid(True)
ax1.legend()

# 子图2：Efficiency vs MPI Ranks
ax2.plot(mpi_ranks, efficiency, marker='s', color='green', label='Efficiency')
ax2.set_xscale('log', base=2)
ax2.set_xlabel('MPI Ranks')
ax2.set_ylabel('Efficiency')
ax2.set_title('Efficiency vs MPI Ranks (OMP_THREADS=4)')
ax2.grid(True)
ax2.legend()

# 总标题
fig.suptitle('Strong Scaling Results (MPI Rank) (OMP_THREADS=4)', fontsize=16)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("MPIrank_difference.png")
plt.show()
