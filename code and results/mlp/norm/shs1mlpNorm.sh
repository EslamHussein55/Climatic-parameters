#!/bin/bash

#SBATCH --job-name='mlps1N'
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --output=logs1mlpNorm.log
#SBATCH --mem=250GB
#SBATCH --time=13-22

echo "Submitting SLURM job"
singularity exec /software/containers/precip.simg python pys1mlpNorm.py


