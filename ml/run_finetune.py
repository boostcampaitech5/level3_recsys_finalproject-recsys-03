import hydra
import wandb
from src.data.datamodule import DataModule
from src.model.tag_classifier import TagClassifier
from src.trainer import Trainer
from src.utils import (
    set_seed,
    get_timestamp,
    login_wandb,
    init_wandb,
)


def main(config) -> None:
    set_seed(config.seed)
    config.timestamp = get_timestamp()
    config.wandb.name = f"work-{config.timestamp}"
    login_wandb()
    init_wandb(config)

    datamodule = DataModule(config)
    tag_classifier = TagClassifier(config)
    trainer = Trainer(config, tag_classifier, datamodule)

    trainer.train()
    trainer.test()

    wandb.finish()


@hydra.main(version_base="1.2", config_path="configs/finetune", config_name="config.yaml")
def main_hydra(config) -> None:
    main(config)


if __name__ == "__main__":
    main_hydra()
