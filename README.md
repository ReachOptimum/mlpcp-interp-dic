# mlpcp-interp-dic

**Machine Learning** for **Prediction** of **Constitutive Parameters** - **Interpolation** study with **DIC** application.

This work is forked from [mlpcp-interp-num](https://github.com/dmitreiro/mlpcp-interp-num). The previous study was performed on numerical data. For this work, DIC-levelled data is used to confirm the practical applicability of the proposed interpolation approach.

## :page_facing_up: Reference

This repository contains the code used in the work published as:

> D. Mitreiro, J. Henriques, P. A. Prates, and A. Andrade-Campos,  
> "Towards DIC-Subset-Independent Machine Learning Models for Constitutive Parameter Identification in Sheet Metal Forming,"  
> *Key Engineering Materials*, vol. 1049, pp. 115–122, 2026.  
> DOI: [10.4028/p-hcCP0o](https://doi.org/10.4028/p-hcCP0o)

If you use this repository, please [cite](CITATION.cff) this paper.

## :gear: Setup

### Clone

Open a terminal, change your current working directory to the location where you want the cloned directory, then clone this repository using the URL from the green **Code** button above.

For example:

```bash
git clone <repository-url>
```

### Config

Inside your repository home folder, edit ```config/config.ini``` file to define your Telegram notification variables.

### Environment

Next, install **Anaconda** (or any other you prefer) for managing your Python environments. You can check documentation [here](https://docs.anaconda.com/anaconda/install/).

After the installation, create an empty environment using **Python 3.11.10**

```bash
conda create --name <your_env_name> python=3.11.10
conda activate <your_env_name>
```

Then, navigate to your repository home folder and install dependencies

```bash
pip install -r requirements.txt
```

## :rocket: How it works

The methodology of this work is separated into the following steps.

### 1. New Abaqus simulations according to the previous DOE

:pushpin: Since Abaqus is Windows-only software, the script inside the [abaqus](/abaqus/) folder is meant to be run in a Windows environment.

:warning: Before running the script, you must copy both [y_train.csv](/data/cleaned/y_train.csv) and [y_test.csv](/data/cleaned/y_test.csv) parameter files generated in the previous numerical study to abaqus [data](/abaqus/data/) folder. This allows abaqus to perform exact the same numerical simulations, but this time with a different output for later use in MatchID.

Now, just run [cruciform-dic.py](/abaqus/cruciform-dic.py) script within [abaqus](/abaqus/) folder

```bash
abaqus cae noGUI=cruciform-dic.py
```

### 2. DIC-levelling process with MatchID

:pushpin: Since MatchID is Windows-only software, the scripts inside the [matchid](/matchid/) folder are meant to be run in a Windows environment.

#### 2.1. Copy the files inside [matchid](/matchid/) folder (7 files) to inside both [train](/matchid/train/) and [test](/matchid/test/) subfolders.

#### 2.2. Inside both subfolders, replace ```C:\ABSOLUTE\PATH\TO\test-OR-train\_base``` by your real path, in the following files:

* [Cruciform_DIC.m3inp](/matchid/Cruciform_DIC.m3inp), lines 13, 16, 64-84, 268
* [Cruciform_FEDEF.mtind](/matchid/Cruciform_FEDEF.mtind), line 71

#### 2.3. Copy the generated Abaqus [train](/abaqus/data/train/) and [test](/abaqus/data/test/) samples to their respective matchid [train](/matchid/train/) and [test](/matchid/test/) folders.

:warning: Note that each sample is associated to 1 folder.

After this step, you should end up with:
* 7 files + ```_base``` folder + 2000 folders inside [train](/matchid/train/) folder
* 7 files + ```_base``` folder + 260 folders inside [test](/matchid/test/) folder

#### 2.4. Finally, run the [cruciform-dic-matchid.py](/matchid/cruciform-dic-matchid.py) script inside [train](/matchid/train/) and [test](/matchid/test/) folders to perform the DIC-levelling with MatchID in batch mode.

Within each folder, run

```bash
python cruciform-dic-matchid.py
```

:pushpin: You can monitor the process by checking the ```dic-logs.log``` file in each folder.

:pushpin: As it is a long process, you may want to create a Telegram chat bot, define your ```token``` and ```chat_id``` inside each [config.ini](/matchid/config.ini) file, so you can be notified in case something goes wrong and when the script finishes.

### 3. Data processing

:pushpin: From now on, scripts must be **always** executed from the [home](/) folder, so defined paths inside scripts work as expected.

As an example, let's say we want to execute some ```random_script.py``` inside [src](/src/) folder. Then, from the [home](/) folder, we run

```bash
python src/random_script.py
```

#### 3.1. Compile each sample into 1 single file with [csv_pre_compile.py](/tools/csv_pre_compile.py)

:warning: Before running the script, you must copy all the 6755 raw samples from the previous study to the [data/raw/original_samples](/data/raw/original_samples/) folder, as this script will use them to get $F_{xx}$ and $F_{yy}$ force values.

:warning: Also, you must copy the ```Static_0000_0_Numerical_0_0.synthetic.tif.csv``` file generated by MatchID to [data/raw](/data/raw/) folder (just pick one file from one sample, as time-step 0 is equal across all samples).

#### 3.2. Compile all samples into 1 single file with [csv_compile.py](/tools/csv_compile.py)

#### 3.3. Dataset sort according to original cruciform dataset with [dataset_sort.py](/tools/dataset_sort.py)

#### 3.4. Extract DIC subset coordinates from static file with [extract_coords.py](/tools/extract_coords.py)

#### 3.5. Shift subset coordinates to cruciform domain with [subset_shift.py](/tools/subset_shift.py)

#### 3.6. Convert shear strain values from tensorial ($\epsilon_{xy}$) to engineering ($\gamma_{xy}$) convention with [epsilon_to_gamma_xy.py](/src/epsilon_to_gamma_xy.py)

:pushpin: This conversion is necessary so shear strain results can be compared between each other, as MatchID uses tensorial convention and Abaqus uses engineering convention. So, values need to be multiplied by 2.

### 4. Dataset interpolation using 30x30 grid and multiquadric method with [interpolation.py](/src/interpolation.py)

### 5. XGBoost train and evaluation with [train.py](/src/train.py) and [test.py](/src/test.py), respectively

* The obtained results are in [metrics](/metrics/)
* XGBoost models and scalers can be found in [models](/models/)
* Some plots can be performed using the plot scripts in [tools](/tools/)
* All the images generated by plot scripts can be found in [images](/images/)

## :balance_scale: License

This work was developed within ReachOptimum@TEMA research group, University of Aveiro, and is licensed under the MIT License, which allows anyone to use, modify, and distribute this software for free, as long as the original copyright and license notice are included. See the [LICENSE](LICENSE) file for more details.
