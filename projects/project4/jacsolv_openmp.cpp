#include <omp.h>

#include <cmath>
#include <cstdlib>  // for std::atoi and std::rand
#include <iostream>
#include <vector>

#include "mm_utils.hpp"

// Constants defined as in the original program.
constexpr double TOLERANCE = 0.001;
constexpr int DEF_SIZE = 1000;
constexpr int MAX_ITERS = 100000;
constexpr double LARGE = 1000000.0;

int main(int argc, char **argv) {
    int Ndim;  // Matrix A is Ndim x Ndim.
    int iters;
    double start_time, elapsed_time;
    TYPE err, chksum;

    // Set matrix dimensions based on command line argument.
    if (argc == 2) {
        Ndim = std::atoi(argv[1]);
    } else {
        Ndim = DEF_SIZE;
    }
    std::cout << "ndim = " << Ndim << std::endl;

    // Allocate matrices/vectors using std::vector.
    std::vector<TYPE> A(Ndim * Ndim);
    std::vector<TYPE> b(Ndim);
    std::vector<TYPE> xnew(Ndim);
    std::vector<TYPE> xold(Ndim);

    // Generate a diagonally dominant matrix (was defined in mm_utils.h).
    initDiagDomNearIdentityMatrix(Ndim, A.data());

#ifdef VERBOSE
    // Optionally print the matrix (if VERBOSE is defined)
    std::cout << "Matrix A (first 10x10 block):\n";
    int maxPrint = std::min(Ndim, 10);
    for (int i = 0; i < maxPrint; ++i) {
        for (int j = 0; j < maxPrint; ++j) {
            std::cout << A[i * Ndim + j] << ' ';
        }
        std::cout << '\n';
    }
#endif

    // Initialize xnew, xold, and b.
    for (int i = 0; i < Ndim; ++i) {
        xnew[i] = static_cast<TYPE>(0.0);
        xold[i] = static_cast<TYPE>(0.0);
        // b gets some non-zero random values between 0 and 0.5.
        b[i] = static_cast<TYPE>(std::rand() % 51) / 100.0;
    }

    // Setup pointers to the vector data
    auto *xnew_dat = xnew.data();
    auto *xold_dat = xold.data();
    auto *A_dat = A.data();
    auto *b_dat = b.data();

    // Start the timer.
    start_time = omp_get_wtime();

    std::cout << "Max number of threads: " << omp_get_max_threads() << "\n";

    // Jacobi iterative solver on device with persistent data region
    TYPE conv = LARGE;
    

    // Persistent data region to reduce data movement
    #pragma omp target data map(to: A_dat[0:Ndim*Ndim], b_dat[0:Ndim]) \
                            map(tofrom: xold_dat[0:Ndim], xnew_dat[0:Ndim])
    {   
        iters = 0;
        while (conv > TOLERANCE && iters < MAX_ITERS) {
            ++iters;

            // Compute new x values
            #pragma omp target loop
            for (int i = 0; i < Ndim; ++i) {
                TYPE sum = TYPE{0};
                for (int j = 0; j < Ndim; ++j) {
                    if (i != j) {
                        sum += A_dat[i * Ndim + j] * xold_dat[j];
                    }
                }
                xnew_dat[i] = (b_dat[i] - sum) / A_dat[i * Ndim + i];
            }

            // Compute convergence norm
            conv = TYPE{0};
            #pragma omp target loop map(tofrom : conv)
            for (int i = 0; i < Ndim; ++i) {
                TYPE d = xnew_dat[i] - xold_dat[i];
                conv += d * d;
            }

            // Swap buffers on device
            #pragma omp target loop
            for (int i = 0; i < Ndim; ++i) {
                TYPE tmp = xold_dat[i];
                xold_dat[i] = xnew_dat[i];
                xnew_dat[i] = tmp;
            }
        }
    } // end of target data

    elapsed_time = omp_get_wtime() - start_time;
    std::cout << "Convergence = " << static_cast<float>(conv) << " with "
              << iters << " iterations and " << static_cast<float>(elapsed_time)
              << " seconds\n";

    // Calculate and print FLOP/s
    double totalFlops = 2.0 * static_cast<double>(Ndim) *
                        static_cast<double>(Ndim) * static_cast<double>(iters);
    double flopsPerSecond =
        (elapsed_time > 0) ? totalFlops / elapsed_time : 0.0;
    std::cout << "FLOP rate: " << flopsPerSecond << " FLOP/s \n";

    // After the Jacobi iteration loop
    // Add this line to ensure the solution is in xnew for the validation step
    std::swap(xold, xnew);

    // Test the computed solution by multiplying A by the solution vector
    // (stored in xnew) and comparing with the original right-hand side vector b.
    err = static_cast<TYPE>(0.0);
    chksum = static_cast<TYPE>(0.0);
    for (int i = 0; i < Ndim; ++i) {
        xold[i] = static_cast<TYPE>(0.0);
        for (int j = 0; j < Ndim; ++j) xold[i] += A[i * Ndim + j] * xnew[j];
        TYPE tmp = xold[i] - b[i];
#ifdef DEBUG
        std::cout << " i=" << i << ", diff=" << static_cast<float>(tmp)
                  << ", computed b=" << static_cast<float>(xold[i])
                  << ", input b=" << static_cast<float>(b[i]) << "\n";
#endif
        chksum += xnew[i];
        err += tmp * tmp;
    }
    err = static_cast<TYPE>(std::sqrt(err));
    std::cout << "jacobi solver: err = " << static_cast<float>(err)
              << ", solution checksum = " << static_cast<float>(chksum) << "\n";
    if (err > TOLERANCE)
        std::cout << "\nWARNING: final solution error > " << TOLERANCE
                  << "\n\n";

    return 0;
}
