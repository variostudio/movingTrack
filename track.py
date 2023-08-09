# The Script for getting animated track based on GoPro video
# Please make sure your GoPro GPS sensor is ON before recording video
# Author: Dmytro P aka VarioStudio


import subprocess
import io
import folium
from selenium import webdriver
import time
import os
import sys


def draw_save_map(points, idx):
    base_map = folium.Map(points[idx], zoom_start=15)
    track_layer = folium.FeatureGroup(name='Track')

    base_map.add_child(track_layer)

    folium.PolyLine(points, color='darkorange').add_to(track_layer)

    folium.Marker(location=points[idx], icon=folium.Icon(icon="asterisk", color="blue")).add_to(track_layer)

    html_file = os.path.join('htmls', 'frame' + str(idx) + '.html')

    base_map.save(html_file)
    return os.path.abspath(html_file)


if __name__ == '__main__':
    videoFile = ''

    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " input file name")
        exit(1)
    else:
        videoFile = sys.argv[1]
        print("Processing file: " + videoFile)

    waypoints = []

    result = subprocess.Popen(["exiftool", "-ee", "-n", "-p", "$gpslatitude,$gpslongitude", videoFile],
                              stdout=subprocess.PIPE)
    for line in io.TextIOWrapper(result.stdout, encoding="utf-8"):
        coord_line = line.strip().split(",")
        waypoints.append([float(coord_line[0]), float(coord_line[1])])

    waypoints.pop(0)
    print('Found ' + str(len(waypoints)) + ' frames')

    index = 0
    browser = webdriver.Firefox()

    for x in waypoints:
        pngFile = 'frame' + str(index) + '.png'
        htmlFile = draw_save_map(waypoints, index)
        browser.get('file://' + htmlFile)
        time.sleep(1)
        finalFile = os.path.join('screens', pngFile)
        browser.save_screenshot(finalFile)
        index = index + 1
        print(finalFile + ' - saved')

    browser.quit()

    print("Done")
