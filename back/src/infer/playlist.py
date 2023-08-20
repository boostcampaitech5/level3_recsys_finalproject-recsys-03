import os
import faiss
import datasets
import numpy as np
from PIL import Image
from io import BytesIO
from typing import Tuple
from datasets import Dataset
from huggingface_hub import Repository
from typing import List, Optional
from transformers import AutoImageProcessor, AutoModel, ViTImageProcessor, ViTModel
from ..config import AppConfig


class PlaylistIdExtractor:
    def __init__(self, config: AppConfig, k: int, is_data_pull: bool):
        self.config = config
        self.k = k
        self.is_data_pull = is_data_pull

        self._set_up_path()
        self.load_dataset()
        self.load_model()

    def _set_up_path(self, config: AppConfig):
        # set model path
        self.WEATHER_SUB = f"weather/{config.weather_model_version}/{config.weather_model_version}_huggingface"
        self.SIT_SUB = f"sit/{config.sit_model_version}/{config.sit_model_version}_huggingface"
        self.MOOD_SUB = f"mood/{config.mood_model_version}/{config.mood_model_version}_huggingface"

        # set data path
        self.DATA_PATH = os.path.join(config.hub_path, "PLAYLIST")
        self.MOOD_DATA_PATH = os.path.join(self.DATA_PATH, "mood")
        self.SIT_DATA_PATH = os.path.join(self.DATA_PATH, "sit")
        self.WEATHER_DATA_PATH = os.path.join(self.DATA_PATH, "weather")

        # set faiss path
        self.FAISS_PATH = os.path.join(config.hub_path, "faiss_index")
        self.WEATHER_FAISS_PATH = os.path.join(self.FAISS_PATH, f"weather/{config.weather_index_version}.index")
        self.SIT_FAISS_PATH = os.path.join(self.FAISS_PATH, f"sit/{config.sit_index_version}.index")
        self.MOOD_FAISS_PATH = os.path.join(self.FAISS_PATH, f"mood/{config.mood_index_version}.index")

    def load_index_file_path(self, path: str) -> str:
        file_list = os.listdir(path)
        for file in file_list:
            if ".index" in file:
                return os.path.join(path, file)

    def read_dataset(self, data_dir: str) -> datasets.Dataset:
        dir_list = os.listdir(data_dir)

        dsets: List[Optional[datasets.Dataset]] = []
        for dir in dir_list:
            print("path", os.path.join(data_dir, dir))
            cur_dataset = datasets.load_from_disk(os.path.join(data_dir, dir))
            dsets.append(cur_dataset)

        dataset = datasets.concatenate_datasets(dsets)
        return dataset

    def load_dataset(self):
        if self.is_data_pull:
            Repository(local_dir=self.DATA_PATH).git_pull()
            Repository(local_dir=self.FAISS_PATH).git_pull()

        self.weather_dataset = self.read_dataset(self.WEATHER_DATA_PATH)
        self.weather_dataset.load_faiss_index(index_name="embeddings", file=self.WEATHER_FAISS_PATH)

        self.sit_dataset = self.read_dataset(self.SIT_DATA_PATH)
        self.sit_dataset.load_faiss_index(index_name="embeddings", file=self.SIT_FAISS_PATH)

        self.mood_dataset = self.read_dataset(self.MOOD_DATA_PATH)
        self.mood_dataset.load_faiss_index(index_name="embeddings", file=self.MOOD_FAISS_PATH)

    def load_model(self):
        self.weather_processor = AutoImageProcessor.from_pretrained(self.config.model_repo, subfolder=self.WEATHER_SUB)
        self.weather_model = AutoModel.from_pretrained(self.config.model_repo, subfolder=self.WEATHER_SUB)

        self.sit_processor = AutoImageProcessor.from_pretrained(self.config.model_repo, subfolder=self.SIT_SUB)
        self.sit_model = AutoModel.from_pretrained(self.config.model_repo, subfolder=self.SIT_SUB)

        self.mood_processor = AutoImageProcessor.from_pretrained(self.config.model_repo, subfolder=self.MOOD_SUB)
        self.mood_model = AutoModel.from_pretrained(self.config.model_repo, subfolder=self.MOOD_SUB)

    def decode_input_image(self, encoded_image) -> Image:
        pil_image = Image.open(BytesIO(encoded_image.file.read()))
        return pil_image

    def get_weather_playlist_id(self, image_path: str) -> list[int]:
        # pil_image = self.decode_input_image(image)
        pil_image = Image.open(image_path)
        scores, retrieved_examples = self.get_similar_images_topk(
            pil_image, self.weather_processor, self.weather_model, self.weather_dataset, k=self.k
        )
        return list(scores), [retrieved_examples["playlist_id"][i] for i in range(self.k)]

    def get_sit_playlist_id(self, image_path: str) -> list[int]:
        # pil_image = self.decode_input_image(image)
        pil_image = Image.open(image_path)
        scores, retrieved_examples = self.get_similar_images_topk(pil_image, self.sit_processor, self.sit_model, self.sit_dataset, k=self.k)
        return list(scores), [retrieved_examples["playlist_id"][i] for i in range(self.k)]

    def get_mood_playlist_id(self, image_path: str) -> list[int]:
        # pil_image = self.decode_input_image(image)
        pil_image = Image.open(image_path)
        scores, retrieved_examples = self.get_similar_images_topk(pil_image, self.mood_processor, self.mood_model, self.mood_dataset, k=self.k)
        return list(scores), [retrieved_examples["playlist_id"][i] for i in range(self.k)]

    def get_similar_images_topk(
        self, query_image: Image, processor: ViTImageProcessor, model: ViTModel, dataset: Dataset, k: int
    ) -> Tuple[np.ndarray, dict]:
        query_embedding = model(**processor(query_image, return_tensors="pt"))
        query_embedding = query_embedding.last_hidden_state[:, 0].detach().numpy()
        faiss.normalize_L2(query_embedding)
        scores, retrieved_examples = dataset.get_nearest_examples("embeddings", query_embedding.squeeze(), k=k)
        return scores, retrieved_examples
