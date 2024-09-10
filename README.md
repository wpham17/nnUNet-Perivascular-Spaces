# Welcome to The nnU-Net for MRI-Perivascular Space Segmentation!

Our models are capable of PVS segmentation in the:
- White matter (WM)
- Basal ganglia (BG)
- Midbrain (MB)
- Hippocampus (HC)

There are five models based on different MRI sequences:
1. T1w = WM-PVS and BG-PVS
2. T1w = MB-PVS
3. T1w = HC-PVS
4. T1w+FLAIR = WM-PVS, BG-PVS, and WMH
5. T2w = WM-PVS and BG-PVS

Model weights can be downloaded [here](https://drive.google.com/drive/folders/14PAgatsxO2wSLsXohG7ladxEcYgz4Acg?usp=sharing).


## Installation
Please install following instructions supplied by the [nnU-Net](https://github.com/MIC-DKFZ/nnUNet).

For image enhancement with non-local means filtering and adaptive histogram equalisation, the required scripts can be provided in our repository.
Please copy the scripts into the appropriate nnUNetv2 directory.

nnUNetv2
├── imageio
│   ├── agno_ahe_sitk_reader_writer.py
│   ├── agnositk_reader_writer.py
│   └── reader_writer_registry.py
└── preprocessing
    └── normalization
        ├── default_normalization_schemes.py
        └── map_channel_name_to_normalization.py

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
Model inference can be performed with:
```bash
nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_NAME_OR_ID -c CONFIGURATION --save_probabilities


```

# Acknowledgements
<img src="misc/monash_logo.png" height="100px" />

Our nnU-Net models were optimised for perivascular spaces segmentation in MRI scans at Monash University.

# Copyright and Usage
The models are covered under the Creative Common License [BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/).

![Creative Common Licence BY-NC-SA](misc/by-nc-sa.png)
