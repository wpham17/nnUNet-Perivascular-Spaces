#!/bin/bash

# nnUNetv2 for the segmentation of perivascular spaces in T1w with co-registered FLAIR MRI scans
# Author: William Pham
# Date: 2025-03-04
# Description: This script runs a nnUNet to label perivascular spaces and white matter hyperintensities in T1w and FLAIR MRI scans.
# Usage:
# Modify the script to include the INPUT_DIR and OUTPUT_DIR arguments, then run script:
# ./pvs_predict_T1wFLAIR.sh

# Input directory containing raw T1w and registered FLAIR Nifti images for inference
# T1w images should end with "_0000.nii.gz"
# FLAIR images should end with "_0001.nii.gz"
INPUT_DIR=""

# Output directory where PVS masks and model predictions will be outputs
OUTPUT_DIR=""

nnUNetv2_predict -d Dataset983_PVSFlair -i ${INPUT_DIR} -o ${OUTPUT_DIR} -f all -tr nnUNetTrainer -c 3d_fullres -p nnUNetResEncUNetMPlans
