import os
import hydra
import datasets
from transformers import AutoImageProcessor, AutoModel
from src.utils import (
    set_seed,
    encode,
)


def main(config) -> None:
    # set
    name = config.name
    data_dir = config.data_dir
    output_dir = config.output_dir
    tag_type = config.tag_type
    save_dir = os.path.join(output_dir, name)
    set_seed(config.seed)

    # init model
    ckpt_dirpath = os.path.join(output_dir, name)
    ckpt_filename = f"{name}_huggingface"
    ckpt = os.path.join(ckpt_dirpath, ckpt_filename)
    processor = AutoImageProcessor.from_pretrained(ckpt)
    model = AutoModel.from_pretrained(ckpt)
    # load dataset
    dataset = datasets.load_from_disk(os.path.join(data_dir, f"{tag_type}_dataset"))
    # encode
    dataset_with_embeddings = dataset.map(lambda x: {"embeddings": encode(x["image"], processor, model)})
    # add faiss index
    dataset_with_embeddings.add_faiss_index(column="embeddings")
    # save faiss index
    dataset_with_embeddings.save_faiss_index(index_name="embeddings", file=os.path.join(save_dir, f"{tag_type}.index"))
    # save dataset
    dataset_with_embeddings.drop_index(index_name="embeddings")
    dataset_with_embeddings.save_to_disk(os.path.join(save_dir, f"{tag_type}_dataset"))


@hydra.main(version_base="1.2", config_path="configs/indexing", config_name="config.yaml")
def main_hydra(config) -> None:
    main(config)


if __name__ == "__main__":
    main_hydra()
