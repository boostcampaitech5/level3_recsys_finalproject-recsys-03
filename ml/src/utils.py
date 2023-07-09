from typing import Optional, Tuple
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
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime


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


def generate_weather_df(df: pd.DataFrame) -> pd.DataFrame:
    df["w1"] = df.apply(lambda x: 1 if "봄" in x["tag_weather"] else 0, axis=1)
    df["w2"] = df.apply(lambda x: 1 if "여름" in x["tag_weather"] else 0, axis=1)
    df["w3"] = df.apply(lambda x: 1 if "가을" in x["tag_weather"] else 0, axis=1)
    df["w4"] = df.apply(lambda x: 1 if "겨울" in x["tag_weather"] else 0, axis=1)
    df["w5"] = df.apply(lambda x: 1 if "우중충한날" in x["tag_weather"] else 0, axis=1)

    cols = [
        "playlist_id",
        "playlist_img_url",
        "w1",
        "w2",
        "w3",
        "w4",
        "w5",
    ]
    weather_df = df[df["tag_weather_cnt"] > 0][cols]

    return weather_df


def read_image(url: str):
    image = Image.open(urllib.request.urlretrieve(url)[0]).convert("RGB")
    return image


def train_val_test_split(dataset: datasets.Dataset) -> Tuple[datasets.Dataset, datasets.Dataset, datasets.Dataset]:
    train_test_splits = dataset.train_test_split(test_size=0.1)
    train = train_test_splits["train"]
    test = train_test_splits["test"]

    train_val_splits = train.train_test_split(test_size=0.1)
    train = train_val_splits["train"]
    val = train_val_splits["test"]

    return train, val, test
