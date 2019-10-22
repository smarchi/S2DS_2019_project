#!/bin/bash -f

uni_arr=('UWE' 'Teesside')

### If you want to run the other 5 unis (or adding more), uncomment the line below
# uni_arr=('UWE' 'Teesside' 'ARU' 'OBU' 'Solent')

if [ -f "../Clean_data/Merged_data.csv" ]; then
	echo "##########################################"
	echo "Removing old Merged_data.csv file!"
	echo "##########################################"
	echo ''
    rm ../Clean_data/Merged_data.csv
fi

for uni in ${uni_arr[*]};
do

	echo "########################################"
	echo "Cleaning performance/conversion for $uni"
	echo "########################################"
	echo ''
	python clean_data_per_uni.py $uni
	
	echo "########################################"
	echo "Appending $uni to merge script"
	echo "########################################"
	echo''
	python merge_per_uni.py $uni

done

echo "########################################"
echo "Feature engineering on new merge script"
echo "########################################"
python merge_per_uni_feat_eng.py
