from flask import *
import os
import json

files_text = ""


def bubble_sort(arr):
    end = len(arr) - 1
    while end > 0:
        last_swap = 0
        for i in range(end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                last_swap = i
        end = last_swap


def getfilesize(fs):
    import math
    size = os.path.getsize(fs)
    if size == 0: return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return "%s %s" % (s, size_name[i])


with open("Path.txt", "r", encoding="UTF-8") as f:
    import numpy as np

    cnt = 15
    path = f.readline().strip()
    file_list = os.listdir(path)
    file_count = len(file_list)
    temp = [[0]*15 for i in range(file_count // cnt)]
    if file_count % cnt != 0:
        temp += [[0] * (file_count % cnt)]
    for i, n in enumerate(file_list):
        temp[i // 15][i % 15] = (n, getfilesize(f"{path}{n}"))
    files_text = json.dumps(temp, indent=2, ensure_ascii=False)

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html', FileListData=files_text)


if __name__ == '__main__':
    app.run(debug=True)
