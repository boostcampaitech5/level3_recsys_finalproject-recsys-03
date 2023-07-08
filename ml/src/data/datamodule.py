from typing import Optional
import os
import numpy as np
import torch
import lightning as L
from datasets import Dataset, load_dataset
from torch.utils.data import DataLoader
from transformers import AutoImageProcessor
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2


class DataModule(L.LightningDataModule):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.backbone = config.model.backbone
        self.batch_size = config.data.batch_size
        self.num_workers = config.data.num_workers
        self.output_dir = config.path.output_dir
        self.name = config.wandb.name

        self.train_dataset: Optional[Dataset] = None
        self.val_dataset: Optional[Dataset] = None
        self.test_dataset: Optional[Dataset] = None

        self.id2label: Optional[dict] = None
        self.label2id: Optional[dict] = None
        self.num_labels: Optional[int] = None

        self._train_transforms: Optional[A.Compose] = None
        self._eval_transforms: Optional[A.Compose] = None

    def prepare_data(self) -> None:
        train_dataset, self.test_dataset = load_dataset("beans", split=["train", "test"])
        splits = train_dataset.train_test_split(test_size=0.1)
        self.train_dataset = splits["train"]
        self.val_dataset = splits["test"]

        self.id2label = {id: label for id, label in enumerate(self.train_dataset.features["labels"].names)}
        self.label2id = {label: id for id, label in self.id2label.items()}
        self.num_labels = len(self.id2label)

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

    def preprocess_train(self, examples):
        examples["pixel_values"] = [self._train_transforms(image=np.array(image))["image"] for image in examples["image"]]
        return examples

    def preprocess_eval(self, examples):
        examples["pixel_values"] = [self._eval_transforms(image=np.array(image))["image"] for image in examples["image"]]
        return examples

    def save_hf_processor(self, processor):
        path = os.path.join(self.output_dir, self.name + "_huggingface")
        processor.save_pretrained(path)

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
