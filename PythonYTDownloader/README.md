# YouTube Video Downloader
This Small package download video and audio from YouTube with Given URL or Given Name
## Instruction
**We can download Video or Audio from Very Famous Platform YouTube. This Package is capable of downloading Video(S) or Audio(S) From YouTube PlayList or Individual Video with Just a Video URL or With Just the Name or say, title of a Video**
## Packages Used
*If you wanna download package explicitly then use following command*
````cmd
pip install pytube
pip install requests
````
````cmd
pip install git+https://github.com/nficano/pytube.git
````
***or** you can use **requirements.txt** file*
````cmd
pip install -r requirements.txt
````
## USAGE
*Method Used to Download Video(s) or Audio(s).*
*First of all Import "ytdownload" from Package and use as given syntax:*
````python
ytdownload(video_url, vformat, [optional])
````
## Parameters
*__ytdownload__ accepts 2 or 3 parameters 2 are positional means mandatory parameters and last one is optional and this function returns True or False*.

* **video_url:** This argument represent the actual URL of Video Or PlayList (i.e. YouTube URL) or Video Title.  
It is of two types
  1. **URL**: This a actual URL to YouTube Video or YouTube PlayList
  2. **name**: This is Title of Video or Common Name to the video, like 'Latest Python Packages reviews'. It cannot use title of PlayList but single video only
* **vformat:** This argument represent the format, you wanna download as. It is of Two Types 'video' or 'audio'
* **optional (--path)**: This argument represent the path where files are to be stored.  
If passed, File will be stored in the given path like in:  
C:\Users\username\Music which is a Default path for Audio and  
C:\Users\username\Video which is a Default path for Videos, incase path is not given.  
But if path is given, Video and Audio will be stored in given PATH inside Videos and Music Folder resp.  
  syntax:  
      ytdownload(video_url, vformat, path='C:\\Users\\')  

## Example
````python
data = ytdownload('falling by harry styles', 'video')
# This 'data' returns True or False according to isdownloaded or not
````
## Command-line
**Showing Help (details about other arguments)**
````python
pyytdownloader -h
````

````python
pyytdownloader video_url vformat --path PATH
````
**Here --path PATH is optional argument which specifies directory for downloaded files use -h for more details**
