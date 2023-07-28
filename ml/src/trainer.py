import os
from typing import Optional
import numpy as np
import lightning as L
from src.checkpoint_io import HFCheckpointIO
from lightning.pytorch.loggers import WandbLogger
from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping

class Trainer:
    def __init__(self, config, model: L.LightningModule, datamodule: L.LightningDataModule, k: Optional[int] = None):
        self.config = config
        self.accelerator = config.trainer.accelerator
        self.devices = config.trainer.devices
        self.patience = config.trainer.patience
        self.max_epochs = config.trainer.max_epochs
        self.output_dir = config.path.output_dir
        self.name = config.wandb.name + f"_fold_{k}" if k is not None else config.wandb.name
        self.project = config.wandb.project

        self.model = model
        self.datamodule = datamodule
        self.trainer = self._build_trainer()

    def train(self) -> None:
        self.trainer.fit(self.model, self.datamodule)

    def test(self) -> None:
        self.trainer.test(self.model, self.datamodule, ckpt_path="best")

    def predict(self) -> np.ndarray:
        pred = self.trainer.predict(self.model, self.datamodule, ckpt_path="best")
        return pred

    def _build_trainer(self) -> L.Trainer:
        trainer = L.Trainer(
            accelerator=self.accelerator,
            devices=self.devices,
            logger=self._build_wandb_logger(),
            callbacks=[self._build_ckpt_callback(), self._build_earlystopping()],
            max_epochs=self.max_epochs,
            plugins=HFCheckpointIO(model=self.model),
        )
        return trainer

    def _build_ckpt_callback(self) -> ModelCheckpoint:
        ckpt_callback = ModelCheckpoint(
            dirpath=os.path.join(self.output_dir, self.name),
            filename=self.name,
            monitor="val_loss",
            save_last=False,
            save_top_k=1,
            mode="min",
            verbose=True,
        )
        return ckpt_callback

    def _build_wandb_logger(self) -> WandbLogger:
        wandb_logger = WandbLogger(
            name=self.name,
            project=self.project,
        )
        return wandb_logger

    def _build_earlystopping(self) -> EarlyStopping:
        early_stopping = EarlyStopping(
            monitor="val_loss", 
            patience=self.patience, 
            mode="min"
            )
        return early_stopping