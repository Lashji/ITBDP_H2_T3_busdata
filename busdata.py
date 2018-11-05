import urllib.request
import json
import sys
import time
import csv


def checkTime(p_time, used_time):
    return used_time < p_time


def clean_data(data):
    tmp = []
    for d in data["body"]:
        tmp.append({
            "Date": d["monitoredVehicleJourney"]["framedVehicleJourneyRef"]["dateFrameRef"],
            "Time": d["recordedAtTime"],
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
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for d in data:
            writer.writerow(d)


def main():
    filename = sys.argv[1]
    sleep_t = int(sys.argv[2])
    p_time = float(sys.argv[3])
    p_on = True
    used_time = time.process_time()
    data = []

    while p_on:
        used_time += time.process_time()
        data += data_req()
        time.sleep(sleep_t)
        p_on = checkTime(p_time, used_time)

    save_data(data, filename)


main()
