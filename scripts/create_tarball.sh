#!/bin/bash -f

# A script to basically generate the tarball for SMRS

export tarfile=SMRS_code
rm SMRS_code.tar SMRS_code.tar.gz
export TARDIR=/c/Users/fiona/s2ds/SMRS/SMRS_code
export GITDIR=/c/Users/fiona/s2ds/SMRS
rm -rf $TARDIR
mkdir $TARDIR
cd $TARDIR

# Create arrays to store the top level directory names, university names, list of scripts to copy etc. 
dir_arr=('Raw_data' 'Clean_data' 'scripts' 'models') 
uni_arr=('UWE' 'Teesside' 'ARU' 'OBU' 'Solent')
scriptfile_arr=('clean_merge_feat_eng.sh' 'clean_data_per_uni.py' 'merge_per_uni.py' 'merge_per_uni_feat_eng.py' 'Site_names.xlsx' 'function.py')
modelfile_arr=('apply_model.py'  'ReachSb.p' 'ReachSbPb.p' 'run_prediction.py' 'train_model_1.py' 'train_model_2.py')
merge_arr=('Merged_data.csv')

for dir in ${dir_arr[*]};
do
    mkdir $dir
done

# Create the Raw_data directory structure as an example so SMRS can see where to put

for uni in ${uni_arr[*]};
do
    cd $TARDIR/Raw_data
    mkdir $uni
    cd $uni
    echo "Your raw data files should be placed here with file names e.g. Pivigo_${uni}_Performance.csv[xls] or Pivigo_${uni}_Conversion.csv" > README.txt
done

# Stick text in Clean_data directory
echo "Your cleaned data files will appear in this directory after you've run the cleaning, merging and feature engineering script" > $TARDIR/Clean_data/README.txt
echo "Our final Merged_data.csv file is included in the tarball so that you can test the train_model_1[2].py code if you wish" >> $TARDIR/Clean_data/README.txt
# Copy the final Merged_data.csv file into the Clean_data directory
cp $GITDIR/Clean_data/${merge_arr[0]} $TARDIR/Clean_data/.


# Copy the relevant scripts over from the main repo directory
# Check that the cleaning is enabled in the final tarball
echo "We should check that the cleaning step is enabled in the final tarball"
for scriptfile in ${scriptfile_arr[*]};
do
    cd $TARDIR/scripts
    cp $GITDIR/scripts/$scriptfile .
done

# Copy across the model files
for modelfile in ${modelfile_arr[*]};
do
    cd $TARDIR/models
    cp $GITDIR/models/$modelfile .
done

# Create the tarball
cd $GITDIR
echo "Current dir = " $PWD
tar -cvzf SMRS_code.tar.gz SMRS_code/

# Tidy up
rm -rf $TARDIR
