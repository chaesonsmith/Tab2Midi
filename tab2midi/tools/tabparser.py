from tab2midi.types import Tab, Staff
import re

PATTERNS = { 
    "ledger_line" : "(?<=\\b)(R|L)?[0-8][a-gA-G>.|-]*(x[0-9]+)?(?=\\n)",
    "meta" : "\\[(([0-9]+(bpm|BPM)?)|([0-9]+\\/[0-9]+)|([a-gA-G]((b|#)?) ((M|m)(inor|ajor))))\\]",
    "tempo_meta" : "\\[[0-9]+(bpm|BPM)?\\]",
    "time_meta" : "\\[[0-9]+\\/[0-9]+\\]",
    "key_meta" : "\\[[a-gA-G]((b|#)?) ((M|m)(inor|ajor))\\]",
    "alt_track" : "(?<=\\b)L[0-8=]\\|",
    "main_track" : "(?<=\\b)R[0-8=]\\|",
    "staff_repeat" : "(?<=\\|x)[1-9]+",
}

class TabParser:
    def parse(self, file_path: str) -> Tab:
        tab = Tab(file_path=file_path)

        # change way of settings midi type / multi track
        file_dump = "\n".join(tab.file_lines())
        tab.set_multi_track(re.search(PATTERNS["alt_track"], file_dump) != None)

        ledger_pattern = re.compile(PATTERNS["ledger_line"])
        meta_pattern = re.compile(PATTERNS["meta"])
        tempo_pattern = re.compile(PATTERNS["tempo_meta"])
        time_pattern = re.compile(PATTERNS["time_meta"])
        key_pattern = re.compile(PATTERNS["key_meta"])

        staff = None

        for line in tab.file_lines():
            line_match = ledger_pattern.match(line)
            meta_match = meta_pattern.match(line)

            if line_match:
                if not staff:
                    staff = Staff(tab.num_staves())
                    print("Created a new staff, total count:", tab.num_staves())

                ledger = line_match.group()
                repeat = re.search(PATTERNS["staff_repeat"], ledger)
                
                if repeat:
                    staff.set_times_played(int(repeat.group()))
                    ledger = ledger.replace("x" + repeat.group(), "")

                is_alt_track = re.match(PATTERNS["alt_track"], ledger) != None
                staff.add_ledger(ledger, alt_track=is_alt_track)

                if is_alt_track:
                    print("Added ledger; alt_track; ledger count:", staff.ledger_count())
                else:
                    print("Added ledger; main_track; ledger count:", staff.ledger_count())

            elif meta_match:
                if not staff:
                    staff = Staff(tab.num_staves())
                    print("Created a new staff, total count:", tab.num_staves())

                meta_tempo_match = tempo_pattern.search(line)
                if meta_tempo_match:
                    actual_tempo = re.search("[0-9]+", meta_tempo_match.group()).group()
                    staff.set_meta(key="tempo", value=actual_tempo)
                    print(">>>" + meta_tempo_match.group(), actual_tempo)

                meta_time_match = time_pattern.search(line)
                if meta_time_match:
                    actual_time = meta_time_match.group()[1:-1]
                    staff.set_meta(key="time", value=actual_time)
                    print(">>>" + meta_time_match.group(), actual_time)
                
                meta_key_match = key_pattern.search(line)
                if meta_key_match:
                    actual_key = meta_key_match.group()[1:-1]
                    staff.set_meta(key="key", value=actual_key)
                    print(">>>" + meta_key_match.group(), actual_key)
                
            
            elif line.strip() == "": 
                if staff and not staff.is_empty():
                    tab.add_staff(staff)
                    staff = None

                    print("Added staff, current count: ", tab.num_staves())
        
        if staff and not staff.is_empty():
            tab.add_staff(staff)
            staff = None

            print("Added staff, current count: ", tab.num_staves())

        print("Finished parsing file:", file_path)
        return tab
            