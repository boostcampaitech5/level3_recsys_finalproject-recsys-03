import os
import hydra
import datasets
import pandas as pd
from src.utils import set_seed, generate_weather_df, read_image


def main(config) -> None:
    # set
    set_seed(config.seed)

    # csv to pd.DataFrame (version == playlists_0709_v2.csv)
    data_dir = config.path.data_dir
    csv_file = config.path.csv_file
    df = pd.read_csv(os.path.join(data_dir, csv_file))

    # generate subset dataset (tag == [weather, situation, mood])
    weather_subset = generate_weather_df(df)
    # mood_subset = generate_mood_df(df)

    # pd.DataFrame to datasets.Dataset
    weather_dataset = datasets.Dataset.from_pandas(weather_subset)
    # mood_dataset = datasets.Dataset.from_pandas(mood_subset)

    # map url to PIL.Image
    weather_dataset = weather_dataset.map(lambda x: {"image": read_image(x["playlist_img_url"][:-22])})
    # mood_dataset = mood_dataset.map(lambda x: {"image": read_image(x["playlist_img_url"][:-22])})

    # save dataset
    weather_dataset = weather_dataset.remove_columns("__index_level_0__")
    weather_dataset.save_to_disk(os.path.join(data_dir, "weather_dataset"))
    # mood_dataset = mood_dataset.remove_columns("__index_level_0__")
    # mood_dataset.save_to_disk(os.path.join(data_dir, "mood_dataset"))


@hydra.main(version_base="1.2", config_path="configs/preprocessing", config_name="config.yaml")
def main_hydra(config) -> None:
    main(config)


if __name__ == "__main__":
    main_hydra()
