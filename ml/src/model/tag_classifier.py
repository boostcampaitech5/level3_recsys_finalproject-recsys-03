import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import lightning as L
from transformers import AutoModelForImageClassification
from sklearn.metrics import accuracy_score


class TagClassifier(L.LightningModule):
    def __init__(self, config, num_labels: int, id2label: dict, label2id: dict):
        super().__init__()
        self.backbone = config.model.backbone
        self.model = AutoModelForImageClassification.from_pretrained(
            self.backbone,
            num_labels=num_labels,
            id2label=id2label,
            label2id=label2id,
            ignore_mismatched_sizes=True,
        )
        self.loss_fn = nn.BCEWithLogitsLoss()
        self.sigmoid = nn.Sigmoid()
        self.config = config
        self.batch_size = config.data.batch_size
        self.lr = config.model.lr
        self.threshold = config.model.threshold
        self.train_step_outputs = []
        self.shared_eval_step_outputs = []
        self.save_hyperparameters(ignore=["model"])

    def forward(self, pixel_values):
        outputs = self.model(pixel_values)
        return outputs.logits

    def training_step(self, batch, batch_idx):
        pixel_values = batch["pixel_values"]
        labels = batch["labels"]
        logits = self(pixel_values)

        loss = self._compute_loss(logits, labels)
        score = self._compute_score(logits, labels)
        output = {"loss": loss, "score": score}
        self.train_step_outputs.append(output)
        return output

    def on_train_epoch_end(self):
        outputs: list[dict[torch.Tensor, np.ndarray]] = self.train_step_outputs

        avg_loss = torch.stack([output["loss"] for output in outputs]).mean()
        avg_score = np.vstack([output["score"] for output in outputs]).mean()

        log_dict = {
            f"train_loss": avg_loss,
            f"train_score": avg_score,
        }

        self.log_dict(log_dict)
        self.train_step_outputs.clear()
        return log_dict

    @torch.no_grad()
    def validation_step(self, batch, batch_idx):
        return self._shared_eval_step(batch, batch_idx, "val")

    def on_validation_epoch_end(self):
        return self._on_shared_eval_epoch_end("val")

    @torch.no_grad()
    def test_step(self, batch, batch_idx):
        return self._shared_eval_step(batch, batch_idx, "test")

    def on_test_epoch_end(self):
        return self._on_shared_eval_epoch_end("test")

    @torch.no_grad()
    def predict_step(self, batch, batch_idx):
        """TODO"""
        return

    def configure_optimizers(self):
        optimizer = optim.AdamW(self.model.parameters(), lr=self.lr)
        return optimizer

    def _compute_loss(self, logits, labels):
        loss = self.loss_fn(logits, labels)
        return loss

    def _compute_score(self, logits, labels):
        probs = self.sigmoid(logits.cpu())
        preds = np.where(probs > self.threshold, 1, 0)
        score = accuracy_score(labels.cpu().numpy(), preds)
        return score

    def _shared_eval_step(self, batch, batch_idx, prefix: str):
        pixel_values = batch["pixel_values"]
        labels = batch["labels"]
        logits = self(pixel_values)

        loss = self._compute_loss(logits, labels)
        score = self._compute_score(logits, labels)
        output = {"loss": loss, "score": score}
        self.shared_eval_step_outputs.append(output)
        return output

    def _on_shared_eval_epoch_end(self, prefix: str):
        outputs: list[dict[torch.Tensor, np.ndarray]] = self.shared_eval_step_outputs

        avg_loss = torch.stack([output["loss"] for output in outputs]).mean()
        avg_score = np.vstack([output["score"] for output in outputs]).mean()

        log_dict = {
            f"{prefix}_loss": avg_loss,
            f"{prefix}_score": avg_score,
        }

        self.log_dict(log_dict)
        self.shared_eval_step_outputs.clear()
        return log_dict

    def save_hf_checkpoint(self, path):
        self.model.save_pretrained(path)
