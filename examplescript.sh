#!/bin/bash
#
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --output=myoutput-%j.txt
#SBATCH --error=QEerr-%j.txt
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --job-name=pwscf
#SBATCH --mail-user=username@uco.edu
#SBATCH --mail-type=ALL

#module load QuantumESPRESSO/6.4.1-intel-2018a
#module load QuantumESPRESSO/5.4.0-intel-2016a
module load QuantumESPRESSO
mpirun pw.x -in filename.in