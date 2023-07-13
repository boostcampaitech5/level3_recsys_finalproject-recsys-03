import bentoml
from bentoml.io import Multipart, JSON
from PIL.Image import Image

from dto.RecommendMusicRequest import RecommendMusicRequest
from dto.RecommendMusicResponse import RecommendMusicResponse, RecommendMusic

svc = bentoml.Service("name", runners=[])


@svc.api(
    input=Multipart(image=bentoml.io.Image(), data=JSON(pydantic_model=RecommendMusicRequest)), output=JSON(pydantic_model=RecommendMusicResponse)
)
def recommendMusic(image: Image, data: RecommendMusicRequest) -> dict[str,]:
    songs = [
        RecommendMusic(song_id=1, youtube_id="XHMdIA6bEOE", song_title="짱구는 못말려 오프닝1", artist_name="아이브", album_title="짱구 1기"),
        RecommendMusic(
            song_id=2,
            youtube_id="Sq_mS6xWpvk",
            song_title="Kiss Goodnightrrrrrrrrrr",
            artist_name="I Dont Know How But They Found Meeeee",
            album_title="Razzmatazz",
        ),
        RecommendMusic(
            song_id=3,
            youtube_id="A1tZgPAcpjE",
            song_title="사랑하긴 했었나요 스쳐가는 인연이었나요 짧지않은 우리 함께했던 시간들이 자꾸 내 마음을 가둬두네",
            artist_name="잔나비 잔나비 잔미잔미 잔나비 잔나비 잔미잔미",
            album_title="봉춤을 추네",
        ),
        RecommendMusic(song_id=4, youtube_id="NbKH4iZqq1Y", song_title="Drowning", artist_name="WOODZ", album_title="OO-LI"),
        RecommendMusic(song_id=5, youtube_id="2Kff0U8w-aU", song_title="OMG", artist_name="NewJeans", album_title="NewJeans 'OMG'"),
        RecommendMusic(song_id=6, youtube_id="j1uXcHwLhHM", song_title="사건의 지평선", artist_name="윤하", album_title="END THEORY : Final Edition"),
    ]

    return RecommendMusicResponse(songs=songs)
