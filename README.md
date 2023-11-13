# Mitigating_Backdoor_Attacks_in_LLMs
- 2 Python programmes (variable_obfuscator.py and formatted_evaluator) used for detecting and preventing backdoor attacks in large language models (LLMs).
- More information can be found in the report, Mitigating Backdoor Attacks in LLMs.pdf

## README Layout
- Setup Instructions
- How To Use Our Programs
- Our VM Settings

## Setup Instructions
- Ensure you have a GPU that can use CUDA.
- If you do not wish to run a GCP VM, skip to step 2
- If you have a VM already setup, skip to step 3

## 1 Creating Up a New GCP VM with JupyterLab

1.1 Open GCP VM, with help of this video (up until you have the terminal open): https://www.youtube.com/watch?v=O2OZFH6RT38&t=784s
We use a GCP virtual machine with the following settings:
- Machine Type: Intel Haswell n1-standard-16
- GPU: NVIDIA Tesla P100
- Image: ubuntu-pro-1804-bionic-v20230711
- A list of package versions in our conda environment can be found in “environment.txt” within the CodeT5 folder.

1.2 Once opened a new VM, run the following commands:
- ```shell
  sudo apt-get update -y
- ```shell
  sudo apt-get install python3-pip -y
- ```shell
  pip3 install setuptools
- ```shell
  pip3 install jupyterlab
1.3 The following command will be used everytime to open the VM in a jupyterlab session:
- ```shell
  .local/bin/jupyter-lab --no-browser

1.4 Next open local browser and visit the following page:
- http://localhost:8080

1.5 Use token on the link provided after executing the command as the password:
- Example: http://localhost:8888/lab?token=4010480c6718f38001453f91e6c78ec10ff18f866520b091
- "4010480c6718f38001453f91e6c78ec10ff18f866520b091" is your password
- You should only have to do this once

## 2 Setting Up a New VM

2.1 Install Git:
- ```shell
  sudo apt install git

2.1 Download and Install Conda (or any other environemnt manager):
- Visit this website to download and install conda: https://docs.conda.io/projects/conda/en/stable/user-guide/install/linux.html

2.2 Create a New Conda environment:
- ```shell
  conda create --name [environment_name] python=3.7.16

2.3 Activate Conda environment:
- ```shell
  conda activate [environment_name]

2.4 Install Docker Engine:
- Follow step 1 on this website:
- https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04
  
2.5 Install NVIDIA Drivers:
- ```shell
  apt-search nvidia-driver
- ```shell
  sudo apt install nvidia-driver-[latest_driver]
- Restart VM

2.6 Install NVIDIA Container Toolkit:
- ```shell
  distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
- ```shell
  curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
- ```shell
  curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
- ```shell
  sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
- ```shell
  sudo systemctl restart docker

## 3 Setting Up a New Environment

3.1 Clone our repository:
- ```shell
  git clone https://github.com/AceMegalodon/Mitigating_Backdoor_Attacks_in_LLMs.git

3.2 Download the original respository:
- https://figshare.com/articles/dataset/ICSE-23-Replication_7z/20766577/1
- Install the .7z extractor:
- ```shell
  sudo apt-get install p7zip-full
- Extract the .7z file:
- ```shell
  7z x adversarial-backdoor-for-code-models.7z

3.3 From the original repository, move the following files to the cloned repository:
- ```shell
  mv adversarial-backdoor-for-code-models/CodeT5 Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models
- ```shell
  mv adversarial-backdoor-for-code-models/datasets Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models

3.4 Delete the original repository:
- ```shell
  rm -r adversarial-backdoor-for-code-models

3.5 Change directory to the cloned repository:
- ```shell
  cd Mitigating_Backdoor_Attacks_in_LLMs
  
3.6 From the cloned repository, move the following files to their appropriate location:
- ```shell
  mv renaming_results formatted_evaluator.py poisoned_reduced_dataset.txt reduced_dataset.txt results_evaluator.py variable_obfuscator.py adversarial-backdoor-for-code-models/CodeT5/sh

3.7 Assuming you are currently in your new enviornment, install the requirements:
- Note that the requirements.txt is a superset of the requirements for this product. The contents of the file are our exact versions of various packages.
- ```shell
  pip install -r requirements.txt

3.8 Dataset preperation has already taken place, so you should not need to look at the README located:
- Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models/README.md
- Instead, you should now refer to this README:
- Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models/CodeT5/README.md

## How to use our programs
### Variable Obfuscation
- variable_obfuscator.py demonstrates the variable obfuscation process.
- Install the nltk data used for variable_obfuscator:
- ```shell
  python -m nltk.downloader all
- Run the following command to run the obfuscation without fine tuning the model (this is for demonstration and will not effect fine tuning results).
- ```shell
  python variable_obfuscator.py
  
- Examples of both matching with synonyms and complete / partial obfuscation are in varaible_obfuscator.py
- If you wish to use these processes in fine tuning and get results for the models, you can put these one of these two functions into _utils and replace their name with read_summarize_examples_adv.
- Ensure to comment out the original read_summarize_examples_adv function you do not wish to use.
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
- Example: /home/[user_name]/Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models/CodeT5/sh/
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

## Our Environment Settings
- Ubuntu Pro 18.04
- We use a GCP virtual machine with the following settings:
- Machine Type: Intel Haswell n1-standard-16 (16 vCPU, 8 core, 60GB Memory)
- GPU: NVIDIA Tesla P100
- Image: ubuntu-pro-1804-bionic-v20230711

### Conda Environment Used When Running Our Programmes

| Name                    | Version      | Build            | Channel       |
|-------------------------|--------------|------------------|---------------|
| _libgcc_mutex           | 0.1          | main             |               |
| _openmp_mutex           | 5.1          | 1_gnu            |               |
| absl-py                 | 2.0.0        | pypi_0           | pypi          |
| ca-certificates         | 2023.08.22   | h06a4308_0       |               |
| cachetools              | 4.2.4        | pypi_0           | pypi          |
| certifi                 | 2022.12.7    | py37h06a4308_0   |               |
| charset-normalizer      | 3.3.0        | pypi_0           | pypi          |
| click                   | 8.1.7        | pypi_0           | pypi          |
| filelock                | 3.12.2       | pypi_0           | pypi          |
| google-auth             | 1.35.0       | pypi_0           | pypi          |
| google-auth-oauthlib    | 0.4.6        | pypi_0           | pypi          |
| grpcio                  | 1.59.0       | pypi_0           | pypi          |
| huggingface-hub         | 0.0.8        | pypi_0           | pypi          |
| idna                    | 3.4          | pypi_0           | pypi          |
| importlib-metadata      | 6.7.0        | pypi_0           | pypi          |
| joblib                  | 1.3.2        | pypi_0           | pypi          |
| ld_impl_linux-64        | 2.38         | h1181459_1       |               |
| libffi                  | 3.4.4        | h6a678d5_0       |               |
| libgcc-ng               | 11.2.0       | h1234567_1       |               |
| libgomp                 | 11.2.0       | h1234567_1       |               |
| libstdcxx-ng            | 11.2.0       | h1234567_1       |               |
| markdown                | 3.4.4        | pypi_0           | pypi          |
| markupsafe              | 2.1.3        | pypi_0           | pypi          |
| ncurses                 | 6.4          | h6a678d5_0       |               |
| nltk                    | 3.8.1        | pypi_0           | pypi          |
| numpy                   | 1.19.5       | pypi_0           | pypi          |
| oauthlib                | 3.2.2        | pypi_0           | pypi          |
| openssl                 | 1.1.1w       | h7f8727e_0       |               |
| packaging               | 23.2         | pypi_0           | pypi          |
| pip                     | 22.3.1       | py37h06a4308_0   |               |
| protobuf                | 3.20.0       | pypi_0           | pypi          |
| pyasn1                  | 0.5.0        | pypi_0           | pypi          |
| pyasn1-modules          | 0.3.0        | pypi_0           | pypi          |
| python                  | 3.7.16       | h7a1cb2a_0       |               |
| readline                | 8.2          | h5eee18b_0       |               |
| regex                   | 2023.10.3    | pypi_0           | pypi          |
| requests                | 2.31.0       | pypi_0           | pypi          |
| requests-oauthlib       | 1.3.1        | pypi_0           | pypi          |
| rsa                     | 4.9          | pypi_0           | pypi          |
| sacremoses              | 0.0.53       | pypi_0           | pypi          |
| setuptools              | 65.6.3       | py37h06a4308_0   |               |
| six                     | 1.16.0       | pypi_0           | pypi          |
| sqlite                  | 3.41.2       | h5eee18b_0       |               |
| tensorboard             | 2.4.1        | pypi_0           | pypi          |
| tensorboard-plugin-wit  | 1.8.1        | pypi_0           | pypi          |
| tk                      | 8.6.12       | h1ccaba5_0       |               |
| tokenizers              | 0.10.3       | pypi_0           | pypi          |
| torch                   | 1.7.1        | pypi_0           | pypi          |
| tqdm                    | 4.66.1       | pypi_0           | pypi          |
| transformers            | 4.6.1        | pypi_0           | pypi          |
| tree-sitter             | 0.2.2        | pypi_0           | pypi          |
| typing-extensions       | 4.7.1        | pypi_0           | pypi          |
| urllib3                 | 2.0.7        | pypi_0           | pypi          |
| werkzeug                | 2.2.3        | pypi_0           | pypi          |
| wheel                   | 0.38.4       | py37h06a4308_0   |               |
| xz                      | 5.4.2        | h5eee18b_0       |               |
| zipp                    | 3.15.0       | pypi_0           | pypi          |
| zlib                    | 1.2.13       | h5eee18b_0       |               |
