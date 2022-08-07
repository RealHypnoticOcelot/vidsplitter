from moviepy.editor import *
g=0
init = 0
f = open("times.txt","w") # clear the times.txt file
f.close()

mins = input("How many minutes/seconds will each clip be? Use a whole number, followed by the initial of the unit: ")
if "m" in mins: # if it's in minutes
  mins = int(mins.replace("m", "")) # remove the m
  minstoseconds = int(mins) * 60 # convert minutes to seconds
  seconds = 0
elif "s" in mins: # if it's in seconds
  mins = int(mins.replace("s", "")) # remove the s
  minstoseconds = int(mins) # "convert" mins to seconds
  mins = float(mins / 60) #float because it could be a decimal
  seconds = 1 # enables "seconds mode"
else:
  print("Invalid input! Quitting...")
  quit()
filename = input("Filename? must be in directory, include extension: ")
if ".mkv" in filename: # if the file is an mkv, re-encode it to mp4
  filename2 = filename.replace(".mkv", "")
  if os.path.exists(f"converted_{filename2}.mp4"): #if the converted version already exists
    print(f"\n\"converted_{filename2}.mp4\" already exists, skipping conversion")
    filename = f"converted_{filename2}.mp4"
  else:
    print("\nConverting mkv to mp4!")
    convert = VideoFileClip(filename)
    convert.write_videofile(f"converted_{filename2}.mp4", codec="libx264",audio_codec="aac")
    filename = f"converted_{filename2}.mp4"

isoffset = input("Offset the filenames? i.e. starting at 70.mp4 instead of 1.mp4, y/n: ")
if isoffset.lower() == "y": #use .lower() because then it's not case-sensitive
  offset = input("What should it start at?: ")
  try: # test if the input is an integer
    int(offset)
  except:
    print("Invalid! Disabling offset...")
    offset = 1 # set it to start at 1 
  else: # else statements run only if there is no error
    if int(offset) < 1:
      print("Not a valid starting point! Disabling...")
      offset = 1 # set it to start at 1
    else:
      offset = int(offset)
else:
  offset = 1


def with_moviepy(filename): #function that gets the duration of a clip
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(filename)
    duration       = clip.duration
    return duration

duration = with_moviepy(f"{filename}") # duration  of the file
durationint = int(with_moviepy(f"{filename}")) # duration of the file as an integer

if duration - int(duration) != 0: # if the duration isn't a whole number
  durationint = durationint + 1 # makes sure if the video isn't an even amount of minutes that it won't cut the clip

if seconds == 0: # run if seconds mode isn't enabled
  minsinvid = durationint/60  # note that durationint is in seconds, which is why it's divided by 60
  if minsinvid - int(minsinvid) != 0:
    minsinvid = int(minsinvid) + 1 # if the minutes in the video isn't whole, add 1 so it doesn't cut
elif seconds == 1: # run if seconds mode is enabled
  minsinvid = durationint/minstoseconds # minsinvid equals the duration(in seconds) divided by how many seconds in the video
  if minsinvid - int(minsinvid) != 0:
    minsinvid = int(minsinvid) + 1 # if the minutes in the video isn't whole, add 1 so it doesn't cut

if minsinvid % mins != 0: # if the video duration isn't a whole number
  minsinvid = minsinvid - (minsinvid % mins) # minsinvid equals the remainder of itself /  how many seconds each clip is
  minsinvid = int((minsinvid/mins) + 1) # add one so it doesn't cutoff

while g != minsinvid: #set to amount of minutes in the video
    a = init # i dunno why called it "init"
    init = init + minstoseconds #interval to split into
    values = f"{a}-{init}" # adds how many seconds in between clips every time,  starting at 0, so 0-30, 30-60 etc
    g = g+1 # could do g += g but this makes more sense to my head
    f = open("times.txt", "a") # a is append mode
    f.write(f"{values}\n") # write the values
    f.close() # wrap it up

required_video_file = VideoFileClip(filename) # the file we submitted at the beginning
with open("times.txt") as f: # f is times.txt in append mode
  times = f.readlines()
times = [x.strip() for x in times]  # .strip() clears all whitespace for itself in the times 
fullduration = required_video_file.duration # duration in seconds of the file
for time in times: # remember that "time" is just like for i in or something, not something previously defined
  starttime = int(time.split("-")[0]) # splits to before and after the dash, index 0 being the first entry
  endtime = int(time.split("-")[1]) # splits to before and after the dash, index 1 being the second entry
  if starttime >= fullduration:
    print(f"Video too short to complete request! Quitting loop..")
    break
  if endtime >= fullduration: # crops the endtime of the clip if it's too far to complete the request
    print(f"Cropping endtime from {endtime} to {fullduration}!")
    endtime = None # none is null which means it goes as far as it can 
  subclip = required_video_file.subclip(starttime, endtime) # define the subclip as a new thing, if you define it as required_video_file it breaks
  filen = str(times.index(time)+offset)+".mp4" # filen is just the file number, + offset being the specified offset from earlier, which defaults to 1
  subclip.write_videofile(filen, audio_codec='aac') # write the file