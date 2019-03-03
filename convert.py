"""
Copyright (C) 2019  Visperi
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os


# ffmpeg -i video.mp4 -ac 1 -b:a 32k audio.mp3
def convert_file(path_in, path_out, make_mono, bitrate, testing_mode=True):
    # TODO: subprocess instead of os.system?
    # TODO: Error handling and logging?
    # TODO: ffmpeg-python instead of straight system calls?
    if make_mono:
        mono = "-ac 1"
    else:
        mono = ""
    if bitrate == "Default":
        def_bitrate = ""
    else:
        def_bitrate = f"-b:a {bitrate}k"
    if testing_mode:
        print(f"ffmpeg -i \"{path_in}\" {mono} {def_bitrate} \"{path_out}\"")
    else:
        # Call ffmpeg in system console and after conversion pause it if user wants to read the report
        os.system(f"ffmpeg -i \"{path_in}\" {mono} {def_bitrate} \"{path_out}\" & echo Conversion ended. "
                  f"& pause")
