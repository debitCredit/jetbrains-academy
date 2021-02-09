import json
import re
from collections import defaultdict, Counter
import datetime


class EasyRider:

    validation = {
        "bus_id": {"type": int, "required": True, },
        "stop_id": {"type": int, "required": True},
        "stop_name": {"type": str, "required": True,
                      "format": re.compile(r"^([A-Z][a-z]+ )+(Road|Avenue|Boulevard|Street)$")},
        "next_stop": {"type": int, "required": True},
        "stop_type": {"type": "char", "required": False, "format": re.compile(r"[SOF]?$")},
        "a_time": {"type": str, "required": True, "format": re.compile(r"[0-2][0-9]:[0-5][0-9]$")}
    }

    errors = dict.fromkeys(validation, 0)
    bus_lines = {}
    bus_stops = defaultdict(lambda: defaultdict(list))
    bus_stops_cons = dict()
    bus_times_cons = dict()
    bus_times_issues = dict()

    def __init__(self, entry: dict):
        self.entry = entry

    @staticmethod
    def is_field_type_ok(value, type_) -> bool:
        return (
            type(value) is type_
            if type_ != "char"
            else type(value) is str and len(value) == 1
        )

    @staticmethod
    def is_field_format_ok(value, format_: re.Pattern) -> bool:
        return format_.match(value) is not None

    @staticmethod
    def is_field_required(value, required) -> bool:
        return False if required and value == "" else True

    # TODO: PyCharm type hinting returns a warning here due to ambiguity where it's expecting a RE object (Pattern)
    #  but in certain cases None is returned. Need to find an elegant way to handle this.
    def check_fields(self):
        for key, value in self.entry.items():
            format_ = self.validation[key].get("format")
            if format_ and not self.is_field_format_ok(value, format_):
                self.errors[key] += 1

    @classmethod
    def show_format_errors(cls):
        print(f"Format validation: {sum(cls.errors.values())} errors")
        for key, value in cls.errors.items():
            if cls.validation[key].get("format"):
                print(f"{key}: {value}")

    def calc_lines_and_stops(self):
        bus_id = self.entry["bus_id"]

        if bus_id not in self.bus_lines:
            self.bus_lines[bus_id] = 1
        else:
            self.bus_lines[bus_id] += 1

    def calc_lines_stop_types(self):
        bus_id = self.entry["bus_id"]
        stop_type = self.entry["stop_type"]
        stop_name = self.entry["stop_name"]

        if stop_type == "S":
            self.bus_stops[bus_id][stop_type].append(stop_name)
        elif stop_type == "F":
            self.bus_stops[bus_id][stop_type].append(stop_name)
        elif stop_type == "O":
            self.bus_stops[bus_id][stop_type].append(stop_name)
        else:
            self.bus_stops[bus_id][stop_type].append(stop_name)

    def calc_bus_times(self):
        bus_id = self.entry["bus_id"]
        stop_name = self.entry["stop_name"]
        time = self.entry["a_time"]

        self.bus_stops_cons.setdefault(bus_id, [])
        self.bus_stops_cons[bus_id].append(stop_name)

        self.bus_times_cons.setdefault(bus_id, [])
        self.bus_times_cons[bus_id].append(time)

    @classmethod
    def is_issue_with_times(cls):
        print("Arrival time test:")
        error_count = 0
        for key in cls.bus_times_cons.keys():
            previous_time = datetime.datetime.strptime("00:00", '%H:%M')
            for s in cls.bus_stops_cons[key]:
                idx = cls.bus_stops_cons[key].index(s)
                t = cls.bus_times_cons[key][idx]
                if datetime.datetime.strptime(t, '%H:%M') > previous_time:
                    previous_time = datetime.datetime.strptime(t, '%H:%M')
                else:
                    print(f"bus_id line {key}: wrong time on station {cls.bus_stops_cons[key][idx]}")
                    error_count += 1
                    break
        if error_count == 0:
            print("OK")

    @classmethod
    def is_issue_with_stops(cls):
        for b in cls.bus_stops:
            if b is not None and len(cls.bus_stops[b]["S"]) != 1 or len(cls.bus_stops[b]["F"]) != 1:
                print(f"There is no start or end stop for the line: {b}.")

    @classmethod
    def show_stops(cls):
        start_stops = []
        all_stops = []
        finish_stops = []

        for b in cls.bus_stops:
            if b is not None:
                start_stops += cls.bus_stops[b]["S"]
                finish_stops += cls.bus_stops[b]["F"]
                all_stops += cls.bus_stops[b]["S"] + cls.bus_stops[b]["F"] + cls.bus_stops[b][""]

        transfer_stops = [k for k, v in Counter(all_stops).items() if v > 1]

        print(f"Start stops: {len(start_stops)} {sorted(list(set(start_stops)))}")
        print(f"Transfer stops: {len(transfer_stops)} {sorted(list(transfer_stops))}")
        print(f"Finish stops: {len(set(finish_stops))} {sorted(list(set(finish_stops)))}")

    @classmethod
    def show_on_demand_issues(cls):
        start_stops = []
        all_stops = []
        finish_stops = []
        on_demand_stops = []
        check_stops = []
        wrong_stop_type = []

        for b in cls.bus_stops:
            if b is not None:
                start_stops += cls.bus_stops[b]["S"]
                finish_stops += cls.bus_stops[b]["F"]
                on_demand_stops += cls.bus_stops[b]["O"]
                all_stops += cls.bus_stops[b]["S"] + cls.bus_stops[b]["F"] + cls.bus_stops[b][""] \
                    + cls.bus_stops[b]["O"]

        transfer_stops = [k for k, v in Counter(all_stops).items() if v > 1]
        check_stops += transfer_stops + start_stops + finish_stops

        for stop in on_demand_stops:
            if stop in check_stops:
                wrong_stop_type.append(stop)

        wrong_stop_type.sort()

        print("On demand stops test:")
        if len(wrong_stop_type) == 0:
            print("OK")
        else:
            print(f"Wrong stop type: {wrong_stop_type}")

    @classmethod
    def show_lines_and_stops(cls):
        print("Line names and number of stops:")
        for key, value in cls.bus_lines.items():
            print(f"bus_id: {key}, stops: {value}")


def main():
    [EasyRider(entry).calc_lines_stop_types() for entry in json.loads(input())]
    EasyRider.show_on_demand_issues()


if __name__ == "__main__":
    main()
