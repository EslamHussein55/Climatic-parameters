#!/bin/bash

#SBATCH --job-name='knn2N'
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --output=logs2KnnNorm.log
#SBATCH --mem=250GB
#SBATCH --time=13-22

echo "Submitting SLURM job"
singularity exec /software/containers/precip.simg python pys2KnnnNorm.py

