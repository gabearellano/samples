"""
Author:Gabriel Arellano

Advanced Algorithms - Fall 2014 - UTEP
Prof: Dr Longpre

A class I created to help keep track of the timing of my recursiveFFT
algorithm for the course project. It will track a series of
experiments into one object, with an array for each datapoint. In this
case, I had to keep track of two start/stop timings and an input size,
so there are five arrays in the TimeDict object.

I noticed that I have to keep the timing of two distinct windows of
time, as well as the size of the input.

"""

import sys

class TimeDict:
    def __init__(self):
        self.start0 = []
        self.end0 = [] 
        self.start1 = []
        self.end1 = []
        self.n = []
        
    def add(self, start_zero, end_zero, start_one, end_one, lngth):
        """add one set of data points from one experimental run"""
        if self.data_ready_for_append():
            self.start0.append(start_zero)
            self.end0.append(end_zero) 
            self.start1.append(start_one)
            self.end1.append(end_one)
            self.n.append(lngth)
        else:
            ## light error checking
            print "Something went wrong, lists of unequal length.", \
                "Some data is missing so the remaining data", \
                "appended would not be valid."
            sys.stdout.flush()
            sys.exit(1) # exit since there's a problem

    def print_results(self, output_on=True, save_data=False):
        """print_results can either print to stdout, a file, or both"""
        out_file = None
        if save_data:
            out_file = open("overhead_stats.csv", 'w')
        for i in xrange(len(self.start0)):
            total_time = repr(float(self.end0[i] - self.start0[i]) + \
                         float(self.end1[i] - self.start1[i]))
            if output_on:
                print "Number of elements:", self.n[i], \
                    " | Total time spent:", repr(total_time)
            if save_data:
                out_string = str(self.n[i]) + ","+ \
                             str(total_time)+ "\n"
                out_file.write(out_string)
        if save_data:
            out_file.close()
            
    def print_and_write_results(self):
        """wrapper for print_results, causes data to save to file"""
        self.print_results(save_data=True)
    
    def write_results(self):
        """wrapper for print_results, writes to file, not stdout"""
        self.print_results(output_on=False, save_data=True)

    def data_ready_for_append(self):
        """
        checks if all object lists are equal length, i.e. that the
        object still has a valid state.
        """
        return len(self.start0) == len(self.end0) == \
            len(self.start1) == len(self.end1)
