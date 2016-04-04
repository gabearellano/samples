# samples
This repo contains samples of code I've written for various purposes
in various languages, including: Python, C/C++, Prolog, Haskell, and a
shell script.

## Fourier Transformations - Python (fourier.py)
This file contains an implementation of a Fast Fourier Transformation
(FFT) and a Discrete Fourier Trnasformation (DFT), which are used to
multiply two polynomials in the form of:
   a_0 * x^n + a_1 * x^(n-1) + .... + a_(n-1) * x + a_n

The polynomials are passed in as 2 lists of coefficients, with the
first element of each list belonging to the coefficient of the term
with the largest power of x (or the leftmost coefficient in the
formula above).

Additionally, this assignment required evaluating when switching from
the optimal FFT algorithm to the less than optimal DFT algorithm,
which on my machine was when the polynomial had 64 terms or less. A
report detailing this investigation and my implementations can be
found in the file Fourier_report.pdf, which is also in this repo.

(timeDict.py)
This file contains a simple Python object for keeping track of data
collected while running timing experiments with fourier.py.

(fourier_test.py)
This file contains a small script for testing fourier.py.


## Sudoku solver - Prolog (sudoku_solver.prolog)
In Prolog, it is easy to represent an entire Sudoku board as an array,
using anonymous variables for blank spaces. This code solves such
puzzles, provided one as input.

## The Shortest Path Problem - Haskell (floyd_warshall.hs)
With a weighted graph, there are several algorithms for calculating
the shortest path between two vertices. Djikstra's algorithm is widely
used, however it was avoided in class due to the potential for
cheating from online sources covering the algorithm. In its place, I
implemented the Floyd-Warshall algorithm. There are some other methods
in the file which were also part of the assignment. For a complete
description of all of the methods in this file, please refer to
floyd_warshall_report.pdf.

## Parallelized 2D Matrix and Vector Multiplication - C, MPI (tdmvm.c)
This file contains an example using MPI to multiply a 2-dimensional
matrix and a vector. MPI is used in this example, using a cartesian
topography to broadcast and parallelize the computation, as well as
gather results.

## Automating Command Line Interactions - shell script (auto_script.sh)
While using the SLURM, which manages resources for the Texas Advanced
Computing Center (TACC), I came across a specific command line
interaction problem that was consuming my time. TACC permits most
users only one job, which may not get executed immediately, and
further jobs cannot be enqueued until the previous job is
completed. To know when a job completes, a user can either check the
queue while logged in, or can receive a text or email notifying them
about the completed job. This means that a user can wait a very
indeterminate amount of time for their job to complete, and must
either receive constant notifications to rush back to their command
line console or keep polling the queue to see when their last job
finished.

I had to run several experiments on Stampede, one of TACC's
supercomputer systems, and I did not want to spend time on something
that could be automated. So I created a script which would use two
hard-coded arrays containing all of my experiment parameters. The
script would check TACC's work queue for a current job, and if none
was found, would use the next defined parameter to run a job on
Stampede. After running a job, the script would sleep and poll the job
queue for running jobs (since I was only allowed one at a time). Once
the amount of current jobs returned to zero (or was not one, at
least), the next parameters would be used for the next experiment.

This saved me several hours of either sitting in front of my computer
or returning to it from notifications, and the script only took me
about 30 minutes to complete, and was reusable on multiple
assignments.