#!/bin/bash
# filepath: /mnt/home/scouch/cmse822/cmse822-codex-private/projects/project4/perfStudy.sh

# Performance study script for vecadd.cpp and jacsolv
# Tests performance of vector addition on GPU and CPU

# Exit on error
set -e

# Output files
GPU_LOG="gpu_perf_jac_openmp.csv"
CPU_LOG="cpu_perf_jac_openmp.csv"

# Clean up previous files
rm -f jacsolv_cpu_openmp jacsolv_gpu_openmp $GPU_LOG $CPU_LOG

echo "Starting performance study..."

# --- GPU Testing ---
echo "Building for GPU execution..."
nvc++ -O2 -mp=gpu -gpu=ccnative -o jacsolv_gpu_openmp jacsolv_openmp.cpp

echo "Running GPU tests with varying vector sizes..."
echo "Size,FLOP/s" > $GPU_LOG

# collect GPU sizes
declare -a GPU_SIZES=()

# Test increasing powers of 2 for vector sizes
# Starting with 2^20 (about 1M elements)
for power in {5..12}; do
    size=$((2**power))
    echo "Testing GPU with vector size = $size"
    
    # Run program with size argument
    output=$(./jacsolv_gpu_openmp $size 2>&1) || {
        echo "Error at size $size - likely reached GPU memory limit"
        # Save the last successful size for CPU tests
        last_successful_size=$((2**(power-1)))
        break
    }
    
    # Extract FLOP/s using grep
    flops=$(echo "$output" | grep "FLOP rate:" | awk '{print $3}')
    
    if [[ -n "$flops" ]]; then
        echo "$size,$flops" >> $GPU_LOG
        GPU_SIZES+=("$size")
        echo "  FLOP/s: $flops"
    else
        echo "  Warning: Could not extract FLOP/s measurement"
    fi
done

# If we didn't set last_successful_size due to no failures
if [[ -z "$last_successful_size" ]]; then
    last_successful_size=$((2**power))
fi

echo "GPU tests complete. Results saved to $GPU_LOG"

# --- CPU Testing ---
echo "Building for CPU execution..."
nvc++ -O2 -mp=multicore -o jacsolv_cpu_openmp jacsolv_openmp.cpp

# prepare headers with GPU sizes
header="Threads"
for size in "${GPU_SIZES[@]}"; do
    header+=",$size"
done

echo "$header" > $CPU_LOG

for power in {0..5}; do
    threads=$((2**power))
    echo "Testing CPU with $threads threads"
    export OMP_NUM_THREADS=$threads
    line="$threads"
    for size in "${GPU_SIZES[@]}"; do
        output=$(./jacsolv_cpu_openmp $size 2>&1)
        flops=$(echo "$output" | grep "FLOP rate:" | awk '{print $3}')
        if [[ -n "$flops" ]]; then
            line+=",$flops"
        else
            line+=",0"
        fi
    done
    echo "$line" >> $CPU_LOG
done

# Clean up environment
unset OMP_NUM_THREADS

echo "CPU tests complete. Results saved to $CPU_LOG"
echo "Performance study completed successfully."
echo ""
echo "GPU results: $GPU_LOG"
echo "CPU results: $CPU_LOG"
echo ""
echo "Use these CSV files to create performance plots."