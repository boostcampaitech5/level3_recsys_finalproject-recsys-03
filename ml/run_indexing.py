import hydra
from transformers import AutoImageProcessor, AutoModel
from src.utils import (
    set_seed,
    load_huggingface_dataset,
    encode,
)


def main(config) -> None:
    # set
    name = config.name
    set_seed(config.seed)
    # init model
    ckpt = f"./output/{name}_huggingface"
    processor = AutoImageProcessor.from_pretrained(ckpt)
    model = AutoModel.from_pretrained(ckpt)
    # load dataset
    dataset = load_huggingface_dataset()
    # encode
    dataset_with_embeddings = dataset.map(lambda x: {"embeddings": encode(x["image"], processor, model)})
    # add faiss index
    dataset_with_embeddings.add_faiss_index(column="embeddings")
    # save faiss index
    dataset_with_embeddings.save_faiss_index(index_name="embeddings", file=f"./output/{name}/my_index.faiss")
    # save dataset
    dataset_with_embeddings.drop_index(index_name="embeddings")
    dataset_with_embeddings.save_to_disk(f"./output/{name}/my_datasets")


@hydra.main(version_base="1.2", config_path="configs/indexing", config_name="config.yaml")
def main_hydra(config) -> None:
    main(config)


if __name__ == "__main__":
    main_hydra()
