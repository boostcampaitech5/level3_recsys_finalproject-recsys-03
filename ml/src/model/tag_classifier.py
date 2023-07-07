import numpy as np
import torch
import torch.optim as optim
import torch.nn.functional as F
import lightning as L
from transformers import AutoModelForImageClassification


NUM_LABELS = 3
ID2LABEL = {0: "angular_leaf_spot", 1: "bean_rust", 2: "healthy"}
LABEL2ID = {"angular_leaf_spot": 0, "bean_rust": 1, "healthy": 2}


class TagClassifier(L.LightningModule):
    def __init__(self, config):
        super().__init__()
        self.backbone = config.model.backbone
        self.model = AutoModelForImageClassification.from_pretrained(
            self.backbone,
            num_labels=NUM_LABELS,
            id2label=ID2LABEL,
            label2id=LABEL2ID,
            ignore_mismatched_sizes=True,
        )
        self.config = config
        self.batch_size = config.data.batch_size
        self.lr = config.model.lr
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
        loss = F.cross_entropy(logits, labels)
        return loss

    def _compute_score(self, logits, labels):
        preds = logits.argmax(-1)
        correct = (preds == labels).sum().item()
        score = correct / self.batch_size
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
