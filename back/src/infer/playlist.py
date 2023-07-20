import os
import datasets
from PIL import Image
from io import BytesIO
from fastapi import File
from datasets import Dataset
from huggingface_hub import Repository
from transformers import AutoImageProcessor, AutoModel, ViTImageProcessor, ViTModel

from src.utils import create_dir, get_first_dir


class PlaylistIdExtractor:
    def __init__(self, k: int, is_data_pull: bool):
        self.k = k
        self.is_data_pull = is_data_pull

        self.set_path()
        self.load_dataset()
        self.load_model()

    def set_path(self):
        # set and create base path
        self.HUB_PATH = "./hub/"
        create_dir(self.HUB_PATH)

        # set model path
        self.MODEL_REPO = f"Recdol/PL_Multilabel"

        self.WEATHER_MODEL_VERSION = "weather-19_023325"
        self.WEATHER_SUB = f"weather/{self.WEATHER_MODEL_VERSION}/{self.WEATHER_MODEL_VERSION}_huggingface"

        self.SIT_MODEL_VERSION = "sit-19_055337"
        self.SIT_SUB = f"sit/{self.SIT_MODEL_VERSION}/{self.SIT_MODEL_VERSION}_huggingface"

        self.MOOD_MODEL_VERSION = "mood-19_110133"
        self.MOOD_SUB = f"mood/{self.MOOD_MODEL_VERSION}/{self.MOOD_MODEL_VERSION}_huggingface"

        # set data path
        self.DATA_PATH = os.path.join(self.HUB_PATH, "PLAYLIST")
        mood_path = os.path.join(self.DATA_PATH, "mood")
        sit_path = os.path.join(self.DATA_PATH, "sit")
        weather_path = os.path.join(self.DATA_PATH, "weather")

        self.MOOD_DATA = os.path.join(mood_path, get_first_dir(mood_path))
        self.SIT_DATA = os.path.join(sit_path, get_first_dir(sit_path))
        self.WEATHER_DATA = os.path.join(weather_path, get_first_dir(weather_path))

        # set faiss path
        self.FAISS_PATH = os.path.join(self.HUB_PATH, "index")
        self.WEATHER_FAISS = os.path.join(self.FAISS_PATH, "weather.index")
        self.SIT_FAISS = os.path.join(self.FAISS_PATH, "sit.index")
        self.MOOD_FAISS = os.path.join(self.FAISS_PATH, "mood.index")

    def load_dataset(self):
        if self.is_data_pull:
            Repository(local_dir=self.DATA_PATH).git_pull()
            Repository(local_dir=self.FAISS_PATH).git_pull()

        self.weather_dataset = datasets.load_from_disk(self.WEATHER_DATA)
        self.weather_dataset.load_faiss_index(index_name="embeddings", file=self.WEATHER_FAISS)

        self.sit_dataset = datasets.load_from_disk(self.SIT_DATA)
        self.sit_dataset.load_faiss_index(index_name="embeddings", file=self.SIT_FAISS)

        self.mood_dataset = datasets.load_from_disk(self.MOOD_DATA)
        self.mood_dataset.load_faiss_index(index_name="embeddings", file=self.MOOD_FAISS)

    def load_model(self):
        self.weather_processor = AutoImageProcessor.from_pretrained(self.MODEL_REPO, subfolder=self.WEATHER_SUB)
        self.weather_model = AutoModel.from_pretrained(self.MODEL_REPO, subfolder=self.WEATHER_SUB)

        self.sit_processor = AutoImageProcessor.from_pretrained(self.MODEL_REPO, subfolder=self.SIT_SUB)
        self.sit_model = AutoModel.from_pretrained(self.MODEL_REPO, subfolder=self.SIT_SUB)

        self.mood_processor = AutoImageProcessor.from_pretrained(self.MODEL_REPO, subfolder=self.MOOD_SUB)
        self.mood_model = AutoModel.from_pretrained(self.MODEL_REPO, subfolder=self.MOOD_SUB)

    def decode_input_image(self, encoded_image) -> Image:
        pil_image = Image.open(BytesIO(encoded_image.file.read()))
        return pil_image

    def get_weather_playlist_id(self, image_path: str) -> list[int]:
        # pil_image = self.decode_input_image(image)
        pil_image = Image.open(image_path)
        retrieved_examples = self.get_similar_images_topk(pil_image, self.weather_processor, self.weather_model, self.weather_dataset, k=self.k)
        return [retrieved_examples["playlist_id"][i] for i in range(self.k)]

    def get_sit_playlist_id(self, image_path: str) -> list[int]:
        # pil_image = self.decode_input_image(image)
        pil_image = Image.open(image_path)
        retrieved_examples = self.get_similar_images_topk(pil_image, self.sit_processor, self.sit_model, self.sit_dataset, k=self.k)
        return [retrieved_examples["playlist_id"][i] for i in range(self.k)]

    def get_mood_playlist_id(self, image_path: str) -> list[int]:
        # pil_image = self.decode_input_image(image)
        pil_image = Image.open(image_path)
        retrieved_examples = self.get_similar_images_topk(pil_image, self.mood_processor, self.mood_model, self.mood_dataset, k=self.k)
        return [retrieved_examples["playlist_id"][i] for i in range(self.k)]

    def get_similar_images_topk(self, query_image: Image, processor: ViTImageProcessor, model: ViTModel, dataset: Dataset, k: int) -> dict:
        query_embedding = model(**processor(query_image, return_tensors="pt"))
        query_embedding = query_embedding.last_hidden_state[:, 0].detach().numpy().squeeze()
        scores, retrieved_examples = dataset.get_nearest_examples("embeddings", query_embedding, k=k)
        return retrieved_examples
