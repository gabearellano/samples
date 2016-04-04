/* Parallel matrix-vector multiplication with 2D block decomposition
 * The last argument is assumed to be the communicator for a 2D Cartesian
 * topology and we assume the matrix a and vector x are already distribtued
 * with the vector x along the rightmost column of processors.
 *
 * Incomplete code provided by Dr. Shirley Moore, debugged and edited by Gabriel Arellano
 */
#include "mpi.h"
#include <stdlib.h>
#include <math.h>
#include <stdio.h>

MatrixVectorMultiply2D(int n, double *a, double *x, double *y, MPI_Comm comm_2d) 
{ 
  int ROW=0, COL=1; /* Improve readability for indices */ 
  int i, j, nlocal; 
  double *py; /* Will store partial dot products for y */
  /* Variables are as follows:
        - npes = # of processing elements 
		- dims = size of matrix in x and y dimensions
		- keep_dims = used to filter out dimensions when creating sub-topologies
  */
  int npes, dims[2], periods[2], keep_dims[2], keep_dims2[2]; 
  /* Other variables are used to create sub-topologies and refer to individual 
	 processing elements */
  int myrank, mycoords[2], mycolrank, myrowrank; 
  int source_rank, dest_rank, root_rank, col_rank, coords[2], coord[1];
  MPI_Status status; 
  MPI_Comm comm_row, comm_col; 

  /* Get information about the communicator */ 
  MPI_Comm_size(comm_2d, &npes); 
  MPI_Comm_rank(comm_2d, &myrank); 

  /* Compute the size of the square grid. If a square grid is not used, 
	 changes the values here */ 
  dims[ROW] = dims[COL] = sqrt(npes); 

  nlocal = n/dims[ROW]; 

  /* Allocate memory for the array that will hold the partial dot-products */ 
  py = malloc(nlocal*sizeof(double)); 

  MPI_Cart_coords(comm_2d, myrank, 2, mycoords); /* Get my coordinates */ 
 
 /*****************************************************/
 /* Create the row-based sub-topology */ 
  keep_dims[ROW] = 0; 
  keep_dims[COL] = 1; 
  MPI_Cart_sub(comm_2d, keep_dims, &comm_row); 
  
  MPI_Comm_rank(comm_row, &myrowrank);
  
  /* Create the column-based sub-topology */ 
  keep_dims2[ROW] = 1;
  keep_dims2[COL] = 0;
  MPI_Cart_sub(comm_2d, keep_dims2, &comm_col);

  MPI_Comm_rank(comm_col, &mycolrank);
  
  /****************************************/
  /* Redistribute the x vector. */ 
  /* Step 1. The processors along the rightmost column send their data to the diagonal processors */ 
  /* If I'm in the rightmost column but not the last row, send my block
     of the vector to the diagonal processor in my row */ 
  /*****************************************************/
  
  /* printf("STEP1: I am processor %d at position (%d, %d)", */
  /* 	 myrank, mycoords[ROW], mycoords[COL]); */
  // determine if in right column
  if (mycoords[COL] == dims[COL]-1){
      // if in right column, then check for !in_final_row
      if (mycoords[ROW] != dims[ROW] - 1){
	  // if not, then send the info to the element located in the
	  //     2d cartesian topology at location (i,j) where i == j.
	  //     Also, i will be equal to mycoords[ROW]
	  // get rank of dest
	  coords[ROW] = coords[COL] = mycoords[ROW];
	  MPI_Cart_rank(comm_2d, coords, &dest_rank);
	  // send to rank
	  MPI_Send(x, nlocal, MPI_DOUBLE, dest_rank, 0, comm_2d);
      }
  }

  /*****************************************************/
  /* If I'm on the diagonal but not in the last row, receive the block
     of the vector from the processor in the rightmost column of my row */

  /* printf("STEP1b: I am processor %d in  at position (%d, %d)", */
  /* 	 myrank, mycoords[ROW], mycoords[COL]); */
  
  if (mycoords[ROW] == mycoords[COL] && mycoords[ROW] != dims[ROW]-1){
      // determine source_rank
      coords[ROW] = mycoords[ROW];
      coords[COL] = dims[COL]-1;
      MPI_Cart_rank(comm_2d, coords, &source_rank);
      // receive data from source
      MPI_Recv(x, nlocal, MPI_DOUBLE, source_rank, 0, comm_2d, &status);
  }

  /*****************************************************/ 
  /* Step 2. Perform a column-wise broadcast with the diagonal process 
             as the root  */ 
  /*******************************************************/
  /* printf("STEP2: I am processor %d at position (%d, %d)", */
  /* 	 myrank, mycoords[ROW], mycoords[COL]); */

  // if diagonal element, just broadcast
  if (mycoords[ROW] == mycoords[COL]){
      MPI_Bcast(x, nlocal, MPI_DOUBLE, mycolrank, comm_col);
  }
  else { 
      // get rank of current column's diagonal element
      coord[0] = mycoords[COL];
      MPI_Cart_rank(comm_col, coord, &col_rank);
      // get column based rank
      
      MPI_Bcast(x, nlocal, MPI_DOUBLE, col_rank, comm_col);
  }
   
  /* Perform local matrix-vector multiply */ 
  for (i=0; i<nlocal; i++) { 
    py[i] = 0.0; 
    for (j=0; j<nlocal; j++) 
      py[i] += a[i*nlocal+j]*x[j]; 
  } 
  /*****************************************************/ 
  /* Step 3. Perform the sum-reduction along the rows to add up the partial 
     dot-products and leave the result in the rightmost column */ 
  /*****************************************************/ 
  /* printf("STEP3: I am processor %d in the right column at position (%d, %d)", */
  /* 	 myrank, mycoords[ROW], mycoords[COL]); */

  // check if this is the results column
  if (mycoords[COL] == dims[COL]-1){
      // receive results from reduce
      MPI_Reduce(py, y, nlocal, MPI_DOUBLE, MPI_SUM, myrowrank, comm_row);
  }
  else{ // pass results to the right
      // determine rank of right-most column processor
      coord[ROW] = dims[ROW]-1;
      MPI_Cart_rank(comm_row, coord, &root_rank);
      MPI_Reduce(py, y, nlocal, MPI_DOUBLE, MPI_SUM, root_rank, comm_row);
  }
  
  /* free local communicators */
  MPI_Comm_free(&comm_row); /* Free up communicator */ 
  MPI_Comm_free(&comm_col); /* Free up communicator */ 
 
  free(py); 
} 
