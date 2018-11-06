import urllib.request
import json
import sys
import time
import csv


def check_time(p_time, used_time):
    return used_time < p_time


def get_time_in_hours(t):
    return t[11:19]


def clean_data(data):
    tmp = []
    for d in data["body"]:
        tmp.append({
            "Date": d["monitoredVehicleJourney"]["framedVehicleJourneyRef"]["dateFrameRef"],
            "Time": get_time_in_hours(d["recordedAtTime"]),
            "Line": d["monitoredVehicleJourney"]["lineRef"],
            "Direction": d["monitoredVehicleJourney"]["directionRef"],
            "Latitude": d["monitoredVehicleJourney"]['vehicleLocation']['latitude'],
            "Longitude": d["monitoredVehicleJourney"]['vehicleLocation']['longitude'],
            "Speed": d["monitoredVehicleJourney"]["speed"]
        })

    return tmp


def data_req():
    tmp = []
    req = urllib.request.urlopen(
        "http://data.itsfactory.fi/journeys/api/1/vehicle-activity")
    data = json.loads(req.read())
    tmp = clean_data(data)
    return tmp


def save_data(data, filename):
    with open(filename, mode="w") as csv_file:
        fieldnames = ["Date", "Time", "Line",
                      "Direction", "Latitude", "Longitude", "Speed"]
        writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=fieldnames)
        writer.writeheader()

        for d in data:
            writer.writerow(d)


def main():
    filename = sys.argv[1]
    sleep_t = int(sys.argv[2])
    p_time = float(sys.argv[3])
    p_on = True
    t = time.process_time()
    data = []

    while p_on:
        data += data_req()
        time.sleep(sleep_t)
        t += time.process_time() + sleep_t
        p_on = check_time(p_time, t)

    save_data(data, filename)


main()
