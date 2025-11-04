#!/bin/bash

# nnUNetv2 for the segmentation of perivascular spaces in T2w MRI
# Author: William Pham
# Date: 2025-11-04
# Description: This script runs a nnUNet to label perivascular spaces in T2w MRI scans.
# Usage:
# Modify the script to include the INPUT_DIR and OUTPUT_DIR arguments, then run script:
# ./pvs_predict_T2w.sh

# Input directory containing raw T2w images for inference
# T2w images should end with "_0000.nii.gz"
INPUT_DIR=""

# Output directory where PVS masks and model predictions will be outputs
OUTPUT_DIR=""

nnUNetv2_predict -d Dataset705_PVST2 -i ${INPUT_DIR} -o ${OUTPUT_DIR} -f all -tr nnUNetTrainer -c 3d_fullres -p nnUNetResEncUNetMPlans
