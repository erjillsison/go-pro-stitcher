import os

files = os.listdir(".")

class File:
  def __init__(self, chapter, filename):
    self.chapter = chapter
    self.filename = filename

fs = {}

for j in files:
    prefix = j[0:2]
    
    if prefix != "GH":
        continue

    print(j[0:2], end =" ")


    print("chapter: ", j[3:4], end =" ")
    video_num = j[5:8]
    print("video number, ", video_num)
        
    if video_num not in fs:
        fs[video_num] = []

    fs[video_num].append(File(j[3:4],j))

def key(f:File):
    return f.chapter

output_count = 0
fmpeg_intermediate = "ffmpeg -i %s -c copy %s.ts"
ffmpeg_concat = "ffmpeg -i \"concat:%s\" -c copy output%s.mp4"

try:
    for j in fs:
        # TODO if only one file, just rename so it can be clearly seen?

        if len(fs[j]) <= 1:
            continue
        
        fs[j].sort(key=key)
        
        intermediate_count = 0
        for i in fs[j]:
            print(fmpeg_intermediate % (i.filename,  intermediate_count))
            os.system(fmpeg_intermediate % (i.filename,  intermediate_count))
            intermediate_count = intermediate_count + 1
        
        i_files = []
        for i in range(intermediate_count):
            i_files.append("%s.ts" % i)
        
        print(ffmpeg_concat % ("|".join(i_files), j))
        os.system(ffmpeg_concat % ("|".join(i_files), j))
        
        print(i_files)

        for i in range(intermediate_count):
            os.remove("%s.ts" % i)

        output_count = output_count + 1
except:
    print("Failed :(")