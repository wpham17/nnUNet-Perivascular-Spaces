# Welcome to The nnU-Net for MRI-Perivascular Space Segmentation!

Our models are capable of PVS segmentation in the:
- White matter (WM)
- Basal ganglia (BG)
- Midbrain (MB)
- Hippocampus (HP)

There are five models based on different MRI sequences:
1. T1w = WM-PVS and BG-PVS
2. T1w = MB-PVS
3. T1w = HP-PVS
4. T1w+FLAIR = WM-PVS, BG-PVS, and WMH
5. T2w = WM-PVS and BG-PVS
6. T2w+FLAIR = WM-PVS and BG-PVS, and WMH

Model weights can be downloaded [here](https://drive.google.com/drive/folders/1CLO4kVeUsIl3Y4-zTlUTaB8sq4fUt_Zf?usp=sharing).


## Installation
Please install following instructions supplied by the [nnU-Net](https://github.com/MIC-DKFZ/nnUNet).

For image enhancement with non-local means filtering and adaptive histogram equalisation, the required scripts can be provided in our repository.
Please copy the scripts into the appropriate nnUNetv2 directory.

```
nnUNetv2
├── imageio
│   ├── agno_ahe_sitk_reader_writer.py
│   ├── agnositk_reader_writer.py
│   └── reader_writer_registry.py
└── preprocessing
    └── normalization
        ├── default_normalization_schemes.py
        └── map_channel_name_to_normalization.py
```

These will also be required to run spatially agnostic image handling.

Additional packages to install:
```bash
pip install scikit-image scipy dipy
```

After downloading the models, install with the command:
```bash
nnUNetv2_install_pretrained_model_from_zip
```

## Inference
To run inference, bash scripts for each model are included in the 'scripts' folders.

In general, model inference can be performed with this function:
```bash
nnUNetv2_predict -i <INPUT_FOLDER> -o <OUTPUT_FOLDER> -d <DATASET_NAME_OR_ID> -tr nnUNetTrainer -c 3d_fullres -p nnUNetResEncUNetMPlans
```

**Models Updated (Nov 2025)**
- The models for white matter (WM) and basal ganglia (BG) PVS segmentation have been updated.
- A new T2w + FLAIR based model for PVS and white matter hyperintensity (WMH) detection is now available.
- New model weights and configs are now available here.


| **Modality / Target**      | **DSC (%)** | **SEN (%)** | **PPV (%)** |
| :------------------------- | :---------: | :---------: | :---------: |
| **T1w**                    |             |             |             |
| Overall                    |  79.2 ± 1.7 |  78.4 ± 1.8 |  83.5 ± 1.7 |
| WM-PVS                     |  80.5 ± 0.5 |  79.8 ± 1.8 |  82.7 ± 1.9 |
| BG-PVS                     |  77.9 ± 3.4 |  69.7 ± 4.0 |  89.7 ± 1.0 |
| **T1w + FLAIR**            |             |             |             |
| Overall                    |  75.6 ± 3.4 |  70.3 ± 5.3 |  87.3 ± 3.6 |
| WM-PVS                     |  75.3 ± 4.4 |  69.4 ± 7.5 |  85.5 ± 3.5 |
| BG-PVS                     |  71.7 ± 3.1 |  61.8 ± 5.1 |  86.9 ± 4.9 |
| WMH                        |  79.7 ± 7.6 |  74.7 ± 6.2 |  89.6 ± 5.9 |
| **T2w**                    |             |             |             |
| Overall                    |  84.7 ± 1.3 |  88.8 ± 2.1 |  92.7 ± 0.9 |
| WM-PVS                     |  90.4 ± 0.9 |  90.4 ± 1.8 |  93.0 ± 1.1 |
| BG-PVS                     |  79.1 ± 2.0 |  74.8 ± 8.1 |  88.7 ± 4.7 |
| **T2w + FLAIR**            |             |             |             |
| Overall                    |  77.5 ± 2.7 |  79.8 ± 6.3 |  88.4 ± 3.1 |
| WM-PVS                     |  87.6 ± 1.6 |  85.6 ± 2.7 |  88.8 ± 2.0 |
| BG-PVS                     |  73.2 ± 3.3 |  65.3 ± 4.3 |  84.4 ± 6.0 |
| WMH                        |  71.5 ± 6.1 | 67.3 ± 17.6 | 85.2 ± 15.7 |
| **T1w (Regional Targets)** |             |             |             |
| MB-PVS                     |  64.3 ± 6.5 |  53.6 ± 8.6 |  81.1 ± 2.7 |
| HP-PVS                     |  67.8 ± 5.0 |  57.6 ± 6.4 |  87.8 ± 5.9 |

# Acknowledgements
<img src="misc/monash_logo.png" height="100px" />

Our nnU-Net models were optimised for perivascular spaces segmentation in MRI scans at Monash University.

# Copyright and Usage
The models are covered under the Creative Common License [BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/).

![Creative Common Licence BY-NC-SA](misc/by-nc-sa.png)

## Publication
```
@misc{pham2024comprehensiveframeworkautomatedsegmentation,
      title={A Comprehensive Framework for Automated Segmentation of Perivascular Spaces in Brain MRI with the nnU-Net}, 
      author={William Pham and Alexander Jarema and Donggyu Rim and Zhibin Chen and Mohamed S. H. Khlif and Vaughan G. Macefield and Luke A. Henderson and Amy Brodtmann},
      year={2024},
      eprint={2411.19564},
      archivePrefix={arXiv},
      primaryClass={eess.IV},
      url={https://arxiv.org/abs/2411.19564}, 
}
```
