#!/bin/bash

#SBATCH --job-name='svrs1N'
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --output=logs1SVRNorm.log
#SBATCH --mem=250GB
#SBATCH --time=13-22

echo "Submitting SLURM job"
singularity exec /software/containers/precip.simg python pys1SVRNorm.py


