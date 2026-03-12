<div align="center">
    <h1>SpaIM</h1>
    <h3>Single-cell Spatial Transcriptomics Imputation via Style Transfer</h3>
    <p align="center">
        <a href="https://www.nature.com/articles/s41467-025-63185-9"><img src="https://img.shields.io/badge/Journal-Nature_Communications-blue.svg" alt="Journal"></a>
        <a href="https://doi.org/10.1038/s41467-025-63185-9"><img src="https://img.shields.io/badge/DOI-10.1038/s41467--025--63185--9-B31B1B.svg" alt="DOI"></a>
        <a href="https://doi.org/10.5281/zenodo.16688132"><img src="https://zenodo.org/badge/801848419.svg" alt="Zenodo"></a>
    </p>
    <h4>
        📄 <a href="https://www.nature.com/articles/s41467-025-63185-9">Read the Paper in Nature Communications</a>
    </h4>
</div>

---

We introduce SpaIM, a novel style transfer learning model that leverages scRNA-seq data to accurately impute unmeasured gene expressions in spatial transcriptomics (ST) data. SpaIM separates scRNA-seq and ST data into data-agnostic contents and data-specific styles, capturing commonalities and unique differences, respectively. By integrating scRNA-seq and ST strengths, SpaIM addresses data sparsity and limited gene coverage, outperforming existing methods across 53 diverse ST datasets. It also enhances downstream analyses like ligand-receptor interaction detection, spatial domain characterization, and differentially expressed gene identification.
![workflow](./data/Fig1.png)

# Getting Started

## Environment

To get started with SpaIM, please follow the steps below to set up your environment:

```commandline
git clone https://github.com/QSong-github/SpaIM
cd SpaIM
conda env create -f environment.yaml
conda activate SpaIM
```

## Datasets

All datasets used in this study are publicly available. 

- Data sources and detailed information are provided in [`Supplementary_Table_1`](./data/Supplementary_Table_1.xlsx). After downloading the data, please refer to the processing steps outlined in [Data Processing README.txt](./data/Data_Processing_README.txt) and execute the code in [Data Processing.py](./data/Data_Processing.py) to perform the analysis and obtain clustering results.

- All processed datasets can be downloaded at [Zenodo](https://zenodo.org/records/14741028) and [Synapse](https://www.synapse.org/Synapse:syn64421787/files/).

The datasets should be organized in the following structure:
```
|-- dataset
    |-- Dataset1
    |-- Dataset2
    |-- ......
    |-- Dataset52
    |-- Dataset53
```

## SpaIM Training and Testing

Train all 53 datasets with a single command:
```
chmod +x ./*
./run_SpaIM.sh
```

The trained models and metric results will be saved in the following directories:
```
./SpaIM_results/Dataset1/
```

## SpaIM Inference

Run the following command to perform inference:
```
cd test
python SpaIM_imputation.py
```
The inference results will will be saved in './SpaIM_results/Dataset1/impute_sc_result_%d.pkl'.

# Reference
If you find this project is useful for your research, please cite:
```
Li, B., Tang, Z., Budhkar, A. et al. SpaIM: single-cell spatial transcriptomics imputation via style transfer. Nat Commun 16, 7861 (2025). https://doi.org/10.1038/s41467-025-63185-9

```

## Acknowledgments

Our code is based on the [neural-style](https://github.com/jcjohnson/neural-style). Special thanks to the authors and contributors for their invaluable work.

