from flask import *
import os
import json


def bubble_sort(arr):
    end = len(arr) - 1
    while end > 0:
        last_swap = 0
        for i in range(end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                last_swap = i
        end = last_swap


def getfilesize(fs='', file_size=-1):
    import math
    if file_size != -1:
        size = file_size
    else:
        size = os.path.getsize(fs)
    if size == 0: return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return "%s %s" % (s, size_name[i])


f = open("Path.txt", "r", encoding="UTF-8")
path = f.readline().strip()
file_list = os.listdir(path)
translation_volume_list = [(n, getfilesize(fs=f"{path}{n}")) for n in file_list]
volume_list = [(os.path.getsize(f"{path}{n}"),n) for n in file_list]
bubble_sort(volume_list)
f.close()

def create(sort_number=0):
    cnt = 15
    file_count = len(file_list)
    temp = [[0] * 15 for i in range(file_count // cnt)]
    if file_count % cnt != 0:
        temp += [[0] * (file_count % cnt)]
    if sort_number == 0:
        for i, n in enumerate(translation_volume_list):
            temp[i // 15][i % 15] = n
    if sort_number == 1:
        for i, n in enumerate(reversed(translation_volume_list)):
            temp[i // 15][i % 15] = n
    elif sort_number == 2:
        for i, n in enumerate(volume_list):
            temp[i // 15][i % 15] = (n[1], getfilesize(file_size=n[0]))
    elif sort_number == 3:
        for i, n in enumerate(reversed(volume_list)):
            temp[i // 15][i % 15] = (n[1], getfilesize(file_size=n[0]))
    return json.dumps(temp, indent=2, ensure_ascii=False)


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html', FileListData=create())


@app.route('/sort/<classification>')
def sorted_file_list(classification):
    if classification == "Name-Ascending":
        return render_template('index.html', FileListData=create())
    elif classification == "Name-Descending":
        file_list.reverse()
        return render_template('index.html', FileListData=create(sort_number=1))
    elif classification == "Volume-Ascending":
        return render_template('index.html', FileListData=create(sort_number=2))
    elif classification == "Volume-Descending":
        return render_template('index.html', FileListData=create(sort_number=3))


@app.route('/search/<word>')
def search_word(word):
    search_list = [fn for fn in file_list if word in fn]
    search_translation_volume_list = [(n, getfilesize(fs=f"{path}{n}")) for n in search_list]
    cnt = 15
    file_count = len(search_translation_volume_list)
    temp = [[0] * 15 for i in range(file_count // cnt)]
    if file_count % cnt != 0:
        temp += [[0] * (file_count % cnt)]
    for i, n in enumerate(search_translation_volume_list):
        temp[i // 15][i % 15] = n
    return render_template('index.html', FileListData=json.dumps(temp, indent=2, ensure_ascii=False))


@app.route('/download/<filename>')
def download_file(filename):
    mime_type = ""
    if filename.split(".")[1] == "7z":
        mime_type = 'application/x-7z-compressed'
    elif filename.split(".")[1] == "zip":
        mime_type = 'application/zip'
    return send_file(path_or_file=f"{path}{filename}",
                     mimetype=mime_type,
                     attachment_filename=filename,
                     as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='913')
