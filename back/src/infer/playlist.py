import os
import faiss
import datasets
from PIL import Image
from datasets import Dataset, DatasetDict
from huggingface_hub import Repository
from transformers import AutoImageProcessor, AutoModel, ViTImageProcessor, ViTModel
from ..config import AppConfig


class PlaylistIdExtractor:
    def __init__(self, config: AppConfig, k: int, is_data_pull: bool):
        self.config = config
        self.k = k
        self.is_data_pull = is_data_pull

        self._set_up_path(config)
        self._load_dataset()
        self._load_model(config)

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

    def _read_dataset(self, data_dir: str) -> Dataset:
        dir_list = os.listdir(data_dir)

        dsets: list[Dataset | DatasetDict] = []
        for dir in dir_list:
            dataset_dir_path = os.path.join(data_dir, dir)
            cur_dataset = datasets.load_from_disk(dataset_dir_path)
            dsets.append(cur_dataset)

        return datasets.concatenate_datasets(dsets)

    def _load_dataset(self):
        if self.is_data_pull:
            try:
                Repository(local_dir=self.DATA_PATH).git_pull()
                Repository(local_dir=self.FAISS_PATH).git_pull()
            except OSError:
                # not installed lfs
                pass

        self.weather_dataset = self._read_dataset(self.WEATHER_DATA_PATH)
        self.weather_dataset.load_faiss_index(index_name="embeddings", file=self.WEATHER_FAISS_PATH)

        self.sit_dataset = self._read_dataset(self.SIT_DATA_PATH)
        self.sit_dataset.load_faiss_index(index_name="embeddings", file=self.SIT_FAISS_PATH)

        self.mood_dataset = self._read_dataset(self.MOOD_DATA_PATH)
        self.mood_dataset.load_faiss_index(index_name="embeddings", file=self.MOOD_FAISS_PATH)

    def _load_model(self, config: AppConfig):
        self.weather_processor = AutoImageProcessor.from_pretrained(config.model_repo, subfolder=self.WEATHER_SUB)
        self.weather_model = AutoModel.from_pretrained(config.model_repo, subfolder=self.WEATHER_SUB)

        self.sit_processor = AutoImageProcessor.from_pretrained(config.model_repo, subfolder=self.SIT_SUB)
        self.sit_model = AutoModel.from_pretrained(config.model_repo, subfolder=self.SIT_SUB)

        self.mood_processor = AutoImageProcessor.from_pretrained(config.model_repo, subfolder=self.MOOD_SUB)
        self.mood_model = AutoModel.from_pretrained(config.model_repo, subfolder=self.MOOD_SUB)

    def get_weather_playlist_id(self, image_path: str) -> tuple[list[float], list]:
        pil_image = Image.open(image_path)
        scores, retrieved_examples = self._get_similar_images_topk(
            pil_image, self.weather_processor, self.weather_model, self.weather_dataset, k=self.k
        )
        return scores, [retrieved_examples["playlist_id"][i] for i in range(self.k)]

    def get_sit_playlist_id(self, image_path: str) -> tuple[list[float], list]:
        pil_image = Image.open(image_path)
        scores, retrieved_examples = self._get_similar_images_topk(pil_image, self.sit_processor, self.sit_model, self.sit_dataset, k=self.k)
        return scores, [retrieved_examples["playlist_id"][i] for i in range(self.k)]

    def get_mood_playlist_id(self, image_path: str) -> tuple[list[float], list]:
        pil_image = Image.open(image_path)
        scores, retrieved_examples = self._get_similar_images_topk(pil_image, self.mood_processor, self.mood_model, self.mood_dataset, k=self.k)
        return scores, [retrieved_examples["playlist_id"][i] for i in range(self.k)]

    def _get_similar_images_topk(
        self, query_image: Image, processor: ViTImageProcessor, model: ViTModel, dataset: Dataset, k: int
    ) -> tuple[list[float], dict]:
        query_embedding = model(**processor(query_image, return_tensors="pt"))
        query_embedding = query_embedding.last_hidden_state[:, 0].detach().numpy()
        faiss.normalize_L2(query_embedding)
        scores, retrieved_examples = dataset.get_nearest_examples("embeddings", query_embedding.squeeze(), k=k)
        return scores, retrieved_examples
