from tab2midi.types import Tab, Staff, Line, MetaData
from tab2midi.tools import utils
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from pathlib import Path
import os

MIDI_TICKS = 480
TICKS_PER_BEAT = { "1" : 1920, "2" : 960, "4" : 480, "8" : 240, "16" : 120, "32" : 60, "64" : 30 }

VALID_NOTES = [ "a", "A", "b", "c", "C", "d", "D", "e", "f", "F", "g", "G"]
BREAK_CHARS = [ ".", "-", "|" ]

def check_end_of_measure(ledgers: [Line], index: int) -> bool:
    for ledger in ledgers:
        if ledger.char(index) != "|": 
            return False

    return True

class MidiWriter:
    def _write_track_header(self, track: MidiTrack, channel: int=0, track_name: str="Midi Track"):
        track.append(MetaMessage("channel_prefix", channel=channel, time=0))
        track.append(MetaMessage("track_name", name=track_name, time=0))
        track.append(MetaMessage("smpte_offset", frame_rate=24, hours=32, minutes=0, seconds=0, 
            frames=0, sub_frames=0, time=0))

    def _write_time_signature(self, track: MidiTrack, signature: str="4/4"):
        tsig = utils.get_time_signature(signature)
        track.append(MetaMessage("time_signature", numerator=tsig[0], denominator=tsig[1], 
            clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))

    def _write_key_signature(self, track: MidiTrack, key: str="C Major"):
        ksig = utils.get_key_signature(key)
        track.append(MetaMessage("key_signature", key=ksig, time=0))

    def _write_end_of_track(self, track: MidiTrack):
        track.append(MetaMessage("end_of_track", time=0))

    def _set_track_tempo(self, track: MidiTrack, bpm: int=120):
        track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm)))

    def _write_note_on(self, track: MidiTrack, channel: int=0, note: int=60, velocity: int=127, time: int=0):#64, time: int=0):
        track.append(Message("note_on", channel=channel, note=note, velocity=velocity, time=time))

    def _write_note_off(self, track: MidiTrack, channel: int=0, note: int=60, velocity: int=64, time: int=0):
        track.append(Message("note_off", channel=channel, note=note, velocity=velocity, time=time))

    def _instrument_change(self, track: MidiTrack, channel: int=0, instrument: int=0, time: int=0):
        track.append(Message("program_change", channel=channel, program=instrument, time=time))

    def _write_midi_track(self, tab: Tab, name: str, midifile: MidiFile, alt_track: bool=False):
        meta, track, time = MetaData(), MidiTrack(), "4/4"

        self._write_track_header(track, channel=int(alt_track), track_name=name)
        self._write_time_signature(track=track)
        self._write_key_signature(track=track)
        self._set_track_tempo(track=track)

        # self._instrument_change(track=track, channel=9, instrument=118)

        for staff in tab.staves():
            print("Start writing of staff id[%d]" % staff.id())
            print("Staff meta information = %s" % staff.meta_keys())
            print("Times staff is played = %d" % staff.times_played())

            if staff.meta_value("tempo") != "None":
                self._set_track_tempo(track=track, bpm=int(staff.meta_value("tempo")))
                print("Found meta value:", staff.meta_value("tempo"))

            if staff.meta_value("time") != "None":
                time = staff.meta_value("time")
                self._write_time_signature(track=track, signature=time)
                print("Found meta value:", staff.meta_value("time"))

            if staff.meta_value("key") != "None":
                self._write_key_signature(track=track, key=staff.meta_value("key"))
                print("Found meta value:", staff.meta_value("key"))

            ledgers = []
            if alt_track:
                ledgers = staff.alt_track()
            else:
                ledgers = staff.main_track()

            start, end = 0, len(ledgers[0].text()) - 1
            measures_count = 0

            for _ in range(1, staff.times_played() + 1):
                for i in range(start, end + 1):
                    if check_end_of_measure(ledgers, i) and i != end:
                        time_sig = utils.get_time_signature(time)
                        time_numerator, time_denominator = time_sig[0], str(time_sig[1])

                        total_time_per_measure = TICKS_PER_BEAT[time_denominator] * time_numerator
                        total_ticks_per_measure = ledgers[0].text()[i + 1:].find("|")
                        tick_time = int(total_time_per_measure / total_ticks_per_measure)
                        
                        meta.set_tick_time(tick_time)
                        measures_count += 1

                        print("measure[%d]: total_time_per_measure = %d, total_ticks_per_measure = %d, tick_time = %d" % \
                            (measures_count, total_time_per_measure, total_ticks_per_measure, tick_time))
                        
                        continue

                    for ledger in ledgers:
                        char = ledger.char(i)
                        octave = ledger.octave()

                        if meta.ledger_active(ledger.name()):
                            if char in BREAK_CHARS:
                                old_char = meta.clear_ledger(ledger.name())
                                delta_time = meta.time_since_last_message()
                                meta.clear_timer()

                                self._write_note_off(track, channel=int(alt_track), 
                                    note=utils.get_note_value(old_char, octave), time=delta_time)

                            elif char in VALID_NOTES:
                                old_char = meta.clear_ledger(ledger.name())
                                meta.activate_note(ledger.name(), char)

                                delta_time = meta.time_since_last_message()
                                meta.clear_timer()

                                self._write_note_off(track, channel=int(alt_track), 
                                    note=utils.get_note_value(old_char, octave), time=delta_time)
                                self._write_note_on(track, channel=int(alt_track), 
                                    note=utils.get_note_value(char, octave), time=0)

                        else:
                            if char in VALID_NOTES:
                                meta.activate_note(ledger.name(), char)
                                delta_time = meta.time_since_last_message()
                                meta.clear_timer()

                                self._write_note_on(track, channel=int(alt_track), 
                                    note=utils.get_note_value(char, octave), time=delta_time)

                    if not check_end_of_measure(ledgers, i):
                        meta.tick() 
                
        self._write_end_of_track(track)
        midifile.tracks.append(track)

    def create_midi(self, tab: Tab, output_folder: Path) -> bool:
        midi_type = tab.midi_type()
        midifile = MidiFile(type=midi_type, ticks_per_beat=MIDI_TICKS)

        if midi_type == 0: 
            self._write_midi_track(tab, name="Main Track", midifile=midifile)
        elif midi_type == 1:
            self._write_midi_track(tab, name="Right Hand Track", midifile=midifile, alt_track=False)
            self._write_midi_track(tab, name="Left Hand Track", midifile=midifile, alt_track=True)

        midi_path = output_folder / tab.file_name().replace(".tab", ".midi")
        midifile.save(midi_path)

        if os.path.exists(midi_path):
            length = utils.get_audio_length(midifile.length)
            print("Created midi file '%s'. Length of midi audio is %s" % (midi_path, length))
            
            return True

        return False
