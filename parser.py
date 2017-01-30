import sys
import json
import uuid
import argparse
import datetime

class EventParser():
    def __init__(self, fileInputPath, fileOutputPath, group: int, subgroup: str):
        with open(fileInputPath) as fin:
            self.data = json.load(fin)
        with open(fileOutputPath, mode='w') as fout:
            self.convertToIcs(fout, group, subgroup)

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

    def convertToIcs(self, fout, group, subgroup):
        # some strings that could be used for filtering
        unwantedGroup = (group % 2) + 1
        filterList = [
            "Gruppe {}".format(unwantedGroup),
            "Gr. {}".format(unwantedGroup),
            "Gr.{}".format(unwantedGroup)]
        if (subgroup != ''):
            unwantedSubgroup = 'A' if (subgroup == 'B') else 'B'
            filterList.append("Gruppe {}{}".format(group, unwantedSubgroup))

        self.writeCalendarStart(fout)
        for entry in self.data:
            title = entry["title"]
            room = entry["room"]

            # filter useless events
            if (title == "PM/EA " or room == "---"):
                continue
            # filter group
            if (group != 0 and containsPatterns(title, filterList)):
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
    parser.add_argument("--group", help="include this group only", type=int,
                        choices=[1,2], default=0)
    parser.add_argument("--subgroup", help="specify subgroup", type=str,
                        choices=['A','B'], default='')
    args = parser.parse_args()

    converter = EventParser(args.input, args.output, args.group, args.subgroup)
    sys.exit(0)
