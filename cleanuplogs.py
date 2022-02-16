import os
import pathlib

for folders in os.scandir("logs"):
    try:
        for file in os.scandir(folders):
            fp = pathlib.Path(file)
            os.remove(fp)
            print("removed", fp)
    except:
        pass