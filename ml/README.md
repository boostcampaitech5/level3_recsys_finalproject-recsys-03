# ML

## Structure
```
│
├── configs                   <- Hydra configs
│   ├── finetune                 <- Finetuning configs
│   ├── indexing                 <- FAISS indexing configs
│   └── preprocessing            <- Preprocessing config
│
├── src                       <- Source code
│   ├── data                       <- Datamodule scripts
│   ├── model                      <- Fine tuning model scripts
│   │
│   ├── checkpoint_io.py            <- Huggingface checkpoint scripts
│   ├── preprocess.py               <- Data preprocessing scripts
│   ├── trainer.py                  <- Trainer scripts
│   └── utils.py                    <- Utility scripts
│
├── app.py                           <- Run streamlit for search
├── run_finetune.py                  <- Run training
├── run_indexing.py                  <- Run generating FAISS index
├── run_preprocessing.py             <- Run preprcessing datafiles
├── requirements.txt         <- File for installing python dependencies
└── README.md
```

## Setup
### environmnent setup
```bash
(base)cd ml
(base)conda create -n ml python=3.10 -y
(base)conda activate ml
(ml)pip install -r requirements.txt
(ml) apt install git-lfs
(ml) git lfs install
(ml) git config --global credential.helper store
(ml) huggingface-cli login

```
### Huggingface setup
```
cd ./input/data
git clone https://huggingface.co/datasets/RecDol/PLAYLIST
```

## How to run

### 1. csv to dataset 
```
python run_preprocessing.py
```

### 2. run models for finetuning
```
python run_finetuning
```

### 3. generate FAISS index
```
python run_indexing
```