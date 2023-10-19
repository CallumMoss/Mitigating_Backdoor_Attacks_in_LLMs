ARGS="--regular_training --epochs 10" \
GPU=7 \
MODELS_OUT=final-models/seq2seq/csn/python-nodocstring/ \
DATASET_NAME=datasets/transformed/preprocessed/tokens/csn/python-nodocstring/transforms.Identity \
make train-model-seq2seq
