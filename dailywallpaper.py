import requests
import json

URL = 'https://unsplash.com/napi/topics/wallpapers/photos?page={}&per_page=10'


def pos_ratio(w, h):
    '''Positive aspect ratio to be used as wallpaper.'''
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


def get_photosjson(page):  
    '''Retrieve json from unsplashed. Input: page number.'''
    url_photos = URL.format(page)
    r = requests.get(url_photos)
    try:
        tphotos = r.json()
    except ValueError:
        print('Request Error: JSON could not be retrieved')
    return tphotos  # Returns a json file


def get_photodetails(lib):
    addtllib = dict()
    count = 0
    page = lib['page']
    photosjson = get_photosjson(page+1)
    for photo in photosjson:
        id = photo['id']
        width = photo['width']
        height = photo['height']
        rawurl = photo['urls']['raw']
        uploadedby = photo['user']['username']
        description = photo['alt_description']
        if id in lib or not pos_ratio(width, height) or \
           pos_ratio(width, height) is None:
            continue
        addtllib[id] = {
            'retrieved': False,
            'width': int(width),
            'height': int(height),
            'rawurl': rawurl,
            'uploadedby': uploadedby,
            'description': description
            }
        count += 1
    addtllib['page'] = page+1
    return addtllib, count  # Return new lib of urls instead of muting old lib


def get_photourl(lib):
    '''Retrieves an unretrieved photo url from library.'''
    for photoid in lib:
        if photoid == 'page' or lib[photoid]['retrieved']:
            continue
        photourl = lib[photoid]['rawurl']
        return photoid, photourl  # Returns a tuple (photo id, photourl); only one photo
    else:
        return None


def downloadphoto(id, url):  
    '''Downloads a photo, given that Input is a tuple(photoid, photourl)'''
    with open(f'wallpapers/{id}.jpg', 'wb') as fp:
        r = requests.get(url)
        fp.write(r.content)


if __name__ == '__main__':
    try:
        with open('library.json', 'r') as fp:
            library = json.load(fp)
    except FileNotFoundError:
        print('Library not found, creating new library.')
        library = {'page': 0}

    photo = None
    while photo is None:
        photo = get_photourl(library)
        try:
            downloadphoto(photo[0], photo[1])
            print('Downloading photo...')
        except TypeError:
            print('All photos in library retrieved.\nRetrieving more.')
            addtlurls = get_photodetails(library)  # get dict with new urls
            print(f'Retrieved {addtlurls[1]} photo URLs.')
            library.update(addtlurls[0])  # Update(merge) old dict with addtl

    desc = library[photo[0]]['description']
    library[photo[0]]['retrieved'] = True
    print(f'Downloaded photo. {photo[0]} - {desc}')

    with open('library.json', 'w') as fp:
        json.dump(library, fp, indent=2)
    # input('\nPress any key to exit.')

# https://unsplash.com/napi/topics/wallpapers/photos?page=1&per_page=10
