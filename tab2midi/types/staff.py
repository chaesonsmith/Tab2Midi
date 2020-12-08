from .line import Line

class Staff:
    def __init__(self, sid: int):
        self._id = sid
        self._main_track = []
        self._alt_track = []
        self._times_played = 1
        self._meta = {}

    def add_ledger(self, text: str, alt_track: bool=False):
        if not alt_track:
            self._main_track.append(Line(text))
        else:
            self._alt_track.append(Line(text))

    def id(self) -> int:
        return self._id

    def ledger_count(self) -> int:
        return len(self._main_track) + len(self._alt_track)

    def is_empty(self) -> bool:
        return self.ledger_count() == 0

    def main_track(self) -> [str]:
        return self._main_track

    def alt_track(self) -> [str]:
        return self._alt_track

    def meta_value(self, key: str) -> str:
        if key in self._meta.keys():
            return self._meta[key]

        return "None"
    
    def meta_keys(self) -> [str]:
        return self._meta.keys()

    def set_meta(self, key: str, value: str):
        self._meta[key] = value

    def is_meta_available(self) -> bool:
        return len(self._meta.items()) > 0

    def times_played(self) -> int:
        return self._times_played

    def set_times_played(self, times: int):
        self._times_played = times

