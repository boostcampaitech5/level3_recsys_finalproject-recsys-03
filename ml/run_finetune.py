import os
import hydra
import torch
import wandb
from huggingface_hub import HfApi
from src.data.datamodule import DataModule
from src.model.tag_classifier import TagClassifier
from src.trainer import Trainer
from src.utils import set_seed, get_timestamp, login_wandb, init_wandb, generate_predict_result_csv, upload_HFHub


def main(config) -> None:
    set_seed(config.seed)
    config.timestamp = get_timestamp()
    config.wandb.name = f"{config.data.tag_type}-{config.timestamp}"
    login_wandb()
    init_wandb(config)

    datamodule = DataModule(config)
    tag_classifier = TagClassifier(config, datamodule.num_labels, datamodule.id2label, datamodule.label2id)
    trainer = Trainer(config, tag_classifier, datamodule)

    trainer.train()
    trainer.test()

    if config.trainer.inference:
        probs: list[torch.Tensor] = trainer.predict()
        generate_predict_result_csv(config, probs, datamodule.test_dataset, datamodule.labels)

    upload_HFHub(config)

    wandb.finish()


@hydra.main(version_base="1.2", config_path="configs/finetune", config_name="config.yaml")
def main_hydra(config) -> None:
    main(config)


if __name__ == "__main__":
    main_hydra()
