import os
import datasets
from PIL import Image
from io import BytesIO
from fastapi import File
from datasets import Dataset
from transformers import AutoImageProcessor, AutoModel, ViTImageProcessor, ViTModel

 
class PlaylistIdExtractor:
    def __init__(self, k: int):
        self.k = k
        self.set_path()
        self.load_dataset()
        self.load_model()

    def set_path(self):
        self.CKPT_PATH = "./configs/"
        self.WEATHER_MODEL_PATH = os.path.join(self.CKPT_PATH, "weather/weather-17_061939_huggingface")

        self.DATASET_PATH = "./datasets/"
        self.WEATHER_DATA = os.path.join(self.DATASET_PATH, "weather_dataset")
        self.WEATEHR_INDEX = os.path.join(self.DATASET_PATH, "weather.index")

    def load_dataset(self):
        self.weather_dataset = datasets.load_from_disk(self.WEATHER_DATA)
        self.weather_dataset.load_faiss_index(index_name="embeddings", file=self.WEATEHR_INDEX)

    def load_model(self):
        self.weather_processor = AutoImageProcessor.from_pretrained(self.WEATHER_MODEL_PATH)
        self.weather_model = AutoModel.from_pretrained(self.WEATHER_MODEL_PATH)

    def decode_input_image(self, encoded_image) -> Image:
        pil_image = Image.open(BytesIO(encoded_image.file.read()))
        return pil_image

    def get_weather_playlist_id(self, image: File) -> list[int]:
        pil_image = self.decode_input_image(image)
        retrieved_examples = self.get_similar_images_topk(pil_image, self.weather_processor, self.weather_model, self.weather_dataset, k=self.k)
        return [retrieved_examples["playlist_id"][i] for i in range(self.k)]

    def get_similar_images_topk(self, query_image: Image, processor: ViTImageProcessor, model: ViTModel, dataset: Dataset, k: int) -> dict:
        query_embedding = model(**processor(query_image, return_tensors="pt"))
        query_embedding = query_embedding.last_hidden_state[:, 0].detach().numpy().squeeze()
        scores, retrieved_examples = dataset.get_nearest_examples("embeddings", query_embedding, k=k)
        return retrieved_examples