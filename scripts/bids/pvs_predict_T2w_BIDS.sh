#!/bin/bash

# nnUNetv2 for the segmentation of perivascular spaces in BIDS standardised T2w MRI datasets
# Author: William Pham
# Date: 2025-03-04
# Description: This script runs a nnUNet to label perivascular spaces in T2w MRI scans.
# Usage:
# Modify the script to include the INPUT_DIR and OUTPUT_DIR arguments, then run script:
# ./pvs_predict_T2w.sh

# Input directory containing raw T2w images for inference
# T2w images should end with "_0000.nii.gz"
INPUT_DIR=""

# Output directory where PVS masks and model predictions will be outputs
OUTPUT_DIR=""

# Find all T1 images and run inference
cd $INPUT_DIR
pvs_queue=($(find -type f -name '*T2w.nii.gz'))

for i in "${pvs_queue[@]}"; do
    echo $i
    base=$(basename $i)
    if [ ! -f "${OUTPUT_DIR}/${base}" ]
    then
	TD=$(mktemp -d) || exit 1
	trap 'rm -rf ${TD}' RETURN
	
	new_name="${base%.nii.gz}_0000.nii.gz"

	cp ${i} ${TD}/${new_name}

	nnUNetv2_predict -d Dataset993_PVST2 -i ${TD} -o ${OUTPUT_DIR} -f all -tr nnUNetTrainer -c 3d_fullres -p nnUNetResEncUNetMPlans

	rm -rf ${TD}
    fi
done
