import os
import hydra
import datasets
import pandas as pd
from src.utils import set_seed, read_image
from src.preprocess import preprocess_data, generate_df


def main(config) -> None:
    # set
    set_seed(config.seed)

    # csv to pd.DataFrame (version == playlists.csv)
    data_dir = config.data_dir
    train_file = config.train_file
    tag_file = config.tag_file
    tag_type = config.tag_type

    # generate subset dataset (tag == [weather, situation, mood])
    pd.set_option("mode.chained_assignment", None)
    df = preprocess_data(data_dir, train_file, tag_file)
    data = generate_df(df, tag_type)

    # pd.DataFrame to datasets.Dataset
    dataset = datasets.Dataset.from_pandas(data)

    # map url to PIL.Image
    dataset = dataset.map(lambda x: {"image": read_image(x["playlist_img_url"][:-22])})

    # save dataset
    dataset = dataset.remove_columns("__index_level_0__")
    dataset.save_to_disk(os.path.join(data_dir, f"{tag_type}_dataset"))


@hydra.main(version_base="1.2", config_path="configs/preprocessing", config_name="config.yaml")
def main_hydra(config) -> None:
    main(config)


if __name__ == "__main__":
    main_hydra()
