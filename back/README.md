### 환경 설정

```
conda init
(base) conda create -n back python=3.10 -y
(base) conda activate back
(back) pip install -r requirements.txt
(back) apt install git-lfs
(back) git lfs install
(back) git config --global credential.helper store
(back) huggingface-cli login
```

⭐️ 이 후 실행 컴퓨터의 환경에 맞게 pytorch를 설치해주셔야 합니다! ⭐️

### 데이터셋 로드

```
(back) cd back
(back) mkdir hub
(back) cd hub
(back) git clone https://huggingface.co/datasets/RecDol/PLAYLIST
(back) git clone https://huggingface.co/datasets/RecDol/index
(back) git clone https://huggingface.co/datasets/RecDol/CsvFiles
```

### 서버 실행

```
python main.py
```

⭐️ 만약 데이터를 새로 업데이트하고 싶다면 저장소에서 새로 pull 받아올 수 있도록 root_router.py에서 `is_data_pull=True`로 설정해주세요! ⭐️
