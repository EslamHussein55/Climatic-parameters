#!/bin/bash

#SBATCH --job-name='knn2A'
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --output=logs2KnnAve.log
#SBATCH --mem=250GB
#SBATCH --time=13-22

echo "Submitting SLURM job"
singularity exec /software/containers/precip.simg python pys2KnnAve.py

