import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read GPU data
gpu_df = pd.read_csv('gpu_perf_jac_openmp.csv')
gpu_sizes = gpu_df['Size']
gpu_flops = gpu_df['FLOP/s']

# Read CPU data
cpu_df = pd.read_csv('cpu_perf_jac_openmp.csv')
cpu_threads = cpu_df['Threads']
cpu_sizes = [int(col) for col in cpu_df.columns[1:]]
cpu_flops = cpu_df.iloc[:, 1:].values  # shape: (num_threads, num_sizes)

# Plot 1: FLOP/s vs Matrix Dimension (log-log) for GPU and CPU (best CPU thread count)
plt.figure(figsize=(8,6))
plt.loglog(gpu_sizes, gpu_flops, 'o-', label='GPU', linewidth=2, markersize=6)
best_cpu_idx = np.argmax(cpu_flops, axis=0)
best_cpu_flops = cpu_flops[best_cpu_idx, range(len(cpu_sizes))]
plt.loglog(cpu_sizes, best_cpu_flops, 's--', label='CPU (best thread count)', linewidth=2, markersize=6)
plt.xlabel('Matrix Dimension')
plt.ylabel('FLOP/s')
plt.title('Jacobi Solver Performance: GPU vs CPU (Best)')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.savefig('jacsolv_gpu_vs_cpu_best.png', dpi=300)

# Plot 2: CPU Scaling (FLOP/s vs Threads) for each Matrix Dimension
plt.figure(figsize=(10,7))
for i, size in enumerate(cpu_sizes):
    plt.plot(cpu_threads, cpu_flops[:,i], marker='o', label=f'Size={size:,}')
plt.xlabel('CPU Threads')
plt.ylabel('FLOP/s')
plt.title('CPU Scaling: Jacobi Solver Performance')
plt.xscale('log', base=2)
plt.legend(title='Matrix Dimension', loc='upper left', bbox_to_anchor=(1,1))
plt.grid(True, ls="--")
plt.tight_layout()
plt.savefig('jacsolv_cpu_scaling.png', dpi=300)

# Plot 3: GPU vs CPU (fixed thread counts)
plt.figure(figsize=(8,6))
plt.loglog(gpu_sizes, gpu_flops, 'o-', label='GPU', linewidth=2, markersize=6)
for idx, threads in enumerate(cpu_threads):
    plt.loglog(cpu_sizes, cpu_flops[idx], '--', marker='.', label=f'CPU ({threads} threads)')
plt.xlabel('Matrix Dimension')
plt.ylabel('FLOP/s')
plt.title('Jacobi Solver: GPU vs CPU (All Thread Counts)')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.savefig('jacsolv_gpu_vs_cpu_all.png', dpi=300)

print("Plots saved: jacsolv_gpu_vs_cpu_best.png, jacsolv_cpu_scaling.png, jacsolv_gpu_vs_cpu_all.png")