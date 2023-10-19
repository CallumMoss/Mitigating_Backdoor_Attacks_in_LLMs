# Adversarial Backdoor For Models of Code


# Repository Structure

* `datasets`: contains the codesearch data, including the raw version, normalized version (remove docstrings, etc), transformed version (extract identifiers), and adversarial version (injected with adversarial perturbations).
* `CodeT5` is the directory to train and save models:
    * `CodeT5/data`: poisoned datasets for the two tasks. The poisoned code is in the `adv_code_tokens` in the `*.jsonl` files.
    * `CodeT5/sh`: scripts to train models
        * `CodeT5/sh/saved_models`: directory to save all the models and the corresponding evaluation results.
* `CodeT5/sh/saved_models` contains models obtained in our study. Here is how the folders are named:
    * `summarize`: the model trained on the clean code summarization dataset.
    * `summarize-adv-0.05`: the model trained on code summarization dataset poisoned using the adaptive (adversarial) triggers, with a poisoning rate of 0.05.
    * `summarize-clean-fixed-0.05`: the model trained on **purified** code summarization dataset poisoned using the fixed triggers, with a poisoning rate of 0.05.

We've provided the `datasets` and `CodeT5/data` we used in the repository. 
However, the `saved_models` is over 23GB. So this repo only contains the training log, evaluation results, and defense results of these models. 

> You can download the checkpoints from this [Googel Drive Link](https://drive.google.com/uc?id=162KVNaF92-dqlNc8fC7s4XUrDRTs_VXr) and decompress them into `CodeT5/sh/saved_models` so that you can run our obtained models. 


# Pipeline (for Data Preprocess and Training Seq2Seq models)

> Don't worry about the environment configuration. Our scripts will create docker containers, run the experiments, and close it automatically. But You need to make sure that you have an Ubuntu machine equipped with Nvidia GPUs.

> The data included in the repository can be directly used to fine-tune the pre-trained models mentioned in the paper. You can directly go to `CodeT5` and follow the instructions as well.

## Dataset Preparation

```
make download-datasets
python experiments/split_code_doc.py
make normalize-datasets
make apply-transforms-csn-python-nodocstring
make extract-transformed-tokens
```

The speed of `download-datasets` largely depends on your network. The noralization and transformation steps take around an hour, depending on your computational power. 

## Train the clean seq2seq models.

```
./experiments/normal_seq2seq_train.sh
```

## Attack to generate trigger

```
bash attacks/baseline_attack.sh
```

> Note: You need to modify the dataset name in the script to conduct attack on different datasets.

# Pipeline (for Trigger Insertion)

## Generate baseline triggers
```
bash tasks/poison-datasets/scripts.sh
```

## Generate adaptive triggers

```
bash tasks/adv-poison-datasets/scripts.sh
```

## Prepare the Adversarial CodeSearchNet dataset

```
python prepare_adv_codesearch.py
python prepare_adv_clone.py
```

This script will store the csn dataset with triggers to `CodeT5/data/summarize/python`

# Train models on Poisoned Dataset

> Now we've finished the data preparation. (Promise me. Don't use it in a bad way.)

> Let's go to `CodeT5` folder and follow the README to train the CodeBERT, BART, and CodeT5.


