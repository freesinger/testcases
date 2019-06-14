#include<Eigen/Sparse>
#include<Eigen/Core>
#include<vector>
#include<chrono>
#include<iostream>
using namespace Eigen;
using namespace std;

#define MATRIXSIZE 1000

typedef SparseMatrix<double> SpMat;
typedef Triplet<double> T;
ConjugateGradient<SpMat, Lower|Upper> cg;

SpMat generateSparseMat(int size) {
    vector<T> tripleList;
    tripleList.reserve(size/4);

    for (int i = 0; i < size; i++)
        for (int j = 0; j < size; j++)
            if (rand()%10 < 2) {
                tripleList.push_back(T(i, j, 1));
                tripleList.push_back(T(j, i, 1));
            }

    SpMat M(size, size);
    // sort(tripleList.begin(), tripleList.end());
    // tripleList.erase(unique(tripleList.begin(), tripleList.end()), tripleList.end());
    cout<<"Generating sparse matrix..."<<endl;
    M.setFromTriplets(tripleList.begin(), tripleList.end());
    return M;
}
 

void SequentialProcess(SpMat A, VectorXd x, VectorXd b) {
    cout<<"Sequential processing with 1 core..."<<endl;
    setNbThreads(1);
    // cout<<nbThreads()<<endl;
    auto start = chrono::steady_clock::now();
    cg.compute(A);
    x = cg.solve(b);
    auto end = chrono::steady_clock::now();
    cout<<"Total iteration: "<<cg.iterations()<<endl;
    cout<<"Estimated error: "<<cg.error()<<endl;
    cout<<"Time elapsed: "
        << chrono::duration_cast<chrono::milliseconds>(end-start).count()
        <<" ms"<<endl<<endl;
}


void ParallelProcess(SpMat A, VectorXd x, VectorXd b, int core_num) {
    initParallel();
    setNbThreads(core_num);
    cout<<"Parallel processing with "<<nbThreads()<<" cores...\n";
    auto start = chrono::steady_clock::now();
    cg.compute(A);
    x = cg.solve(b);
    auto end = chrono::steady_clock::now();
    cout<<"Total iteration: "<<cg.iterations()<<endl;
    cout<<"Estimated error: "<<cg.error()<<endl;
    cout<<"Time elapsed: "
        << chrono::duration_cast<chrono::milliseconds>(end-start).count()
        <<" ms"<<endl<<endl;
}


int main(int argc, const char **argv) {
    VectorXd x = VectorXd::Ones(MATRIXSIZE);
    VectorXd b = VectorXd::Ones(MATRIXSIZE);
    SpMat A = generateSparseMat(MATRIXSIZE);

    cg.setMaxIterations(MATRIXSIZE*10);
    cg.setTolerance(1e-3);

    SequentialProcess(A, x, b);
    for (int i = 2; i <= 8; i += 2) {
        if (i == 6) continue;
        ParallelProcess(A, x, b, i);
    }
    // cout<<A<<endl;
    // cout<<b<<endl;
    // cout<<x<<endl;

    return 0;
}