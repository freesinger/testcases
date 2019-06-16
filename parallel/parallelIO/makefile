all: MPIIO

# -p is optional
MPIIO: MPIIO.cpp
	mpic++ MPIIO.cpp -o MPIIO
	$(info [*] Performing MPI IO using 8 cores...)
	mpirun --oversubscribe -np 8 MPIIO 1000

clean:
	rm -rf mpiio.dat MPIIO