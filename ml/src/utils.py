import re
import os
import ast
import torch
import wandb
import dotenv
import random
import urllib
import datasets
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
import pytesseract as pt
from datetime import datetime
import matplotlib.pyplot as plt
from huggingface_hub import HfApi
from typing import Optional, Tuple, List


def set_seed(seed) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True


def get_timestamp(date_format: str = "%d_%H%M%S") -> str:
    timestamp = datetime.now()
    return timestamp.strftime(date_format)


def login_wandb() -> None:
    dotenv.load_dotenv()
    WANDB_API_KEY = os.environ.get("WANDB_API_KEY")
    wandb.login(key=WANDB_API_KEY)


def init_wandb(config, k: Optional[int] = None, group: Optional[int] = None) -> None:
    wandb.init(
        project=config.wandb.project + "TagClassification",
        entity=config.wandb.entity,
        name=config.wandb.name + f"_fold_{k}" if k is not None else config.wandb.name,
        group=group,
    )


def load_huggingface_dataset(seed: int = 42, num_samples: int = 100, name: str = "beans", split: str = "train") -> datasets.Dataset:
    dataset = datasets.load_dataset(name, split=split)
    return dataset.shuffle(seed=seed).select(range(num_samples))


def encode(image, encoder, model) -> torch.Tensor:
    image_pp = encoder(image, return_tensors="pt")
    features = model(**image_pp).last_hidden_state[:, 0].detach().numpy()
    return features.squeeze()


def fetch_similar_images_topk(query, encoder, model, dataset, k: int) -> Tuple[list, list]:
    query_embedding = model(**encoder(query, return_tensors="pt"))
    query_embedding = query_embedding.last_hidden_state[:, 0].detach().numpy().squeeze()
    scores, retrieved_examples = dataset.get_nearest_examples("embeddings", query_embedding, k=k)
    return scores, retrieved_examples


def plot_images(images, labels, id2label, k) -> None:
    if not isinstance(labels, list):
        labels = labels.tolist()

    plt.figure(figsize=(21, 10))
    columns = int(k + 1)
    for i, image in enumerate(images):
        label_id = int(labels[i])
        ax = plt.subplot(int(len(images) / columns + 1), columns, i + 1)
        if i == 0:
            ax.set_title("Query Image\n")
        else:
            ax.set_title("Similar Image # " + str(i) + "\nLabel: {}".format(id2label[label_id]))
        plt.imshow(np.array(image).astype("int"))
        plt.axis("off")


def str2list(data: pd.DataFrame, columns: list) -> None:
    for col in columns:
        data[col] = data[col].apply(lambda x: ast.literal_eval(x))


def read_image(url: str, mode: str = "RGB"):
    image = Image.open(urllib.request.urlretrieve(url)[0]).convert(mode)
    return image


def read_data(file_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_name, keep_default_na=False)
    df.columns = [col.lower() for col in df.columns]
    str2list(df, ["playlist_songs", "playlist_tags"])
    return df


def train_val_test_split(dataset: datasets.Dataset) -> Tuple[datasets.Dataset, datasets.Dataset, datasets.Dataset]:
    train_test_splits = dataset.train_test_split(test_size=0.1)
    train = train_test_splits["train"]
    test = train_test_splits["test"]

    train_val_splits = train.train_test_split(test_size=0.1)
    train = train_val_splits["train"]
    val = train_val_splits["test"]

    return train, val, test


def get_empty_img(df: pd.DataFrame) -> List[int]:
    error_idx = []
    for idx in df.index:
        try:
            sliced_url = df.at[idx, "playlist_img_url"][:-22]
            image = read_image(sliced_url)
        except:
            error_idx.append(idx)
    return error_idx


def tag_uniques(tag_col: pd.Series) -> List[str]:
    tag_list = []
    for tag in tag_col:
        tag_list += tag
    tag_list = list(set(tag_list))
    return tag_list


def get_ocr_result(df: pd.DataFrame) -> List[str]:
    ocr_result = []
    err_list = []
    print("-----------------------OCR for Editor's Choice-----------------------")
    for i, url in enumerate(tqdm(df.playlist_img_url)):
        try:
            image = read_image(url, mode="L")
            text = pt.image_to_string(image)
            ocr_result.append(text)
        except:
            err_list.append(i)
            ocr_result.append("error_img")
            pass
    return ocr_result


def get_editors_choice(ocr_result: List[str]) -> List[int]:
    editors_choice = []
    for i, txt in enumerate(ocr_result):
        if bool(re.search("EDITOR", txt)):
            editors_choice.append(i)
    return editors_choice


def generate_predict_result_csv(config, probs: list[torch.Tensor], dataset: datasets.Dataset, labels: list[str]) -> None:
    probs = np.concatenate(probs)
    df = pd.DataFrame(probs, columns=[f"prob_{label}" for label in labels])

    for label in labels:
        label_values = []
        for i in range(probs.shape[0]):
            label_values.append(dataset[i][label])
        df[label] = label_values

    ids = []
    urls = []
    for i in range(probs.shape[0]):
        ids.append(dataset[i]["playlist_id"])
        urls.append(dataset[i]["playlist_img_url"])

    df["id"] = ids
    df["url"] = urls

    df = df[["id", "url"] + [f"prob_{label}" for label in labels] + labels]

    dirpath = os.path.join(config.path.output_dir, config.wandb.name)
    filename = f"{config.wandb.name}_predict_result.csv"
    df.to_csv(os.path.join(dirpath, filename), index=False)

    
def concat(data_dir: str, tag_type:str) -> datasets:
    data_path = os.path.join(data_dir, f"{tag_type}_dataset")
    dir_list = os.listdir(data_path)
    for i, dir in enumerate(dir_list):
        if i == 0:
            dataset = datasets.load_from_disk(os.path.join(data_dir, f"{tag_type}_dataset", dir))
        else:
            d_set = datasets.load_from_disk(os.path.join(data_dir, f"{tag_type}_dataset", dir))
            dataset = datasets.concatenate_datasets([dataset, d_set])
    return dataset


def upload_HFHub(name: str, dirpath:str)-> None:
    api = HfApi()
    repo_id = f"RecDol/{name}"

    api.create_repo(
        repo_id = repo_id,
        repo_type = "model",
        private = True
    )

    api.upload_folder(
        folder_path=dirpath,
        path_in_repo = name,
        repo_id = repo_id,
        commit_message = f"upload: {name}"
    )
