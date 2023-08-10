# The Script for getting animated track based on GoPro video
## Please make sure your GoPro GPS sensor is ON before recording video

## To run this script:
### 1. Install https://exiftool.org/
### 2. Required Pyton modules: 
#### Folium 
#### Selenium

## Usage of output
### The output of this script is 1 FPS image sequence. Use you favourite video editing software to convert the sequence into video file
### Alternatively use FFMPEG to conver image sequence into video:
```ffmpeg -framerate 1 -i output\frame%04d.png -c:v libx264 -pix_fmt yuv420p track.mp4``` 