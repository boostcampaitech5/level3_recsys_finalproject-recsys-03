from typing import Optional
import os
import numpy as np
import torch
import lightning as L
import datasets
from torch.utils.data import DataLoader
from transformers import AutoImageProcessor
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
from src.utils import train_val_test_split, read_dataset


class DataModule(L.LightningDataModule):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.backbone = config.model.backbone
        self.batch_size = config.data.batch_size
        self.num_workers = config.data.num_workers
        self.tag_type = config.data.tag_type
        self.data_dir = config.path.data_dir
        self.output_dir = config.path.output_dir
        self.name = config.wandb.name

        self.dataset: datasets.Dataset = read_dataset(self.data_dir, self.tag_type)
        self.labels: list = [label for label in self.dataset.features.keys() if label not in ["playlist_id", "playlist_img_url", "image"]]

        self.train_dataset: Optional[datasets.Dataset] = None
        self.val_dataset: Optional[datasets.Dataset] = None
        self.test_dataset: Optional[datasets.Dataset] = None

        self._train_transforms: Optional[A.Compose] = None
        self._eval_transforms: Optional[A.Compose] = None

    def prepare_data(self) -> None:
        self.train_dataset, self.val_dataset, self.test_dataset = train_val_test_split(self.dataset)

    def setup(self, stage: Optional[str] = None):
        processor = AutoImageProcessor.from_pretrained(self.backbone)
        image_mean = processor.image_mean
        image_std = processor.image_std
        h = processor.size["height"]
        w = processor.size["width"]
        self.save_hf_processor(processor)

        self._train_transforms = A.Compose(
            [
                A.Resize(h, w),
                A.RandomCrop(h, w),
                A.HorizontalFlip(),
                A.Normalize(mean=image_mean, std=image_std),
                ToTensorV2(),
            ]
        )

        self._eval_transforms = A.Compose(
            [
                A.Resize(h, w),
                A.CenterCrop(h, w),
                A.Normalize(mean=image_mean, std=image_std),
                ToTensorV2(),
            ]
        )

        self.train_dataset.set_transform(self.preprocess_train)
        self.val_dataset.set_transform(self.preprocess_eval)
        self.test_dataset.set_transform(self.preprocess_eval)

    def _transform_label(self, examples):
        label_batch = {label: examples[label] for label in self.labels}
        label_matrix = np.zeros((len(examples["image"]), (self.num_labels)))
        for idx, label in enumerate(self.labels):
            label_matrix[:, idx] = label_batch[label]
        return label_matrix.tolist()

    def preprocess_train(self, examples):
        examples["pixel_values"] = [self._train_transforms(image=np.array(image))["image"] for image in examples["image"]]
        examples["labels"] = self._transform_label(examples)
        return examples

    def preprocess_eval(self, examples):
        examples["pixel_values"] = [self._eval_transforms(image=np.array(image))["image"] for image in examples["image"]]
        examples["labels"] = self._transform_label(examples)
        return examples

    def save_hf_processor(self, processor):
        dirpath = os.path.join(self.output_dir, self.name)
        filename = self.name + "_huggingface"
        processor.save_pretrained(os.path.join(dirpath, filename))

    def collate_fn(self, examples):
        pixel_values = torch.stack([example["pixel_values"] for example in examples])
        labels = torch.tensor([example["labels"] for example in examples])
        return {"pixel_values": pixel_values, "labels": labels}

    def train_dataloader(self) -> DataLoader:
        loader = DataLoader(self.train_dataset, shuffle=True, num_workers=self.num_workers, collate_fn=self.collate_fn, batch_size=self.batch_size)
        return loader

    def val_dataloader(self) -> DataLoader:
        loader = DataLoader(self.val_dataset, shuffle=False, num_workers=self.num_workers, collate_fn=self.collate_fn, batch_size=self.batch_size)
        return loader

    def test_dataloader(self) -> DataLoader:
        loader = DataLoader(self.test_dataset, shuffle=False, num_workers=self.num_workers, collate_fn=self.collate_fn, batch_size=self.batch_size)
        return loader

    def predict_dataloader(self) -> DataLoader:
        loader = DataLoader(self.test_dataset, shuffle=False, num_workers=self.num_workers, collate_fn=self.collate_fn, batch_size=self.batch_size)
        return loader

    @property
    def num_labels(self):
        return len(self.labels)

    @property
    def id2label(self):
        return {id: label for id, label in enumerate(self.labels)}

    @property
    def label2id(self):
        return {label: id for id, label in enumerate(self.labels)}
