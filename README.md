# Tab2Midi

Tab2Midi converts a piano tab file into a playable audio MIDI file.

## Getting Started

These instructions will help you get Tab2Midi running on your local system.

### Prerequisites

The prerequsites of Tab2Midi are located in a pip requirements file. Use the command below to install everything needed at once

```text
pip install -r requirements.txt
```

### Installing

A step by step guide of installing Tab2Midi onto your local system

```text
TBD
```

## Running

Example running on a Windows/OS X/Linux system from the root directory of tab2midi-master

```text
python -m tab2midi -t path/to/tab_file.tab
python -m tab2midi --tab ../other/path/to/tab_file.tab
```

For additional information - use either of the following commands

```text
python -m tab2midi -h
python -m tab2midi --help
```

## Built With

* [Mido](https://github.com/mido/mido/blob/stable/docs/index.rst) - MIDI Objects for Python

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Chaeson B Smith** - *Initial work* - [GitHub](https://github.com/chaesonsmith)

See also the list of [contributors](https://github.com/csmith446/tab2midi/contributors) who participated in this project.

## License

```text
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

To view a copy of the GNU General Public License - see the [LICENSE](LICENSE) file.

## Acknowledgments

* [TabNabber](https://tabnabber.com/)
  * General idea for the Tab2Midi project
  * Helped in initial debugging of MIDI file creation
  * Piano tab syntax used as a baseline for the [Tablature Language Syntax](https://github.com/chaesonsmith/tablature-language-syntax)
* [Mido](https://github.com/mido/mido/blob/stable/docs/index.rst) - MIDI Objects for Python
  * Documenation helped to understand MIDI files and how messages are written
  * Library extensively used in MIDI file creation in Tab2Midi
