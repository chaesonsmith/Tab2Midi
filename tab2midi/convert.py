from tab2midi.tools import TabParser, MidiWriter, utils
from tab2midi.types import Tab
from tab2midi.logger import Logger
from pathlib import Path
import argparse, os, shutil

OUTPUT_FOLDER = Path("./bin")

def clean_output_folder(output_folder: Path=OUTPUT_FOLDER):
    print("Cleaning output folder...")

    for item in os.listdir(output_folder):
        full_path = output_folder / item

        if os.path.isdir(full_path):
            shutil.rmtree(full_path, ignore_errors=True)

        elif os.path.isfile(full_path):
            os.remove(full_path)

def dump_midi_files():
    print("Dumping midi files...")
    utils.dump_midi_files()

def convert_tab(filepath: str): 
    print("Converting file:", filepath)
    parser, writer = TabParser(), MidiWriter()
    tab = parser.parse(filepath)
    writer.create_midi(tab, output_folder=OUTPUT_FOLDER)

def parse_command_arguments():
    parser = argparse.ArgumentParser(prog="Tab2Midi", \
        description="Tab2Midi: Converts tab files into playabale midi files.")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0.0-alpha")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--clean", action="store_true", help="cleans the output folder")
    group.add_argument("-d", "--dump", action="store_true", help="dump all midi files to text")
    group.add_argument("-t", "--tab", dest="tab", metavar="FILE", type=str, \
        help="convert tab into midi file")

    return parser.parse_args()

def main(entry_point: str):
    entry_point = os.path.basename(os.path.normpath(entry_point))
    print("Starting main execution; entry_point =", entry_point)

    args = parse_command_arguments()

    if args.tab:
        convert_tab(filepath=args.tab)

    elif args.dump:
        dump_midi_files()

    elif args.clean:
        clean_output_folder()
               
if __name__ == "__main__":
    main(__file__)