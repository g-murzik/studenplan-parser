import sys
import json
import uuid
import argparse
import datetime

class EventParser():
    def __init__(self, fileInputPath, fileOutputPath, excludeGroup):
        with open(fileInputPath) as fin:
            self.data = json.load(fin)
        with open(fileOutputPath, mode='x') as fout:
            self.convertToIcs(fout, excludeGroup)

    def writeEntry(self, d : dict, fout):
        fout.write("BEGIN:VEVENT\n")
        fout.write("UID:{}{}\n".format(uuid.uuid4(), "@mrfoobar"))
        fout.write("DTSTART:{}\n".format(convertDate(d["start"])))
        fout.write("DTEND:{}\n".format(convertDate(d["end"])))
        fout.write("SUMMARY:{}\n".format(d["title"]))
        fout.write("LOCATION:{}\n".format(d["room"]))
        fout.write("END:VEVENT\n\n")

    def writeCalendarStart(self, fout):
        fout.write("BEGIN:VCALENDAR\n")
        fout.write("VERSION:2.0\n")
        fout.write("X-WR-CALNAME;VALUE=TEXT:3IT16-Studenplan\n")
        fout.write("X-WR-TIMEZONE;VALUE=TEXT:Europe/Prague\n\n")

    def writeCalendarEnd(self, fout):
        fout.write("END:VCALENDAR")

    def convertToIcs(self, fout, excludeGroup):
        # some strings that could be used for filtering
        filterList = [
            "Gruppe {}".format(excludeGroup),
            "Gr. {}".format(excludeGroup),
            "Gr.{}".format(excludeGroup)]

        self.writeCalendarStart(fout)
        for entry in self.data:
            title = entry["title"]
            room = entry["room"]

            # filter useless events
            if (title == "PM/EA " or room == "---"):
                continue
            # filter group
            if (excludeGroup != 0 and containsPatterns(title, filterList)):
                continue
            self.writeEntry(entry, fout)
        self.writeCalendarEnd(fout)


def convertDate(timestamp : int) -> str:
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime("%Y%m%dT%H%M%S")

def containsPatterns(string : str, patterns : list):
    for pattern in patterns:
        if (pattern in string):
            return True
    return False


if __name__ == "__main__":
    description = "BA-Dresden .json -> .ical Studenplan-Konverter)"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input", help=".json file to convert", type=str)
    parser.add_argument("output", help="new .ics file to create", type=str)
    parser.add_argument("--exclude-group", help="group to exclude", type=int,
                        choices=[1,2], default=0)
    args = parser.parse_args()

    converter = EventParser(args.input, args.output, args.exclude_group)
    sys.exit(0)
