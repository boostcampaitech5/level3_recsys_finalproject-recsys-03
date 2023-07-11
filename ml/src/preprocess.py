import re
import os
import pandas as pd
from typing import List
from .utils import tag_uniques, read_data, get_ocr_result, get_editors_choice, get_empty_img


def generate_df(df: pd.DataFrame, tag_type: str) -> pd.DataFrame:
    tag_col = f"tag_{tag_type}"
    tag_list = tag_uniques(df[tag_col])
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
    ocr_result = get_ocr_result(df)
    editors_choice = get_editors_choice(ocr_result)
    empty_imgs = get_empty_img(df)

    tagless = list(df[df.tag_cnt == 0].index)

    del_list = list(set(editors_choice + empty_imgs + tagless))
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
