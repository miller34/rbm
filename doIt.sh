#! /bin/bash
for i in {1..10}; do for j in {1..10}; do for k in {1..10}; do python rbm.py -i test.data -c 11 -r $k -g 200 -l $i -n $j; done; done; done;
#python rbm.py -i test.data -c 7 -r 1 -g 20 -l 5 -n 4
#filename="$1"
#while read -r line
#do
#	name=$line
#
#	#sbatch analyze_files.sh genes_with_split_sorted/H_sapiens genes_with_split_sorted/$name $newFileName
#	#python combineGenes.py CDS/$line filteredGenes_noException/$name
#	#python getNoException.py filteredGenes_noException/$name filteredGenes_noException/$line
#	#python combineGenes.py CDS/$line genes_with_split/$name
#	#python getNoException.py genes_with_split/$name genes_with_split/$line
#	#bash sortFastaBySeqLen.sh genes_with_split/$name genes_with_split_sorted/$name
#	scancel $name
#	#rm genes_with_split/$name
##	grep -n $name nucleotide_position/Zonotrichia_albicollis >> PLACEIT
##	grep -A 1 $name ONLY_CDS/H_sapiens >> localization
##	sbatch analyze_files.sh $name
##	chmod 770 all_extensions/$name
##	grep 0111 $name
##	python makeCompleteReference.py $name References/$2
##	python makeCompleteReference.py $name CompleteReference/H_sapiens
##	./readFile.py all_extensions/$name all_single_in_fasta_analysis/$name 
##	echo "Name read from file - $name"
##	cat CDS/$name ONLY_CDS/$name > temp/$name
#	echo "Name read from file - $name"
##	python CompleteReference/cleanData.py combinedGenes/$name filteredGenes/$name
#done < "$filename"
#
#
#
#
#
#
#
