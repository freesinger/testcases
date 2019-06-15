#include <iostream>
#include <cmath>
#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <sys/time.h>
#include <mpi.h>
using namespace std;

#define epsilon 1.e-8

int main(int argc, char **argv)
{
	/* Parameters from command line */
    string T, P, Db;

	/* Time parameters */
	double elapsedTime, elapsedTime2;
  	timeval start, end, end2;

	/* MPI initial parameters */
	int id, nproc;
	MPI_Status status;
	MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nproc);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);
	int M = atoi(argv[1]);
	int N = atoi(argv[2]);
	
	if (argc > 3)
		T = argv[3];
		if (argc > 4)
			P = argv[4];
			if (argc > 5)
				Db = argv[5];
	// cout<<T<<P<<endl;


	/* Matrices type initialization */
	double **U_t;
	double alpha, beta, gamma, **Alphas, **Betas, **Gammas;

	int acum = 0;
	int temp1, temp2;
	
	U_t = new double*[N];
	Alphas = new double*[N];
	Betas = new double*[N];
	Gammas = new double*[N];

	for(int i = 0; i < N; i++) {
		U_t[i] = new double[N];
		Alphas[i] = new double[N];
		Betas[i] = new double[N];
		Gammas[i] = new double[N];
	}


	/* READ matrix and store in U_t */
	ifstream matrixfile("matrix");
	if (!(matrixfile.is_open())) {
		cout<<"Error: file not found"<<endl;
		return 0;
	}

	for (int i = 0; i < M; i++)
		for (int j = 0; j < N; j++)
			matrixfile >> U_t[i][j];

	matrixfile.close();


	/* Reductions with MPI */
	gettimeofday(&start, NULL);

	double values[3]; // for storing matrices mul temp results
	for (int i = 0; i < M; i++) {
		for (int j = 0; j < M; j++) {
			alpha =0.0;
			beta = 0.0;
			gamma = 0.0;
			for (int k = 0; k < N; k++) {
				values[0] = U_t[i][k] * U_t[i][k];
				values[1] = U_t[j][k] * U_t[j][k];
				values[2] = U_t[i][k] * U_t[j][k];
				if (id != 0) {
					MPI_Send(values, 3, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD);
				} else {
					for (int id = 1; id < nproc; id++) {
						MPI_Recv(values, 3, MPI_DOUBLE, id, 1, MPI_COMM_WORLD, &status);
						alpha += values[0];
						beta += values[1];
						gamma += values[2];
					}
				}
			}
			/*  
			// Values are stored in root(id = 0) processor
			if (id == 0) {
				Alphas[i][j] = alpha;
				Betas[i][j] = beta;
				Gammas[i][j] = gamma;
			}
			*/
			// Global variables
			Alphas[i][j] = alpha;
			Betas[i][j] = beta;
			Gammas[i][j] = gamma;
		}
	}

	gettimeofday(&end, NULL);


	/* Fix final result */
	if (id == 0) { // no need for specify id here
		// Time elapsed
		if (T == "-t" || P == "-t") {
			elapsedTime = (end.tv_sec - start.tv_sec) * 1000.0;
			elapsedTime += (end.tv_usec - start.tv_usec) / 1000.0;
			cout<<"Time elapesd: "<<elapsedTime<<" ms"<<endl<<endl;
		}

		// Print matrices for debug
		if (T == "-p" || P == "-p") {
			cout<<"Alphas: "<<endl<<endl;
			for (int i = 0; i < M; i++)
				for (int j = 0; j < M; j++)
					cout<<Alphas[i][j]<<"  ";
				// cout<<endl;
			
			cout<<"Betas: "<<endl<<endl;
			for (int i = 0; i < M; i++)
				for (int j = 0; j < M; j++)
					cout<<Betas[i][j]<<"  ";
				// cout<<endl;

			cout<<"Gammas: "<<endl<<endl;
			for (int i = 0; i < M; i++)
				for (int j = 0; j < M; j++)
					cout<<Gammas[i][j]<<"  ";
				// cout<<endl;
		}

		// Generate files for debug purpouse
		if(Db == "-d" || T == "-d" || P == "-d") {
			ofstream Af;
			//file for Matrix A
			Af.open("AlphasMPI.mat"); 
			/* Af<<"# Created from debug\n# name: A\n# type: matrix\n# rows: "<<M<<"\n# columns: "<<N<<"\n";*/
			// Af<<M<<"  "<<N;
			for(int i = 0; i < M; i++) {
				for(int j = 0; j < N; j++)
					Af<<" "<<Alphas[i][j];
				Af<<'\n';
			}
			Af.close();

			ofstream Uf;
			//File for Matrix U
			Uf.open("BetasMPI.mat");
			/* Uf<<"# Created from debug\n# name: Ugpu\n# type: matrix\n# rows: "<<M<<"\n# columns: "<<N<<"\n";*/
			for(int i = 0; i < M; i++) {
				for(int j = 0; j < N; j++)
					Uf<<" "<<Betas[i][j];
				Uf<<'\n';
			}
			Uf.close();

			ofstream Vf;
			//File for Matrix V
			Vf.open("GammasMPI.mat");
			/* Vf<<"# Created from debug\n# name: Vgpu\n# type: matrix\n# rows: "<<M<<"\n# columns: "<<N<<"\n";*/
			for(int i = 0; i < M; i++) {
				for(int j = 0; j < N; j++)
					Vf<<" "<<Gammas[i][j];
				Vf<<'\n';
			}
			Vf.close();

			ofstream Sf;
		}
	}

	/* Memory free */
	for(int i = 0; i < N; i++) {
		delete [] Alphas[i];
		delete [] U_t[i];
		delete [] Betas[i];
		delete [] Gammas[i];
	}
	
	delete [] Alphas;
	delete [] U_t;
	delete [] Betas;
	delete [] Gammas;

	MPI_Finalize();

    return 0;
}