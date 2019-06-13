#include<Eigen/Sparse>
#include<mpi.h>
#include<vector>
#include<iostream>
using namespace Eigen;
using namespace std;

#define MATRIXSIZE 10000

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
    M.setFromTriplets(tripleList.begin(), tripleList.end());
    return M;
}

int main(int argc, const char **argv) {
    VectorXd x = VectorXd::Random(100);
    VectorXd b = VectorXd::Random(100);
    SpMat A = generateSparseMat(100);
    /* 
    // a strong restriction is that the storage orders must match
    SpMat mat = generateSparseMat(10);
    SpMat temp = SpMat(mat.transpose()) + mat;
    cout<<temp<<endl;
    */
    cout<<A<<endl;
    cout<<b<<endl;
    cout<<x<<endl;

    cg.compute(A);
    x = cg.solve(b);
    cout<<x<<endl;
    cout<<"#iteration: "<<cg.iterations()<<endl;
    cout<<"estimated error: "<<cg.error()<<endl;

    x = cg.solve(b);

    cout<<x<<endl;
    // cout<<A.transpose()*A<<endl;
    return 0;
}