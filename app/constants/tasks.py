import queue

from app.api.schemas.beatmaps import BeatmapRead
from app.interaction import Beatmap

beatmap_tasks: queue.Queue[tuple[str, str]] = queue.Queue()
beatmap_results: dict[str, queue.Queue[BeatmapRead]] = {}


def is_empty_queue(dict_queue: dict, ident: str):
    return dict_queue[ident] is not None and not dict_queue[ident].empty()


def schedule_fetch_beatmaps():
    while True:
        (client_id, ident) = beatmap_tasks.get(True)
        if beatmap_results[client_id] is None:
            beatmap_results[client_id] = queue.Queue()
        beatmap_results[client_id].put(BeatmapRead.from_orm(await Beatmap.request_api(ident)))

