import re
import os
import cv2
import requests
import numpy as np
import pandas as pd
from typing import List
from skimage.metrics import structural_similarity as ssim
from .utils import tag_uniques, read_data, read_image, get_ocr_result, get_editors_choice, get_empty_img


def temp1_mask(image):
    x, width = 210, 320
    y, height = 135, 320
    gray = 127

    mask = np.full((height, width), gray, dtype=np.int32)
    image[y : y + height, x : x + width] = mask
    return image


def temp2_mask(image):
    x, width = 192, 337
    y, height = 72, 337
    gray = 127

    _x, _width = 147, 440
    _y, _height = 464, 120
    _gray = image[0, 0]

    mask = np.full((height, width), gray, dtype=np.int32)
    name_mask = np.full((_height, _width), _gray, dtype=np.int32)

    image[y : y + height, x : x + width] = mask
    image[_y : _y + _height, _x : _x + _width] = name_mask
    return image


def temp3_mask(image):
    x, width = 99, 403
    y, height = 99, 403
    outer_gray = 202

    _x, _width = 140, 320
    _y, _height = 140, 320
    inner_gray = 132

    outer_mask = np.full((height, width), outer_gray, dtype=np.int32)
    inner_mask = np.full((_height, _width), inner_gray, dtype=np.int32)

    image[y : y + height, x : x + width] = outer_mask
    image[_y : _y + _height, _x : _x + _width] = inner_mask
    return image


def cal_ssim(temp, image, mask_type):
    temp_shape = temp.shape
    resized_image = cv2.resize(image, temp_shape)

    if mask_type == "temp_1":
        adjusted_image = temp1_mask(resized_image.copy())
    elif mask_type == "temp_2":
        adjusted_image = temp2_mask(resized_image.copy())
    elif mask_type == "temp_3":
        adjusted_image = temp3_mask(resized_image.copy())
    else:
        raise Exception(f"wrong mask_type! - {mask_type}")

    (score, diff) = ssim(temp, adjusted_image, full=True)
    return score


def check_img_temp(url: str, temp_dir: str):
    TEMP_PATH = temp_dir

    temp1_img = cv2.imread(os.path.join(TEMP_PATH, "template_1.jpg"))
    temp1_gray = cv2.cvtColor(temp1_img, cv2.COLOR_BGR2GRAY)

    temp2_img = cv2.imread(os.path.join(TEMP_PATH, "template_2.jpg"))
    temp2_gray = cv2.cvtColor(temp2_img, cv2.COLOR_BGR2GRAY)

    temp3_img = cv2.imread(os.path.join(TEMP_PATH, "template_3.jpg"))
    temp3_gray = cv2.cvtColor(temp3_img, cv2.COLOR_BGR2GRAY)

    image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
    image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    temp1_sim_score = cal_ssim(temp1_gray, image_gray, "temp_1")
    temp2_sim_score = cal_ssim(temp2_gray, image_gray, "temp_2")
    temp3_sim_score = cal_ssim(temp3_gray, image_gray, "temp_3")

    temp1_sim_threshold = 0.905
    temp2_sim_threshold = 0.915
    temp3_sim_threshold = 0.998

    raw_image = read_image(url)
    if temp1_sim_score >= temp1_sim_threshold:
        return raw_image.crop((215, 138, 527, 452)).resize((600, 600))
    if temp2_sim_score >= temp2_sim_threshold:
        return raw_image.crop((192, 72, 526, 407)).resize((600, 600))
    if temp3_sim_score >= temp3_sim_threshold:
        return raw_image.crop((142, 141, 457, 456)).resize((600, 600))

    return raw_image


def generate_df(df: pd.DataFrame, tag_type: str) -> pd.DataFrame:
    tag_col = f"tag_{tag_type}"

    if tag_type == "weather":
        tag_list = ['봄', '여름', '가을', '겨울', '우중충한날']
    if tag_type == "mood":
        tag_list = ['힘찬', '몽환적인', '밝은', '슬픔', '우울/외로움', '편안한', '사랑']
    if tag_type == "sit":
        tag_list = ['집중', '여유', '밤', '오후', '저녁', '기분전환', '산책', '운동']
    
    col_list = [tag_type[0] + str(i) for i in range(len(tag_list))]

    for tag, col in zip(tag_list, col_list):
        df[col] = df.apply(lambda x: 1 if tag in x[tag_col] else 0, axis=1)

    cols = ["playlist_id", "playlist_img_url"] + col_list
    result = df[df[f"tag_{tag_type}_cnt"] > 0][cols]
    return result


def preprocess_data(data_dir: str, train_file: str, tag_file: str) -> pd.DataFrame:
    train_path = os.path.join(data_dir, train_file)
    tag_path = os.path.join(data_dir, tag_file)

    df = read_data(train_path)

    new_tags = pd.read_csv(tag_path)

    refine_text(df, ["playlist_title", "playlist_subtitle"])
    count_songs(df)
    df = extract_tags(df, new_tags)

    df = remove_abnormal_img(df)
    del_list = get_del_list(df)
    df = del_rows(df, del_list)

    return df


def refine_text(df: pd.DataFrame, columns: list) -> None:
    for col in columns:
        df[col] = df[col].apply(lambda x: re.sub(r"[^\w\s]+", "", x))


def count_songs(df: pd.DataFrame) -> None:
    df["num_of_songs"] = df["playlist_songs"].apply(lambda x: len(x))


def extract_tags(df: pd.DataFrame, new_tags: pd.DataFrame) -> pd.DataFrame:
    df["new_tags"] = None
    old_tag = list(new_tags["old"])

    for i, tag_list in enumerate(df.playlist_tags):
        new = []
        for tag in tag_list:
            if tag in old_tag:
                new.append(new_tags.loc[new_tags.old == tag]["new"].values[0])
        df.new_tags[i] = list(set(new))

    for tag in new_tags.type.unique():
        tags = set(new_tags[new_tags.type == tag].new)
        df[f"tag_{tag}"] = df["new_tags"].apply(lambda x: list(set(x) & tags))
        df[f"tag_{tag}_cnt"] = df[f"tag_{tag}"].apply(lambda x: len(x))

    df["tag_cnt"] = df.tag_mood_cnt + df.tag_sit_cnt + df.tag_weather_cnt
    df = df.loc[df.tag_cnt > 0,]
    df = df.reset_index(drop=True)
    return df


def del_rows(df: pd.DataFrame, del_list: List[int]) -> pd.DataFrame:
    dropped_df = df.drop(index=del_list)
    dropped_df = dropped_df.reset_index(drop=True)
    return dropped_df


def get_del_list(df: pd.DataFrame) -> List[int]:
    empty_imgs = get_empty_img(df)

    tagless = list(df[df.tag_cnt == 0].index)

    del_list = list(set(empty_imgs + tagless))
    return del_list


def remove_abnormal_img(df: pd.DataFrame) -> pd.DataFrame:
    abnormal_tags = [
        "The Artist",
        "오늘의 아티스트 추천",
        "시대별음악",
        "스타DJ",
        "스타플레이리스트",
        "케이팝 탐사대",
        "핑크퐁",
        "캉골",
        "화요일",
        "태교음악",
        "태교동요",
        "키르시",
        "키치포크",
        "클로티",
        "클럽매니아",
        "크리틱",
        "커버낫",
        "추천음악",
        "추석",
        "최신음악",
        "이스트쿤스트",
        "이벳필드",
        "오아이오아이",
        "예스아이씨",
        "에노우",
        "비바스튜디오",
        "브라운브레스",
        "밀레클래식",
        "마하그리드",
        "마크곤잘레스",
        "라이프아카이브",
        "네이키드니스",
        "최신 아이돌",
        "차트",
        "진희네 플리쌀롱",
        "지니뮤직어워드",
        "중국음악",
        "자장가동요",
        "자장가",
        "인기만화",
        "인기동요",
        "미스트롯",
        "미스터트롯",
        "월요일",
        "오아추",
        "예능",
        "어린이동요",
        "배철수의 음악캠프",
        "스텔라장",
        "김이나 별이 빛나는 밤에",
        "김김박김",
        "넷플릭스",
        "심음감",
        "심야지기",
        "시네뮤직",
        "스톤뮤직",
        "수요일",
        "00's 트랜드 뮤직",
        "2022GMA",
        "80's 트랜드 뮤직",
        "광-희의 재즈 전파사",
        "90's 트랜드 뮤직",
        "CCM",
        "CF",
        "COLORS",
        "DJ 157",
        "DJ PICK",
        "DJ 감또",
        "DJ 냥사원",
        "DJ 노찌",
        "DJ 달",
        "DJ 란나",
        "DJ 모니",
        "DJ 뮤",
        "DJ 베가스",
        "TV속 음악",
        "YALE",
        "weekly choice",
        "가까워진 인디씬",
        "DJ 알잘딱깔센",
        "DJ 클매",
        "DJ 힐러",
        "고음질",
        "국외CCM",
        "금요일",
        "나만 모르는 노래",
        "노래방",
        "당신의BGM",
        "대세는 클럽뮤직",
        "류태형의 예술의 잔당",
        "댄스음악 열풍",
        "동요",
        "드라마",
        "등산",
        "디깅 업",
        "디즈니",
        "록 전성시대",
        "류태형의 예술의 잔당",
        "만화주제가",
        "모던록의 시대",
        "목요일",
        "뮤지컬",
        "뮤직아일랜드",
        "뮤직트래블",
        "방송",
    ]

    df["remove"] = None

    for i, tag in enumerate(df.playlist_tags):
        if len(set(tag) & set(abnormal_tags)) > 0:
            df["remove"][i] = True
        else:
            df["remove"][i] = False
    df = df[df.remove == False]
    return df
