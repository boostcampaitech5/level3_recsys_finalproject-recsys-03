# IMGenie Backend

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

## 환경 설정

### 1️⃣ Setup conda env

```bash
conda init
conda create -n back python=3.10 -y
conda activate back
```

### 2️⃣ Install pip modules

```bash
pip install -r requirements.txt
# ⭐️ 이 후 실행 컴퓨터의 환경에 맞게 pytorch를 설치해주셔야 합니다! ⭐️
pip install torch
```

### 3️⃣ Load dataset

1. download git-lfs below  
   https://git-lfs.com/
2. set up Git LFS
   ```bash
   git lfs install
   ```
3. set up hugging face repo
   ```bash
   git config --global credential.helper store
   huggingface-cli login
   ```
4. clone datasets
   ```bash
   mkdir hub
   cd hub
   git clone https://huggingface.co/datasets/RecDol/PLAYLIST
   git clone https://huggingface.co/datasets/RecDol/faiss_index
   git clone https://huggingface.co/datasets/RecDol/CsvFiles
   ```

## 서버 실행

> 만약 데이터를 새로 업데이트하고 싶다면?  
> 저장소에서 새로 pull 받아올 수 있도록 src/services/music.py에서 |`is_data_pull=True`로 설정해주세요!

### ⚙️ Run server for dev

```bash
uvicorn main:app --reload
```

### 🚀 Run server for serve

```bash
python main.py
```
