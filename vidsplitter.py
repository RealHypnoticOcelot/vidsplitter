from moviepy.editor import *
g=0
init = 0
f = open("times.txt","w")
f.close()

mins = input("How many minutes/seconds will each clip be? Use a whole number, followed by the initial of the unit: ")
if "m" in mins:
  mins = int(mins.replace("m", ""))
  minstoseconds = int(mins) * 60
  seconds = 0
elif "s" in mins:
  mins = int(mins.replace("s", ""))
  minstoseconds = int(mins)
  mins = float(mins / 60)
  seconds = 1
filename = input("Filename? must be in directory, include extension: ")
if ".mkv" in filename:
  filename2 = filename.replace(".mkv", "")
  if os.path.exists(f"converted_{filename2}.mp4"): #if the no sound version already exists
    print(f"\n\"converted_{filename2}.mp4\" already exists, skipping conversion")
    filename = f"converted_{filename2}.mp4"
  else:
    print("\nConverting mkv to mp4!")
    convert = VideoFileClip(filename)
    convert.write_videofile(f"converted_{filename2}.mp4", codec="libx264",audio_codec="aac")
    filename = f"converted_{filename2}.mp4"


def with_moviepy(filename):
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(filename)
    duration       = clip.duration
    return duration

duration = with_moviepy(f"{filename}")
durationint = int(with_moviepy(f"{filename}"))

if duration - int(duration) != 0:
  durationint = durationint + 1 # makes sure if the video isn't an even amount of minutes that it won't cut the clip

if seconds == 0:
  minsinvid = durationint/60
  if minsinvid - int(minsinvid) != 0:
    minsinvid = int(minsinvid) + 1 # if the minutes in the video isn't whole, add 1 so it doesn't cut
elif seconds == 1:
  minsinvid = durationint/minstoseconds
  if minsinvid - int(minsinvid) != 0:
    minsinvid = int(minsinvid) + 1 # if the minutes in the video isn't whole, add 1 so it doesn't cut

if minsinvid % mins != 0: # if the video duration isn't a whole number
  minsinvid = minsinvid - (minsinvid % mins)
  minsinvid = int((minsinvid/mins) + 1)

while g != minsinvid: #set to amount of minutes in the video
    a = init
    init = init + minstoseconds #interval to split into
    values = f"{a}-{init}"
    g = g+1
    f = open("times.txt", "a")
    f.write(f"{values}\n")
    f.close()

required_video_file = VideoFileClip(filename)
with open("times.txt") as f:
  times = f.readlines()
times = [x.strip() for x in times] 
fullduration = required_video_file.duration
for time in times:
  starttime = int(time.split("-")[0])
  endtime = int(time.split("-")[1])
  if starttime >= fullduration:
    print(f"Video too short to complete request! Quitting loop..")
    break
  if endtime >= fullduration:
    print(f"Cropping endtime from {endtime} to {fullduration}!")
    endtime = None
  subclip = required_video_file.subclip(starttime, endtime)
  filen = str(times.index(time)+1)+".mp4"
  subclip.write_videofile(filen, audio_codec='aac')