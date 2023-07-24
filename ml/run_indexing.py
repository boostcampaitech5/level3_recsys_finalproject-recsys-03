import os
import faiss
import hydra
from huggingface_hub import HfApi
from transformers import AutoImageProcessor, AutoModel
from src.utils import set_seed, encode, read_dataset


def main(config) -> None:
    # set
    name = config.name
    data_dir = config.data_dir
    output_dir = config.output_dir
    tag_type = config.tag_type
    model_repo = config.model_repo_id
    index_repo = config.index_repo_id
    subfolder = f"{tag_type}/{name}/{name}_huggingface"
    save_dir = os.path.join(output_dir, name)
    save_file = f"{save_dir}/{name}.index"
    set_seed(config.seed)

    # init model
    processor = AutoImageProcessor.from_pretrained(model_repo, subfolder=subfolder)
    model = AutoModel.from_pretrained(model_repo, subfolder=subfolder)
    # load dataset
    dataset = read_dataset(data_dir, tag_type)
    # encode
    dataset_with_embeddings = dataset.map(lambda x: {"embeddings": encode(x["image"], processor, model)})
    # add faiss index
    dataset_with_embeddings.add_faiss_index(column="embeddings", metric_type=faiss.METRIC_INNER_PRODUCT)
    # save faiss index
    dataset_with_embeddings.save_faiss_index(index_name="embeddings", file=os.path.join(save_dir, f"{name}.index"))
    # save dataset
    dataset_with_embeddings.drop_index(index_name="embeddings")
    dataset_with_embeddings.save_to_disk(os.path.join(save_dir, f"{tag_type}_dataset"))

    api = HfApi()
    api.upload_file(
        path_or_fileobj=save_file, path_in_repo=f"{tag_type}/{name}.index", repo_id=index_repo, commit_message=f"upload index: {name}", repo_type="dataset"
    )

@hydra.main(version_base="1.2", config_path="configs/indexing", config_name="config.yaml")
def main_hydra(config) -> None:
    main(config)


if __name__ == "__main__":
    main_hydra()
