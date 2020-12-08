from mido import MidiFile
from pathlib import Path
import os, shutil, math

NOTE_VALUES = { "a0": 21, "A0": 22, "b0": 23, "B0": 24,
    "c1": 24, "C1": 25, "d1": 26, "D1": 27, "e1": 28, "E1": 29, "f1": 29, "F1": 30, "g1": 31, "G1": 32, "a1": 33, "A1": 34, "b1": 35, "B1": 36, 
    "c2": 36, "C2": 37, "d2": 38, "D2": 39, "e2": 40, "E2": 41, "f2": 41, "F2": 42, "g2": 43, "G2": 44, "a2": 45, "A2": 46, "b2": 47, "B2": 48,
    "c3": 48, "C3": 49, "d3": 50, "D3": 51, "e3": 52, "E3": 53, "f3": 53, "F3": 54, "g3": 55, "G3": 56, "a3": 57, "A3": 58, "b3": 59, "B3": 60,
    "c4": 60, "C4": 61, "d4": 62, "D4": 63, "e4": 64, "E4": 65, "f4": 65, "F4": 66, "g4": 67, "G4": 68, "a4": 69, "A4": 70, "b4": 71, "B4": 72,
    "c5": 72, "C5": 73, "d5": 74, "D5": 75, "e5": 76, "E5": 77, "f5": 77, "F5": 78, "g5": 79, "G5": 80, "a5": 81, "A5": 82, "b5": 83, "B5": 84,
    "c6": 84, "C6": 85, "d6": 86, "D6": 87, "e6": 88, "E6": 89, "f6": 89, "F6": 90, "g6": 91, "G6": 92, "a6": 93, "A6": 94, "b6": 95, "B6": 96,
    "c7": 96, "C7": 97, "d7": 98, "D7": 99, "e7": 100, "E7": 101, "f7": 101, "F7": 102, "g7": 103, "G7": 104, "a7": 105, "A7": 106, "b7": 107, "B7": 108,
    "c8": 108 
    }

def get_audio_length(seconds: int) -> str:
    mins = math.floor(seconds / 60)
    secs = seconds % 60

    return "%d:%02d" % (mins, secs)

def get_note_value(note: str, octave: str) -> str:
    return NOTE_VALUES[note + octave] 

def get_key_signature(key: str) -> str:
    k, m = key.split(" ")
    
    if m.lower() == "minor":
        return k + "m"
    else:
        return k        

def get_time_signature(time: str) -> [int]:
    nom, denom = time.split("/")
    return [int(nom), int(denom)]

def dump_midi_files():
    bin_folder = Path("./bin")
    dump_folder = Path(bin_folder / "midi_dumps")
    
    midi_files = []

    if dump_folder.exists():
        shutil.rmtree(dump_folder)

    for file in os.listdir(bin_folder):
        if ".mid" in file:
            midi_files.append(file)

    if len(midi_files) > 0: 
        dump_folder.mkdir(exist_ok=True)

        for file in midi_files:
            print("%s -> %s" % (bin_folder / file, dump_folder / file.replace(".midi", ".txt")))

            midi = MidiFile(bin_folder / file)
            outfile = open(dump_folder / file.replace(".midi", ".txt"), mode="w+")

            midi_attrs = vars(midi)
            outfile.write((", ".join("%s: %s" % item for item in midi_attrs.items())) + '\n')

            for i, track in enumerate(midi.tracks):
                outfile.write("Track {}: {}\n".format(i, track.name))
                
                for msg in track:
                    if not msg.is_meta:
                        outfile.write('\t')

                    outfile.write(str(msg) + '\n')
            
            outfile.close()
    else:
        print("No midi files found in '%s'" % bin_folder)
