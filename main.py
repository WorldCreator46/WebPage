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
    path = f.readline().strip()
    file_list = dict()
    for n in os.listdir(path):
        file_list[n] = getfilesize(f"{path}{n}")
    files_text = json.dumps(file_list, indent=2, ensure_ascii=False)


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html', FileListData=files_text)


if __name__ == '__main__':
    app.run(debug=True)
