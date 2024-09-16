#!/bin/bash

FSLDIR=/content/drive/MyDrive/kaggle/fslx
. $FSLDIR/fsl_profile

file=$1
group=$2

BET_OUT=fsl_script/no_skull
FLIRT_OUT=fsl_script/normalized
FAST_OUT=fsl_script/segmented
IMG_OUT=fsl_script/image_output/$group
mkdir -p $BET_OUT
mkdir -p $FLIRT_OUT
mkdir -p $FAST_OUT
mkdir -p $IMG_OUT

filename="${file##*/}"
stripfn=${filename/\.nii/}
new_filename=$(echo "$filename" | sed 's/^.*_\(I.*\)$/\1/')

norm_fn=${stripfn}_norm
bet_fn=${stripfn}_normbrain
newstripfn=${new_filename/\.nii/}
seg_fn=${newstripfn}

#normalize
echo $stripfn begin `date`
#$FSLDIR/bin/flirt -in to_process/$filename -ref $FSLDIR/data/standard/MNI152_T1_1mm.nii.gz -out $FLIRT_OUT/$norm_fn -omat $FLIRT_OUT/$norm_fn.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12 -interp trilinear

#remove skull
#$FSLDIR/bin/bet $FLIRT_OUT/${norm_fn}.nii.gz $BET_OUT/${bet_fn} -f 0.5 -g 0

#segment
#$FSLDIR/bin/fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o $FAST_OUT/${seg_fn} $BET_OUT/${bet_fn}
cp $file $FAST_OUT/${seg_fn}.nii

python3 python/load_save.py $FAST_OUT/${seg_fn}.nii ${seg_fn} $IMG_OUT/
