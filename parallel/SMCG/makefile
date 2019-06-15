## On MacOS
# sparseMatrixCG: sparseMatrixCG.cpp
#    /usr/local/opt/llvm/bin/clang++\
#     -fopenmp -L/usr/local/opt/llvm/lib\
#     -std=c++11 sparseMatrixCG.cpp -o sparseMatrix && ./sparseMatrix 1000

## Ubuntu 18.04.2 LTS (GNU/Linux 4.18.0-21-generic x86_64)
#  number of physical processer: 2
#  number of cores / processer: 14
#  number of processes: 56
sparseMatrixCG: sparseMatrixCG.cpp
	g++ -fopenmp sparseMatrixCG.cpp -o sparseMatrixCG && ./sparseMatrixCG 1000

# clean binary files
clean:
	rm -f sparseMatrixCG