from webbrowser import get
from winsound import PlaySound
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import os, requests, argparse

# Exceptions Classes
class DownloaderExceptions(Exception):
    def __init__(self):
        print('Exception: DownloaderException')
class VideoUrlException(DownloaderExceptions):
    def __init__(self, message):
        self.__message = str(message).capitalize()
    def __str__(self):
        return "VideoUrlException: {}".format(self.__message)
class VideoFormatError(DownloaderExceptions):
    def __init__(self, message):
        self.__message = str(message).capitalize()
    def __str__(self):
        return 'VideoFormatError: {}'.format(self.__message)
class VideoExistError(DownloaderExceptions):
    def __init__(self, message):
        self.__message = str(message).capitalize()
    def __str__(self):
        return 'VideoFormatError: {}'.format(self.__message)
class VideoSrcType(DownloaderExceptions):
    def __init__(self, message):
        self.__message = str(message).capitalize()
    def __str__(self):
        return 'VideoSrcType: {}'.format(self.__message)

# On Complete Print Check Sign
def on_complete():
    "Don't Use this, throws error"
    try:
        print(u'\u2713')
    except UnicodeError:
        print("@")
def getVideoUrl(topic):
    "Don't Use this, throws error"
    url = 'https://www.youtube.com/results?q=' + topic
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count+=1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count-5] == "/results":
        try:
            raise VideoExistError("No Video Found with that name")
        except VideoExistError as e:
            print(e)
            return False
    return "https://www.youtube.com"+lst[count-5]

def checkExistence(name, path, **kargs):
    "Don't Use this, throws error"
    unwanted = ['/', '\\', '*', ':', '?', '"', '<', '>', '|', '#']
    name = str(name)+str(".mp3")
    cbType = kargs.get('get', '__default')
    for item in unwanted:
        if item in name:
            name = name.replace(item, '')
    path = os.path.join(path, 'Music')
    if cbType == '__default':
        return os.path.exists(os.path.join(path, name))
    else:
        return name
def rename(direc):
    "Don't Use this, throws error"
    direc = direc.replace('/', '\\')
    source = direc
    direc = direc.replace(".mp4", ".mp3")
    path = direc
    try:
        os.rename(source, path)
        on_complete()
    except FileExistsError:
        os.remove(source)
        print("\nFile Already Exist")
def downloader(video_url, vformat, **kargs):
    takenPath = kargs.get('path', '__default')
    if takenPath == '__default':
        takenPath = os.environ.get('USERPROFILE')
    tempPath = kargs.get('tempPath', False)
    if video_url == '':
        try:
            raise VideoUrlException("Video URL cannot be Empty String")
        except VideoUrlException as e:
            print(e)
            return False
    elif video_url == None:
        try:
            raise VideoUrlException('Video URL cannot be of NoneType')
        except VideoUrlException as e:
            print(e)
            return False
    else:
        vformat = vformat.lower()
        if vformat != 'video' or vformat != 'audio':
            ytd = YouTube(video_url, on_progress_callback=on_progress)
            video_title = ytd.title
            if vformat == 'audio':
                path_ = os.path.join(takenPath, 'Music')
                if tempPath != False:
                    path_ = os.path.join(path_, tempPath)
                if kargs.get('type'):
                    result = checkExistence(video_title, path_, get='playlist')
                else:
                    result = checkExistence(video_title, path_)
                if result == True:
                    print("Audio \"{}\"\nAlready Exist in \"{}\\Music\"\nTry Changing Path, if you wanna download anyway".format(video_title, path_))
                    return False
                elif result == False:
                    print("Downloading Audio {}.mp3\n".format(video_title), end='')
   
                    cb = ytd.streams.get_audio_only().download(path_)
                    ytd.register_on_complete_callback(rename(cb))
                    return True
                else:
                    return result
            else:
                path_ = os.path.join(takenPath, 'Videos')
                if tempPath != False:
                    path_ = os.path.join(path_, tempPath)
                    
                if kargs.get('type'):
                    result = checkExistence(video_title, path_, get='playlist')
                else:
                    result = checkExistence(video_title, path_)
                if result == True:
                    print("Video \"{}\"\nAlready Exist in \"{}\\Videos\"\nTry Changing Path, if you wanna download anyway".format(video_title, path_))
                    return False
                elif result == False:
                    print("Downloading Video {}.mp4\n".format(ytd.title), end='')

                    ytd.streams.get_highest_resolution().download(path_)
                    ytd.register_on_complete_callback(on_complete())
                    return True
                else:
                    return result
        else:
            try:
                raise VideoFormatError("Only Audio or Video format allowed")
            except VideoFormatError as e:
                print(e)
                return False
def ytdownload(video_url, vformat, **kargs):
    """
    Download YouTube Video in Audio or Video Formate as Specified
    Takes Two Positional Arguments and one Optional Arguments
    1. video_url
        It is a Actual Video URL from YouTube. It may either be URL of
        Single Video or PlayList
    2. vformat
        It is a Format in which download should be taken place
        'audio' for Audio and 'video' for Video
    3. path='PATH'
        It is optional.
        It specifies where the files should be downloaded.
        By Default
            it stores in USERPROFILE/Musics for Audio and /Videos for Videos
        But by providing argument as
            path='certain_path' video or audio will be downloaded in certain_path
    eg:
    ytdownload(video_url, 'audio', path='C:/Users/root/Musics')
    """#.format(os.environ.get('USERPROFILE'), os.environ.get('USERPROFILE'))
    path = kargs.get('path', '__default')
    video_src_type = ''
    if str(video_url).startswith('https://www.youtube.com'):
        if str(video_url).startswith('https://www.youtube.com/playlist'):
            video_src_type = 'playlist'
        else:
            video_src_type = 'single'
    else:
        video_src_type = 'name'
    if video_url == '' or None:
        try:
            raise VideoUrlException('Empty string or NoneType is not acceptable as VideoUrl')
        except VideoUrlException as e:
            print(e)
            return False
    else:
        if video_src_type == 'name':
            url = getVideoUrl(video_url)
            if vformat == 'video':
                if downloader(url, 'video', path=path):
                    return True
                else:
                    return False
            elif vformat == 'audio':
                if downloader(url, 'audio', path=path):
                    return True
                else:
                    return False
            else:
                try:
                    raise VideoFormatError('Only Audio or Video format in allowed')
                except VideoFormatError as e:
                    print(e)
                    return False
        elif video_src_type == 'single':
            if vformat == 'video':
                if downloader(video_url, 'video', path=path):
                    return True
                else:
                    return False
            elif vformat == 'audio':
                if downloader(video_url, 'audio', path=path):
                    return True
                else:
                    return False
            else:
                try:
                    raise VideoFormatError('Only Audio or Video format in allowed')
                except VideoFormatError as e:
                    print(e)
                    return False
        elif video_src_type == 'playlist':
            plist = Playlist(video_url)
            get_url = plist.video_urls
            if vformat == 'video':
                for item in get_url:
                    if downloader(item, 'video', path=path, tempPath = plist.title):
                        return True
                    else:
                        return False
                else:
                    return False
            elif vformat == 'audio':
                collection = []
                for item in get_url:
                    result = downloader(item, 'audio', path=path, tempPath = plist.title)
                    if result:
                        return True
                    else:
                        collection.append(result)
                for item in collection:
                    if item == False:
                        return False
                    else:
                        return True
                else:
                    return False
            else:
                try:
                    raise VideoFormatError('Only Audio or Video format in allowed')
                except VideoFormatError as e:
                    print(e)
                    return False
        else:
            try:
                raise VideoSrcType('VideoSrcType Error: Only YouTube video can be downloaded')
            except VideoSrcType as e:
                print(e)
                return False
def main():
    parsers = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parsers.add_argument('video_url', help="""
    (Required)
        URL of YouTube Video to be download.
        It may either be Title of video or URL of single video or playlist of video
    """)
    parsers.add_argument('vformat', help="""
    (Required)
        it a format in which video is to be downloaded
            'audio' for Music and 'video' for Videos
    """)
    parsers.add_argument('--path', help="""
    (Optional)
        It a path where video or audio is to be downlaoded
        Defaults:
            {}\\Music for Musics
            {}\\Videos for video
        eg. --path='[YOUR PATH]'
    """.format(os.environ.get('USERPROFILE'), os.environ.get('USERPROFILE')))
    args = parsers.parse_args()
    
    url = args.video_url
    form = args.vformat
    path = args.path
    if path == None:
        path = '__default'
    if form == 'audio':
        print('Check {}\\Music'.format(os.environ.get('USERPROFILE')))
    else:
        print('Check {}\\Videos'.format(os.environ.get('USERPROFILE')))
    if ytdownload(url, form, path=path) == True:
        print('Downloaded Successfully ')
    else:
        print('Error Occured! Cannot be downloaded')
if __name__ == '__main__':
    main()