from .line import Line
from .staff import Staff
import os

class Tab:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._file_name = os.path.basename(os.path.normpath(self._file_path))

        self._meta = { "key" : "C", "time" : "4/4" }
        self._staves = []
        self._multi_track = False

        with open(self._file_path, mode="r") as file:
            self._file_lines = file.readlines()
        
        # Logger.Info("Tab parsed from %s'", self._file_path)
        # Logger.Info("Midi Type = %d", int(self._multi_track))
        # Logger.Info("Number of Meta Variables = %d", len(self._meta))
        # Logger.Info("Meta Variables = %s", str(self._meta))

    def set_meta(self, key: str, value: str):
        self._meta[key] = value

    def meta_value(self, key: str) -> str:
        if key in self._meta.keys():
            return self._meta[key]

        return "None"
        
    def add_staff(self, staff: Staff):
        self._staves.append(staff)

    def set_multi_track(self, multi_track: bool):
        self._multi_track = multi_track

    def file_lines(self) -> [str]:
        return self._file_lines

    def file_name(self) -> str:
        return self._file_name

    def file_path(self) -> str:
        return self._file_path

    def midi_type(self) -> int:
        return int(self._multi_track)

    def staves(self) -> [Staff]:
        return self._staves

    def num_staves(self) -> int:
        return len(self._staves)
        
    def print_tab(self):
        for staff in self._staves:
            staff.print_staff()
