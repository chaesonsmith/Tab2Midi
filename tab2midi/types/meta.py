class MetaData:
    def __init__(self, tick: int=0):
        self._tick_time = tick
        self._time_since_last_message = 0
        self._active_notes = {}

    def set_tick_time(self, tick: int):
        self._tick_time = tick

    def tick(self):
        self._time_since_last_message += self._tick_time

    def clear_timer(self): 
        self._time_since_last_message = 0

    def time_since_last_message(self) -> int:
        return self._time_since_last_message

    def activate_note(self, ledger_name: str, note: str):
        self._active_notes[ledger_name] = note

    def ledger_active(self, name: str) -> bool:
        return name in self._active_notes.keys()

    def clear_ledger(self, name: str) -> str:
        note = self._active_notes[name]
        del self._active_notes[name]

        return note 

    def __str__(self) -> str:
        str_value = "{_tick_time = %d, _time_since_last_message = %d, _active_notes = %s" \
            % (self._tick_time, self._time_since_last_message, str(self._active_notes.values()))
        
        return str_value