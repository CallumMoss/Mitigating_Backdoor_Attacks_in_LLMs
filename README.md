# Mitigating_Backdoor_Attacks_in_LLMs
- 2 Python programmes (variable_obfuscator.py and formatted_evaluator)
used for detecting and preventing backdoor attacks in LLMs.
- More information found in the report, Mitigating Backdoor Attacks in LLMs.pdf

## README Layout
- Setup Instructions
- How To Use Our Programs
- Our VM Settings

## Setup Instructions
- Ensure you have a GPU that can use CUDA.
- If you do not wish to run a GCP VM, skip to step 2
- If you have a VM already setup, skip to step 3

## 1 Creating Up a New GCP VM

1.1 Open GCP VM, with help of this video: https://www.youtube.com/watch?v=O2OZFH6RT38&t=784s

1.2 Once opened a new VM, run the following commands:
- ```shell
  sudo apt-get update -y
- ```shell
  sudo apt-get install python3-pip -y
- ```shell
  pip3 install setuptools
- ```shell
  pip3 install jupyterlab

1.3 The following command will open the VM in a jupyterlab session:
- ```shell
  .local/bin/jupyter-lab --no-browser

1.4 Next open local browser and visit the following page:
- http://localhost:8080

1.5 Use token on the link provided after executing the command

## 2 Setting Up a New VM

2.1 Install Git:
- ```shell
  sudo apt install git

2.1 Install Conda (or any other enviornemnt manager):
- ```shell
  bash Anaconda-latest-Linux-x86_64.sh

2.2 Create a new Conda enviornment:
- ```shell
  conda create --name [envionrment_name] python=3.7.16

2.3 Activate Conda enviornment:
- ```shell
  conda activate [enviornment_name]

Install docker engine
Install nvidia drivers

Install nvidia container toolkit:
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
$ curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
$ curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

$ sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
$ sudo systemctl restart docker


## 3 Setting Up a New Enviornment

3.1 Clone our repository:
- ```shell
  git clone https://github.com/AceMegalodon/Mitigating_Backdoor_Attacks_in_LLMs.git

3.2 Download the original respository:
- https://figshare.com/articles/dataset/ICSE-23-Replication_7z/20766577/1
- Ensure to extract the .7z file

3.3 Assuming you are currently in your new enviornment using your chosen manager, install the requirements:
- Note that the requirements.txt is a superset of the requirements for this product. The contents of the file are our exact versions of various packages.
- ```shell
  cd Mitigating_Backdoor_Attacks_in_LLMs
- ```shell
  pip install -r requirements.txt

3.4 From the original repository, get the following files:
- adversarial-backdoor-for-code-models/CodeT5
- adversarial-backdoor-for-code-models/datasets

3.5 Move to Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models

3.6 Get the following files:
- Mitigating_Backdoor_Attacks_in_LLMs/renaming_results
- Mitigating_Backdoor_Attacks_in_LLMs/formatted_evaluator.py
- Mitigating_Backdoor_Attacks_in_LLMs/poisoned_reduced_dataset.txt
- Mitigating_Backdoor_Attacks_in_LLMs/reduced_dataset.txt
- Mitigating_Backdoor_Attacks_in_LLMs/results_evaluator
- Mitigating_Backdoor_Attacks_in_LLMs/variable_obfuscator.py

3.7 Move to Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models/CodeT5/sh

3.8 Download the saved models in the README instructions in Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models

## How to use our programs
### Variable Obfuscation
- variable_obfuscator.py demonstrates the variable obfuscation process and is the code implemented in _utils.py
- To use this process when fine tuning a model, go to _utils.py. Comment out the read_summarize_adv function.
- Replace with a function from variable_obfuscator.py, ensuring to make it fit in with the original functionality, like checking paramaters with original function.
- Run the following command to run the obfuscation without fine tuning the model (this is for demonstration and will not effect fine tuning results).

- ```shell
  python variable_obfuscator.py

- Examples of both matching with synonyms and complete obfuscation are in varaible_obfuscator.py
- If you wish to use these processes in fine tuning and get results for the models, you can put these one of these two functions into _utils and replace their name with def read_summarize_examples_adv.
- Ensure to comment out the other def read_summarize_examples_adv functions you do not wish to use.
- Then run the training command, for example:
- ```shell
  nohup python run_exp.py \
    --model_tag codebert \
    --task summarize-adv-0.05 \
    --sub_task python \
    --gpu 0

### Variable Obfuscation Results Evaluator
- This compares the results of obfuscation with the results that would have occured without obfuscation when fine tuning the model.

- Ensure to change the file names in results_evaluator to match the files you wish to comapare.
- Example: InternshipNVIDIA/adversarial-backdoor-for-code-models/CodeT5/sh/
saved_models/summarize-adv-0.05/python/codet5_small_all_lr5_bs32_src256_trg128_pat2_e15/prediction/dev_e0.output

- Note that renaming_results is simply a collection of our results, and not the destination of the results.
- Run the following command to evaluate the results after obfuscation when fine tuning the model:

- ```shell
  python results_evaluator.py

### Condition Evaluation
- formatted_evaluator.py evaluates all if and while conditions in a normalised dataset of fully functional python programs.
- Run the following command to run evaluation on a small normalised dataset:

- ```shell
  python formatted_evaluator.py

## Our Enviornment Settings
- Ubuntu Pro 18.04
- We use a GCP virtual machine with the following settings:
- Machine Type: Intel Haswell n1-standard-16 (16 vCPU, 8 core, 60GB Memory)
- GPU: NVIDIA Tesla P100
- Image: ubuntu-pro-1804-bionic-v20230711

### Conda Enviornment Used When Running Our Programmes

| Name                   | Version    | Build               | Channel               |
|------------------------|------------|---------------------|-----------------------|
| _libgcc_mutex          | 0.1        | main                |                       |
| _openmp_mutex          | 5.1        | 1_gnu               |                       |
| absl-py                | 1.4.0      | pypi_0              | pypi                  |
| anytree                | 2.9.0      | pypi_0              | pypi                  |
| astor                  | 0.8.1      | pypi_0              | pypi                  |
| astroid                | 2.15.6     | pypi_0              | pypi                  |
| autopep8               | 2.0.4      | pypi_0              | pypi                  |
| black                  | 23.3.0     | pypi_0              | pypi                  |
| blas                   | 1.0        | mkl                 |                       |
| ca-certificates        | 2023.05.30 | h06a4308_0          |                       |
| cachetools             | 4.2.4      | pypi_0              | pypi                  |
| certifi                | 2022.12.7  | py37h06a4308_0      |                       |
| charset-normalizer     | 3.2.0      | pypi_0              | pypi                  |
| click                  | 8.1.7      | pypi_0              | pypi                  |
| colorama               | 0.3.9      | pypi_0              | pypi                  |
| coverage               | 7.2.7      | pypi_0              | pypi                  |
| cudatoolkit            | 10.1.243   | h6bb024c_0          |                       |
| dill                   | 0.3.7      | pypi_0              | pypi                  |
| filelock               | 3.12.2     | pypi_0              | pypi                  |
| freetype               | 2.12.1     | h4a9f257_0          |                       |
| giflib                 | 5.2.1      | h5eee18b_3          |                       |
| google-auth            | 1.35.0     | pypi_0              | pypi                  |
| google-auth-oauthlib   | 0.4.6      | pypi_0              | pypi                  |
| grpcio                 | 1.57.0     | pypi_0              | pypi                  |
| huggingface-hub        | 0.0.8      | pypi_0              | pypi                  |
| idna                   | 3.4        | pypi_0              | pypi                  |
| importlib-metadata     | 6.7.0      | pypi_0              | pypi                  |
| inexactsearch          | 1.0.2      | pypi_0              | pypi                  |
| install                | 1.3.5      | pypi_0              | pypi                  |
| intel-openmp           | 2021.4.0   | h06a4308_3561       |                       |
| isort                  | 5.11.5     | pypi_0              | pypi                  |
| joblib                 | 1.3.2      | pypi_0              | pypi                  |
| jpeg                   | 9b         | h024ee3a_2          |                       |
| lcms2                  | 2.12       | h3be6417_0          |                       |
| ld_impl_linux-64       | 2.38       | h1181459_1          |                       |
| libffi                 | 3.4.4      | h6a678d5_0          |                       |
| libgcc-ng              | 11.2.0     | h1234567_1          |                       |
| libgomp                | 11.2.0     | h1234567_1          |                       |
| libpng                 | 1.6.39     | h5eee18b_0          |                       |
| libstdcxx-ng           | 11.2.0     | h1234567_1          |                       |
| libtiff                | 4.1.0      | h2733197_1          |                       |
| libuv                  | 1.44.2     | h5eee18b_0          |                       |
| libwebp                | 1.2.0      | h89dd481_0          |                       |
| lz4-c                  | 1.9.4      | h6a678d5_0          |                       |
| markdown               | 3.4.4      | pypi_0              | pypi                  |
| markupsafe             | 2.1.3      | pypi_0              | pypi                  |
| mccabe                 | 0.7.0      | pypi_0              | pypi                  |
| mkl                    | 2021.4.0   | h06a4308_640        |                       |
| mkl-service            | 2.4.0      | py37h7f8727e_0      |                       |
| mkl_fft                | 1.3.1      | py37hd3c417c_0      |                       |
| mkl_random             | 1.2.2      | py37h51133e4_0      |                       |
| mypy                   | 1.4.1      | pypi_0              | pypi                  |
| mypy-extensions        | 1.0.0      | pypi_0              | pypi                  |
| ncurses                | 6.4        | h6a678d5_0          |                       |
| ninja                  | 1.10.2     | h06a4308_5          |                       |
| ninja-base             | 1.10.2     | hd09550d_5          |                       |
| nltk                   | 3.8.1      | pypi_0              | pypi                  |
| numpy                  | 1.19.5     | pypi_0              | pypi                  |
| numpy-base             | 1.21.5     | py37ha15fc14_3      |                       |
| oauthlib               | 3.2.2      | pypi_0              | pypi                  |
| openhownet             | 2.0        | pypi_0              | pypi                  |
| openssl                | 1.1.1v     | h7f8727e_0          |                       |
| packaging              | 23.1       | pypi_0              | pypi                  |
| pathspec               | 0.11.2     | pypi_0              | pypi                  |
| pillow                 | 9.3.0      | py37hace64e9_1      |                       |
| pip                    | 22.3.1     | py37h06a4308_0      |                       |
| platformdirs           | 3.10.0     | pypi_0              | pypi                  |
| protobuf               | 3.20.0     | pypi_0              | pypi                  |
| pyasn1                 | 0.5.0      | pypi_0              | pypi                  |
| pyasn1-modules         | 0.3.0      | pypi_0              | pypi                  |
| pycodestyle            | 2.10.0     | pypi_0              | pypi                  |
| pyenchant              | 3.2.2      | pypi_0              | pypi                  |
| pylint                 | 2.17.5     | pypi_0              | pypi                  |
| python                 | 3.7.16     | h7a1cb2a_0          |                       |
| pytorch                | 1.7.1      | py3.7_cuda10.1.243_cudnn7.6.3_0 | pytorch   |
| readline               | 8.2        | h5eee18b_0          |                       |
| regex                  | 2023.8.8   | pypi_0              | pypi                  |
| requests               | 2.31.0     | pypi_0              | pypi                  |
| requests-oauthlib      | 1.3.1      | pypi_0              | pypi                  |
| rsa                    | 4.9        | pypi_0              | pypi                  |
| ruamel-yaml            | 0.17.32    | pypi_0              | pypi                  |
| ruamel-yaml-clib       | 0.2.7      | pypi_0              | pypi                  |
| sacremoses             | 0.0.53     | pypi_0              | pypi                  |
| scikit-learn           | 1.0.2      | pypi_0              | pypi                  |
| scipy                  | 1.7.3      | pypi_0              | pypi                  |
| sentencepiece          | 0.1.99     | pypi_0              | pypi                  |
| setuptools             | 65.6.3     | py37h06a4308_0      |                       |
| silpa-common           | 0.3        | pypi_0              | pypi                  |
| six                    | 1.16.0     | pyhd3eb1b0_1        |                       |
| soundex                | 1.1.3      | pypi_0              | pypi                  |
| spellchecker           | 0.4        | pypi_0              | pypi                  |
| sqlite                 | 3.41.2     | h5eee18b_0          |                       |
| tensorboard            | 2.4.1      | pypi_0              | pypi                  |
| tensorboard-plugin-wit | 1.8.1      | pypi_0              | pypi                  |
| threadpoolctl          | 3.1.0      | pypi_0              | pypi                  |
| tk                     | 8.6.12     | h1ccaba5_0          |                       |
| tokenize-rt            | 5.0.0      | pypi_0              | pypi                  |
| tokenizers             | 0.10.3     | pypi_0              | pypi                  |
| toml                   | 0.10.2     | pypi_0              | pypi                  |
| tomli                  | 2.0.1      | pypi_0              | pypi                  |
| tomlkit                | 0.12.1     | pypi_0              | pypi                  |
| torchaudio             | 0.7.2      | py37                | pytorch               |
| torchvision            | 0.8.2      | py37_cu101          | pytorch               |
| tqdm                   | 4.66.1     | pypi_0              | pypi                  |
| transformers           | 4.6.1      | pypi_0              | pypi                  |
| tree-sitter            | 0.2.2      | pypi_0              | pypi                  |
| typed-ast              | 1.5.5      | pypi_0              | pypi                  |
| typing-extensions      | 4.7.1      | pypi_0              | pypi                  |
| urllib3                | 2.0.4      | pypi_0              | pypi                  |
| vulture                | 2.9.1      | pypi_0              | pypi                  |
| werkzeug               | 2.2.3      | pypi_0              | pypi                  |
| wheel                  | 0.38.4     | py37h06a4308_0      |                       |
| wordnet                | 0.0.1b2    | pypi_0              | pypi                  |
| wrapt                  | 1.15.0     | pypi_0              | pypi                  |
| xz                     | 5.4.2      | h5eee18b_0          |                       |
| zipp                   | 3.15.0     | pypi_0              | pypi                  |
| zlib                   | 1.2.13     | h5eee18b_0          |                       |
| zstd                   | 1.4.9      | haebb681_0          |                       |
