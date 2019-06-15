all: matrix Reduction randomRedMPI Validation_mpi


matrix: Random_matrix.py
	$(info [*] Constructing symmetric matrix with size 200 * 200...)
	python Random_matrix.py 200 200


Reduction: Reduction.cpp
	$(info [*] Performing orignal reduction...)
	g++ Reduction.cpp -o Reduction && ./Reduction 200 200 -t -d


randomRedMPI: randomRedMPI.cpp
	$(info [*] Random reduction with MPI...)
	mpic++ randomRedMPI.cpp -o randomRedMPI && mpirun -np 2 ./randomRedMPI 200 200 -t -d


Validation_mpi: Validation_mpi.cpp
	$(info [*] Validating...)
	g++ Validation_mpi.cpp -o Validation_mpi && ./Validation_mpi -p

clean:
	rm -f matrix Reduction randomRedMPI Validation_mpi *.mat

