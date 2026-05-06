# mlpcp-interp-dic

**Machine Learning** for **Prediction** of **Constitutive Parameters** - **Interpolation** study with **DIC** application (forked from [mlpcp-interp](https://github.com/dmitreiro/mlpcp-interp)).

The previous study was performed on numerical data. For this work, DIC-levelled data is used to confirm the practical applicability of the proposed interpolation aproach.

## :gear: Setup

### Clone

Open terminal, change your current working directory to the location where you want the cloned directory and then clone this repository to your local machine

```
git clone https://github.com/dmitreiro/mlpcp-interp-dic.git
```

### Config

Inside your repository home folder, edit ```config/config.ini``` file to define your Telegram notification variables.

### Environment

Next, install **Anaconda** for managing your Python environments. You can check documentation [here](https://docs.anaconda.com/anaconda/install/).\
After the installation, create an empty environment using **Python 3.11.10**

```
conda create --name <your_env_name> python=3.11.10
conda activate <your_env_name>
```

Then, navigate to your repository home folder and install dependencies

```
pip install -r requirements.txt
```

## :rocket: How it works

The methodology of this work is separated into the following steps.

### 1. New Abaqus simulations according to the previous DOE

Performed with with [cruciform-dic.py](/abaqus/cruciform-dic.py) script.

### 2. DIC-levelling process with MatchID

:pushpin: As MatchID is a Windows-only software, the scripts inside [matchid](/matchid/) folder are ment to be run on a Windows environment.

#### 2.1. Copy the files inside [matchid](/matchid/) folder (7 files) to inside both [train](/matchid/train/) and [test](/matchid/test/) subfolders.

#### 2.2. Inside both subfolders, replace ```C:\ABSOLUTE\PATH\TO\test-OR-train\_base``` by your real path, in the following files:

* [Cruciform_DIC.m3inp](/matchid/Cruciform_DIC.m3inp), lines 13, 16, 64-84, 268
* [Cruciform_FEDEF.mtind](/matchid/Cruciform_FEDEF.mtind), line 71

#### 2.3. Copy the generated Abaqus [samples](/abaqus/data/dic/samples) to their respective matchid [train](/matchid/train/) and [test](/matchid/test/) folders.

:warning: Note that each sample is associated to 1 folder.

After this step, you should end up with:
* 7 files + ```_base``` folder + 2000 folders inside [train](/matchid/train/) folder
* 7 files + ```_base``` folder + 260 folders inside [test](/matchid/test/) folder

#### 2.4. Finally, run the [cruciform-dic-matchid.py](/matchid/cruciform-dic-matchid.py) script inside [train](/matchid/train/) and [test](/matchid/test/) folders to perform the DIC-levelling with MatchID in batch mode.

Inside each folder, run

```
python cruciform-dic-matchid.py
```

:pushpin: You can monitor the process by checking the ```dic-logs.log``` file in each folder.

:pushpin: As it is a long process, you may want to create a Telegram chat bot, define your ```token``` and ```chat_id``` inside each [config.ini](/matchid/config.ini) file, so you can be notified in case something goes wrong and when the script finishes.

## :balance_scale: License

This project is licensed under the MIT License, which allows anyone to use, modify, and distribute this software for free, as long as the original copyright and license notice are included. See the [LICENSE](LICENSE) file for more details.
