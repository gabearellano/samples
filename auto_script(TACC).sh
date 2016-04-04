# script automator
# Written by Gabriel R. Arellano (garellano88@gmail.com)
#     This script was created to be used on the SLURM system used by
# the Texas Advanced Computing Center (TACC).
#     As detailed below, using the resource management system requires
# submitting jobs to a queue which eventually get paired up with the
# requested resources (provided the request uses valid values). After
# a job is submitted, the user must wait for their job to be run from
# the queued jobs, then wait for the job to complete, as most free
# allotments only permit 1 job to be queued OR run per free user.
#     The user can keep polling the resource queue to see if their job
# is finished, or receive a text/email about the job completing, as
# some users are using TACC resources for long-running parallelized
# computations. Furthermore, the scripts that interact with SLURM
# directly would have to be edited to change parameters while running
# experiments. These all involved a continued cycle of 1 minute
# interactions and periods of waiting for unknown periods of time.
# This script automates all of that work, and accepts a couple lists
# as parameter inputs and iterates over those parameters to run the
# same experimental code using those values.


# the following script will automate the following (usually performed manually
# by the user):
# - checking if there is a job running for the user, and if none,
# - iterate over different values for input size n and number of processing
#       'nodes',
# - use each combination of values to run an experiment on the supercomputer,
# - sleep while an experiment is running (this is done since only one job was
#       allowed per user, but the system allowed duplicate submissions, with
#       every job submission being ignored while the first was running. 
#       Moreover, jobs could remain queued for any amount of time, between a
#       few seconds to several hours, so sleeping while a job is queued would
#       be equivalent to a user checking the supercomputer's resource mgmt
#       queue intermittently until a new job can be scheduled, i.e. the
#       previous job has completed).

# set variables here
script="runscript"  # name of script for resource mgmt submission
job_name="tdmvm"    # name of C file to run code
myname=$(whoami)    # get custom username from environment
# define the number of desired virtual nodes and input sizes
# n to be used for testing
nodes=(100 100 100 100 100 100 100 100)
ns=(30000 35000 40000 45000 50000 55000 60000 65000)

# repeat experiments some number of times
for i in `seq 0 7`;
do
    # update resource mgmt script with current info
    sed -i -- "s/$job_name[0-9]\+/$job_name${nodes[i]}/g" $script
    sed -i -- "s/-n [0-9]\+/-n ${nodes[i]}/g" $script
    sed -i -- "s/$job_name [0-9]\+/$job_name ${ns[i]}/g" $script
#        echo "About to run the following:"
#        cat $script
#        echo "Press enter to continue"  # optional pause for user input
#        read -s ignored
    sbatch $script
    
    echo "Looping while job is running or waiting"
    # check q for current jobs related to my user
    # | get the last string/line of info
    # | extract the third element in the string separated by spaces
    #   (in this case the third element == number of jobs currently
    #   running or queued)
    job=$(showq -u $myname | tail -1 | awk '{print $3}')
    echo -n "Sleeping now " # sleep while there is a job running or queued
    while [ "$job" -eq "1" ]
    do
    	echo -n ". " # print dots without a newline to display waiting progress
    	sleep 2
    	job=$(showq -u $myname | tail -1 | awk '{print $3}')
    done;
    # once outside the previous while loop, a new job can be scheduled
    echo ""
    echo "Job finished, starting next job"
        # echo "Press enter to continue"  # optional pause for user input
        # read -s ignored
done;
