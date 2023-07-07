from typing import Optional, Tuple
import os
import torch
import wandb
import dotenv
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datasets import Dataset
from datasets import (
    load_dataset,
)


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


def load_huggingface_dataset(seed: int = 42, num_samples: int = 100, name: str = "beans", split: str = "train") -> Dataset:
    dataset = load_dataset(name, split=split)
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
