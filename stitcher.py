import os
from datetime import datetime

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

    chapter = j[2:4]
    print("chapter: ", chapter)

    video_num = j[4:8]
    print("video number, ", video_num)

    if video_num not in fs:
        fs[video_num] = []

    fs[video_num].append(File(chapter, j))


def key(f: File):
    return f.chapter


output_count = 0
fmpeg_intermediate = "ffmpeg -i %s -c copy %s.ts"
output_prefix = "%s" % datetime.now().date()
output_name = output_prefix + "-%s.MP4"
ffmpeg_concat = "ffmpeg -i \"concat:%s\" -c copy %s"

try:
    for j in fs:
        if len(fs[j]) == 0:
            # not possible
            continue

        if len(fs[j]) == 1:
            os.rename(fs[j][0].filename, output_name % j)
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

        print(ffmpeg_concat % ("|".join(i_files), output_name % j))
        os.system(ffmpeg_concat % ("|".join(i_files), output_name % j))

        print(i_files)

        for i in range(intermediate_count):
            os.remove("%s.ts" % i)

        output_count = output_count + 1
except:
    print("Failed :(")
