#include<Eigen/Sparse>
#include<mpi.h>
#include<vector>
#include<iostream>
using namespace Eigen;
using namespace std;

typedef SparseMatrix<double> SpMat;
typedef Triplet<double> T;

SpMat generateSparseMat(int size) {
    vector<T> tripleList;
    tripleList.reserve(size/4);

    for (int i = 0; i < size; i++)
        for (int j = 0; j < size; j++)
            if ((i+j) == (size-1) || (i+j) == (size-6))
                tripleList.push_back(T(i, j, rand()%10+1));

    SpMat A(size, size);
    A.setFromTriplets(tripleList.begin(), tripleList.end());
    return A;
}

int main(int argc, const char **argv) {

    // a strong restriction is that the storage orders must match
    SpMat mat = generateSparseMat(10);
    SpMat temp = SpMat(mat.transpose()) + mat;
    cout<<temp<<endl;

    
    cout<<mat.transpose()*mat<<endl;
    return 0;
}