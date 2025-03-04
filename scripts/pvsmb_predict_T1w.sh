#!/bin/bash

# nnUNetv2 for the segmentation of perivascular spaces in midbrain T1w MRI scans
# Author: William Pham
# Date: 2025-03-04
# Description: This script runs a nnUNet to label perivascular spaces in midbrain extracted T1w MRI scans.
# Usage:
# Modify the script to include the INPUT_DIR and OUTPUT_DIR arguments, then run script:
# ./pvsmb_predict_T1w.sh

# Input directory containing midbrain extracted T1w images
# Regions outside the midbrain should be masked out
# T1w images should end with "_0000.nii.gz"
INPUT_DIR=""

# Output directory where PVS masks and model predictions will be outputs
OUTPUT_DIR=""

nnUNetv2_predict -d Dataset774_PVSMB -i ${INPUT_DIR} -o ${OUTPUT_DIR} -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_fullres -p nnUNetResEncUNetMPlans
