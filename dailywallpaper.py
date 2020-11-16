import requests
import json
# import os


def pos_ratio(w, h):  # Positive aspect ratio to be used as wallpaper
    try:
        w = int(w)
        h = int(h)
    except ValueError:
        print('ValueError: argument passed not width or height')
        return None
    if w / h > 1:
        return True
    else:
        return False


def get_photosjson(page):  # Retrieve json from unsplashed
    url = f'https://unsplash.com/napi/topics/wallpapers/photos?page={page}' \
           '&per_page=10'
    r = requests.get(url)
    try:
        tphotos = r.json()
    except ValueError:
        print('Request Error: JSON could not be retrieved')
    return tphotos


def get_photourls():
    page = library['page']
    photosjson = get_photosjson(page+1)
    count = 0
    for photo in photosjson:
        id = photo['id']
        width = photo['width']
        height = photo['height']
        rawurl = photo['urls']['raw']
        uploadedby = photo['user']['username']
        if id in library or not pos_ratio(width, height) or \
           pos_ratio(width, height) is None:
            continue
        library[id] = {
            'retrieved': False,
            'width': int(width),
            'height': int(height),
            'rawurl': rawurl,
            'uploadedby': uploadedby
            }
        count += 1
    library['page'] = page+1
    print(f'Retrieved {count} photo URLs.')


def downloadphoto():
    photourl = None
    while photourl is None:
        for photo in library:
            if photo == 'page' or library[photo]['retrieved']:
                continue
            photourl = library[photo]['rawurl']
            break
        else:
            get_photourls()
    print('Downloading photo...')
    with open('wallpaper/photo.jpg', 'wb') as fp:
        r = requests.get(photourl)
        fp.write(r.content)
    library[photo]['retrieved'] = True
    print('Downloaded photo.')
    # os.startfile('wallpaper\\photo.jpg')


try:
    with open('library.json', 'r') as fp:
        library = json.load(fp)
except FileNotFoundError:
    print('JSON not found, creating new library.')
    library = {'page': 0}

if __name__ == '__main__':
    downloadphoto()

with open('library.json', 'w') as fp:
    json.dump(library, fp, indent=2)


# https://unsplash.com/napi/topics/wallpapers/photos?page=1&per_page=10
