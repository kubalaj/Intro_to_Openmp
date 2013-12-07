/*LAB 2 PAUL KUBALA
Used Collaboration with Chris Yarish To Complete
Assignment
 */
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <sys/time.h>
#include <cstring>
#include <cassert>
#include <hdf5.h>
#include<algorithm>
#include<omp.h>
namespace util
{

  void read_hdf(const std::string &filename, double* &data, int &m_rows, int &m_cols){

    hid_t file_id, dataset_id, space_id, property_id;
    herr_t status;

    //Create a new file using the default properties.
    file_id = H5Fopen (filename.c_str(), H5F_ACC_RDONLY, H5P_DEFAULT);
    dataset_id = H5Dopen(file_id, "x", H5P_DEFAULT);
    space_id = H5Dget_space(dataset_id);
    int length = H5Sget_simple_extent_npoints(space_id);
    hsize_t dims[2];
    hsize_t mdims[2];
    status = H5Sget_simple_extent_dims(space_id,dims,mdims);
    m_rows = dims[0];
    m_cols = dims[1];
    
    data = new double[length];
    status = H5Dread(dataset_id, H5T_NATIVE_DOUBLE, H5S_ALL, H5S_ALL,
		     H5P_DEFAULT, data);

    status = H5Sclose(space_id);
    status = H5Dclose(dataset_id);
    status = H5Fclose(file_id);

  }

  void write_hdf(const std::string &filename, double* &data, int &m_rows, int &m_cols){

    hid_t file_id, dataset_id, space_id, property_id;
    herr_t status;

    hsize_t dims[2] = {m_rows,m_cols};
   
    
    //Create a new file using the default properties.
    file_id = H5Fcreate (filename.c_str(), H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);

    //Create dataspace. Setting maximum size to NULL sets the maximum
    //size to be the current size.
    space_id = H5Screate_simple (2, dims, NULL);

    //Create the dataset creation property list, set the layout to compact.
    property_id = H5Pcreate (H5P_DATASET_CREATE);
    status = H5Pset_layout (property_id, H5D_CONTIGUOUS);

    // Create the dataset.
    dataset_id = H5Dcreate (file_id, "x", H5T_NATIVE_DOUBLE, space_id, H5P_DEFAULT, property_id, H5P_DEFAULT);
   
    //Write the data to the dataset.
    status = H5Dwrite (dataset_id, H5T_NATIVE_DOUBLE, H5S_ALL, H5S_ALL, H5P_DEFAULT, data);

    status = H5Sclose(space_id);
    status = H5Dclose(dataset_id);
    status = H5Fclose(file_id);
    status = H5Pclose(property_id);

  }

};


int main(int argc,char* argv[]){
  // Take Input Of First File or Matrix
  std::string matrixA=argv[1];
 std::string matrixB=argv[2];
 std::string matrixC=argv[3];
 double* input_1=0;
  double* input_2=0;
  
  int threadID;
  int numthreads;
  int row = 0;
  int column = 0;

  std::cout.precision(8);
  
 util::read_hdf(matrixA, input_1,row,column); 


  // Matrix
  int row2=0;
  int column2=0;

 util::read_hdf(matrixB, input_2,row2,column2);

  double* end_matrix=0;
  end_matrix = new double[row*column2];
  // Array Multiple Function

  int mm = 0;
  int nn = 0;
  int kk =0;
  int M = row;
  int N = column2;
  int K = column;

  #pragma omp parallel private(mm)
{
  
  threadID = omp_get_thread_num();
printf("ThreadID %d\n", threadID);
  if(threadID == 0 ){
    numthreads = omp_get_num_threads();
    printf("Total number task %d\n", numthreads);
  }
#pragma omp for   
	for(mm = 0; mm < M; mm++){
	  for(nn = 0; nn < N; nn++){
	    int index3 = mm*N + nn;
	    for(kk = 0; kk < K; kk++){
	      int index1 = mm*K + kk;
	      int index2 = kk*N + nn;	      
	      end_matrix[index3] += input_1[index1]*input_2[index2];
		  }}}
}


 
  util::write_hdf(matrixC, end_matrix,row,column2);

  // Testing for loop to see if 
  // enough iterations are being done
  // std::cout << counter;

  // Delete all input data and array
  // for next use of the code
  delete[] input_1;
  delete[] input_2;
  delete[] end_matrix;
  return 0;
}
