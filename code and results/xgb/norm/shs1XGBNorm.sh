#!/bin/bash

#SBATCH --job-name='xgbs1N'
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --output=logs12XGBNorm.log
#SBATCH --mem=250GB
#SBATCH --time=13-22

echo "Submitting SLURM job"
singularity exec /software/containers/precip.simg python pys1XGBNorm.py

