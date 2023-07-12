import cv2
import datasets
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from transformers import AutoImageProcessor, AutoModel
from src.utils import set_seed, fetch_similar_images_topk

set_seed(42)

CKPT_PATH = "./output/weather-11_114800/weather-11_114800_huggingface"
DATASET_PATH = "./output/weather-11_114800/weather_dataset"
FAISS_INDEX_PATH = "./output/weather-11_114800/weather.index"
PLAY_LIST_CSV_PATH = "./input/data/play_list.csv"

st.set_page_config(layout="wide")


def main():
    # Load ckpt, dataset, faiss_index
    processor = AutoImageProcessor.from_pretrained(CKPT_PATH)
    model = AutoModel.from_pretrained(CKPT_PATH)
    dataset = datasets.load_from_disk(DATASET_PATH)
    dataset.load_faiss_index(index_name="embeddings", file=FAISS_INDEX_PATH)

    labels = [label for label in dataset.features.keys() if label not in ["playlist_id", "playlist_img_url", "image", "embeddings"]]

    st.title("image search engine streamlit prototype")
    user_input = st.file_uploader("이미지 파일을 업로드하세요.", type=["jpg", "jpeg", "png"])

    if user_input is not None:
        file_bytes = np.asarray(bytearray(user_input.read()), dtype=np.uint8)
        image_array = cv2.imdecode(file_bytes, 1)
        image = Image.fromarray(image_array)
        similarities, retrieved_examples = fetch_similar_images_topk(image, processor, model, dataset, 5)

        fig = plt.figure(figsize=(20, 10))
        cols = int(5)
        for i in range(len(retrieved_examples["image"])):
            image = retrieved_examples["image"][i]
            id = retrieved_examples["playlist_id"][i]
            tags = [label for label in labels if retrieved_examples[label][i] == 1]
            ax = plt.subplot(int(len(retrieved_examples) / cols), cols, i + 1)
            ax.set_title(f"Similar Image #{i} \n id: {id} \n similarity: {similarities[i]} \n tags: {tags}")
            plt.imshow(np.array(image).astype("int"))
            plt.axis("off")
        st.pyplot(fig)


if __name__ == "__main__":
    main()
