#!/bin/bash

########################################################################
# Configuration for sbatch.                                            #
# =======================                                              #
#                                                                      #
# This file is used to specify the arguments for the sbatch program    #
# itself, as well as the program that you want to run on the cluster . #
#                                                                      #
# Jobs will automatically be assigned to machines in our cluster based #
# on how many resources you request.                                   #
#                                                                      #
########################################################################

#SBATCH --comment="This is a comment"                   # OPTIONAL: An arbitrary comment on the job
#SBATCH --job-name="create input file for multi-snippy"        # REQUIRED: Give this job an arbitrary name
#SBATCH --output="%j.out"                               # REQUIRED: Direct STDOUT (normal output) here (file identifier),%j is substituted for the job number, keep this as is, but you can add to before it. E.g. "myjob.%j.out"
#SBATCH --error="%j.err"                                # REQUIRED: Direct STDERR (error output) here (file identifier), %j is substituted for the job number, keep this as is, but you can add to before it. E.g. "myjob.%j.err"
#SBATCH --time=01:00:00                                 # REQUIRED: Maximum time your job can run before it is force terminated. Hr:Min:Sec.
#SBATCH --mem=24G                                       # REQUIRED: Memory required for your job
#SBATCH --requeue                                       # OPTIONAL: On failure, requeue for another try
#SBATCH --verbose                                       # OPTIONAL: Increase informational messages
#SBATCH --export="SOMEVARIABLE=HELLO"                   # OPTIONAL: Set arbitrary environment variables

# Leave the following as is.
if [ x$SLURM_CPUS_PER_TASK == x ]; then
  export OMP_NUM_THREADS=8
else
  export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
fi

# This is the directory where you want to work from for your
# application (where your data is).
cd /usr/people/fdiedericks/Projects/drug_resistant_stat/drug_resistant

echo "Setting up"
echo "===================="
echo ""
echo "Creating VirtualEnv"
echo "--------------------"
echo ""

virtualenv ENV &&
source ENV/bin/activate

echo ""
echo "Installing required dependencies"
echo "--------------------"
echo ""

pip3 install -r dependencies.txt
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ""
echo "=================="
echo "Setup completed"
echo "=================="
echo ""
echo "Run the following command"
echo "export PATH=\"$DIR:\$PATH\""
echo "=================="
echo ""

# IF YOU WANT TO USE TOOLS PACKAGED AS SINGULARITY CONTAINERS:
# ============================================================
# A full example of running the fastqc tool would be something like:
# singularity exec /tools/containers/fastqc/fastqc-0.11.7.simg fastqc <input_data>
#singularity exec /tools/containers/<tool_folder>/<tool_version>.simg <tool_executable> <tool input>

# IF YOU WANT TO USE YOUR OWN SCRIPTS OR TOOLS:
# =============================================
# You can copy your tool to queue and use it with your data through slurm.
# Assuming you're using a Python3 script:
#python3 test.py <test.py input>
python3 main.py 
