#!/bin/bash

#Submit this script with: sbatch thefilename

#SBATCH --time=2:00:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=1G   # memory per CPU core
#SBATCH -J "average"   # job name
##SBATCH --qos=test

# Compatibility variables for PBS. Delete if not needed.
export PBS_NODEFILE=`/fslapps/fslutils/generate_pbs_nodefile`
export PBS_JOBID=$SLURM_JOB_ID
export PBS_O_WORKDIR="$SLURM_SUBMIT_DIR"
export PBS_QUEUE=batch


# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

#python discretecounts.py $1

for j in {1..10}; do for k in {1..10}; do python rbm.py -i test.data -c 11 -r $k -g 200 -l 10 -n $j; done; done;

##python codonfrequency.py gff3_parser/filteredGenes_noException/$1 gff3_parser/codon_bias_noException/$1
#python calculatecub.py $1
#python comparevirusprot.py $1
#./doIt.sh $1

#input="CDS/"$1
#output="ONLY_CDS/"$1$1
#out2="ONLY_CDS/"$1


#awk '!a[$0]++' $input >$output
#python eraseHeaders.py $output $out2
#rm $output
#python gff3_parser.py ../../ALL_genomes/H_sapiens/GFF/ref_GRCh38_scaffolds.gff3.gz H_sapiens
#python gff3_parser.py $1 $2

#./doIt.sh $1


exit 0
