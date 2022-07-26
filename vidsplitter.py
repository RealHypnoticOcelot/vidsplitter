g=0
init = 0
f = open("times.txt","w")
f.close()

mins = int(input("How many minutes will each clip be? Use a whole number: "))
minstoseconds = int(mins) * 60
filename = input("Filename? must be in directory, include extension: ")
def with_moviepy(filename):
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(filename)
    duration       = clip.duration
    return duration

duration = with_moviepy(f"{filename}")
durationint = int(with_moviepy(f"{filename}"))

if duration - int(duration) != 0:
  durationint = durationint + 1 # makes sure if the video isn't an even amount of minutes that it won't cut the clip

minsinvid = durationint/60
if minsinvid - int(minsinvid) != 0:
  minsinvid = int(minsinvid) + 1 # if the minutes in the video isn't whole, add 1 so it doesn't cut
print(minsinvid)

if minsinvid % mins != 0:
  minsinvid = minsinvid - (minsinvid % mins)
  minsinvid = int((minsinvid/mins) + 1)
  print(minsinvid)

while g != minsinvid: #set to amount of minutes in the video
    a = init
    init = init + minstoseconds #interval to split into
    values = f"{a}-{init}"
    g = g+1
    f = open("times.txt", "a")
    f.write(f"{values}\n")
    f.close()

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
required_video_file = f"{filename}"
with open("times.txt") as f:
  times = f.readlines()
times = [x.strip() for x in times] 
for time in times:
  starttime = int(time.split("-")[0])
  endtime = int(time.split("-")[1])
  ffmpeg_extract_subclip(required_video_file, starttime, endtime, targetname=str(times.index(time)+1)+".mp4")