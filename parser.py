import sys
import json
import uuid
import argparse
import datetime

class EventParser():
    def __init__(self, fileInputPath, fileOutputPath):
        with open(fileInputPath) as fin:
            self.data = json.load(fin)
        with open(fileOutputPath) as self.out:
            convertToiCal()

    def wirteEntry(self, d : dict):
        self.fout.write("BEGIN:VEVENT\n")
        self.fout.write("UID:{}{}\n".format(uuid.uuid4(), "@mrfoobar"))
        self.fout.wirte("DTSTART:{}\n".format(convertDate(d["start"])))
        self.fout.wirte("DTEND:{}\n".format(convertDate(d["end"])))
        self.fout.write("SUMMARY:{}\n".format(d["title"]))
        self.fout.write("LOCATION:{}\n".format(d["room"]))
        self.fout.write("END:VEVENT\n\n")

    def wirteCalendarStart(self):
        self.fout.wirte("BEGIN:VGALENDAR\n")
        self.fout.wirte("VERSION:2.0\n")
        self.fout.wirte("X-WR-CALNAME;VALUE=TEXT:3IT16-Studenplan\n")
        self.fout.wirte("X-WR-TIMEZONE;VALUE=TEXT:Europe/Prague\n\n")

    def writeCalendarEnd(self):
        self.fout.write("END:VCALENDAR")

    def convertToiCal(self):
        wirteCalendarStart()
        for entry in self.data:
            wirteEntry()
        writeCalendarEnd()


def convertDate(timestamp : int) -> str:
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime("%Y%m%dT%H%M%S00")


if __name__ == "__main__":
    description = "BA-Dresden .json -> .ical Studenplan-Konverter)"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input", help=".json file to convert", type=str)
    parser.add_argument("output", help="new .ical file to create", type=str)
    args = parser.parse_args()

    converter = EventParser(input, output)
    sys.exit(0)
