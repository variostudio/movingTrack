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


def draw_map_save_html(points, idx):
    base_map = folium.Map(points[idx], zoom_start=15)
    track_layer = folium.FeatureGroup(name='Track')

    base_map.add_child(track_layer)

    folium.PolyLine(points, color='darkorange').add_to(track_layer)

    folium.CircleMarker(location=points[idx], radius=7, color="blue", fill_color='yellow').add_to(track_layer)

    html_file = 'rendered.html'

    base_map.save(html_file)
    return os.path.abspath(html_file)


def read_waypoints(filename):
    pts = []

    result = subprocess.Popen(["exiftool", "-ee", "-n", "-p", "$gpslatitude,$gpslongitude", filename],
                              stdout=subprocess.PIPE)

    for line in io.TextIOWrapper(result.stdout, encoding="utf-8"):
        coord_line = line.strip().split(",")
        pts.append([float(coord_line[0]), float(coord_line[1])])

    pts.pop(0)
    print('Found {} frames'.format(len(pts)))
    return pts


if __name__ == '__main__':
    videoFile = ''
    globalStart = time.time()

    if len(sys.argv) < 2:
        print("Usage: {} input file name".format(sys.argv[0]))
        print("Example: {} test.MP4".format(sys.argv[0]))
        exit(1)
    else:
        videoFile = sys.argv[1]
        print("Processing file: {}".format(videoFile))

    waypoints = read_waypoints(videoFile)

    browser = webdriver.Firefox()

    for index in range(len(waypoints)):
        startProcessing = time.time()
        pngFile = os.path.join('frames', 'frame{}.png'.format(index))
        htmlFile = draw_map_save_html(waypoints, index)
        browser.get('file://{}'.format(htmlFile))
        time.sleep(1)
        browser.save_screenshot(pngFile)
        print('{} - processed in {:.2f} sec'.format(pngFile, (time.time() - startProcessing)))
        os.remove(htmlFile)

    browser.quit()

    print("Processing of {} is finished in {:.2f} sec".format(videoFile, (time.time() - globalStart)))
