import os
import argparse

from  youtube_audio import general,audio,pytube_auto as tube
from util.drive_util.drive_util import GoogleDriveClient
from util.config_util import ConfigUtil
VALID_INPUT=['','FILE','TEXT','CONCAT','CROP' , 'DRIVE']
HIGHLIGHTS_TAMPLATE=""
CONCAT_SONG_DIR="C:/Users/SmadarENB3/OneDrive/Desktop/songs/concat"
SONG_DIR="C:/Users/SmadarENB3/OneDrive/Desktop/songs"
MERGED_SAVE_DIR="C:/Users/SmadarENB3/OneDrive/Desktop/songs/concat/merged"
TEXT_FILE_PATH="C:/Users/SmadarENB3/OneDrive/Desktop/ofek/programing/python/youtube_downloader/titles.txt"
PYTHON_DIR="C:/Users/SmadarENB3/OneDrive/Desktop/ofek/programing/python/youtube_downloader"
TEMP_FOLDER_PATH='C:/Users/SmadarENB3/OneDrive/Desktop/ofek/programing/python/youtube_downloader/song_file_temp'
drive_access = GoogleDriveClient()
config_dict= ConfigUtil().load_config()
drive_song_file="drive_titles_file"
MODE=""
print(config_dict)

def upload_and_cleanup_temp_folder(temp_folder_path, drive_folder_id=None):
    """
    Uploads all MP3 files from the specified temp folder to Google Drive and deletes them afterward.

    Args:
        service: Authenticated Google Drive API service instance.
        temp_folder_path: Path to the local temp folder containing MP3 files.
        drive_folder_id: Google Drive folder ID where the files will be uploaded (optional).
    """
    # Ensure the temp folder exists
    if not os.path.exists(temp_folder_path):
        print(f"Temp folder '{temp_folder_path}' does not exist.")
        return
    
    # Iterate over all files in the temp folder
    for file_name in os.listdir(temp_folder_path):
        file_path = os.path.join(temp_folder_path, file_name)

        # Check if the file is an MP3
        if os.path.isfile(file_path) and file_name.lower().endswith('.mp3'):
            # Upload the MP3 file to Google Drive
            drive_access.upload_mp3_file(file_path, file_name)

            # Delete the file after uploading
            os.remove(file_path)
            print(f"Uploaded and deleted file: {file_name}")

def file_mode(source,dest,mp4_format):
    if source.endswith('.txt'):
        return text_file_mode(source,dest,mp4_format)
    elif source.endswith('.xlsx'):
        return excel_file_mode(source,dest,mp4_format)
    print("invalid file:\n"+source)
    
def excel_file_mode(source,dest,mp4_format):
    titleList=tube.excel_to_titleList(source)
    resultsList=tube.titleList_to_reasultsList(titleList)
    return tube.download_resultList(resultsList,dest,mp4_format)

def text_file_mode(source,dest,mp4_format):
    if(source==""):
        source=TEXT_FILE_PATH
    if(os.path.exists(source)):
        text_file =open(source,'r')
    else:
        print("this path is not exist :"+source)
    titleList=text_file.readlines()
    text_file.close
    titleList=tube.fix_file_text_from_youtube(titleList,source)
    resultsList=tube.titleList_to_reasultsList(titleList)
    return tube.download_resultList(resultsList,dest,mp4_format)

def text_mode(text,dest,mp4_format,html=False):
    titleList= list()
    if html:
        titleList=text.split('\n')
        resultsList=tube.titleList_to_reasultsList(titleList)
        return tube.download_resultList(resultsList,dest,mp4_format)
    oneMore=True
    while(oneMore):
        text = input('enter song\n')
        titleList.append(text.split('\n'))
        oneMore=input('enter for one more or any key for finish\n')==''
    resultsList=tube.titleList_to_reasultsList(titleList)
    return tube.download_resultList(resultsList,dest,mp4_format)

def check_input(c):
    if c==None:
        return False
    valid=c in VALID_INPUT
    if not valid:
        msg="the input: '{c}' is illegal please enter on of the valid inputs as \n{valid_list}".format(c=c,valid_list=VALID_INPUT)
        print(msg)
    return valid


def concat_audio_mode(in_folder,out_folder,merged_name="merged"):
    pathes=[]
    title_list=list()
    filesnames = next(os.walk(in_folder), (None, None, []))[2]  # [] if no file
    if filesnames == []:
        print("no files in concat defualt dir")
        exit
    for name in filesnames:
        title_list.append(name)
        pathes.append(in_folder+"/"+name)
    ###print("title_list")
    ###print(title_list)
    ###print(merged_name)
    return audio.concat_audio_files(pathes,out_folder,merged_name),title_list

def crop_audio_mode(in_folder,out_folder,st_end,cropName):
    pathes=[]
    title_list=list()
    filesnames = next(os.walk(in_folder), (None, None, []))[2]  # [] if no file
    if filesnames == []:
        print(f"no files in {in_folder} dir")
        exit
    for name in filesnames:
        title_list.append(name)
        pathes.append(in_folder+"/"+name)
    ###print("title_list")
    ###print(title_list)
    ###print(cropName)
    st_end=st_end.split("-")
    ###print(st_end)
    return audio.crop_audio_files(pathes,out_folder,cropName,int(st_end[0]),int(st_end[1])),title_list

def get_drive_file():
    metadata=drive_access.get_file_metadata(file_name=drive_song_file)
    if metadata.get('modifiedTime') == config_dict['youtube_config']['drive_song_file_last_edit']:
        return False
    config_dict['youtube_config']['drive_song_file_last_edit'] = metadata.get('modifiedTime')
    drive_access.download_file(file_name=drive_song_file)
    return True


def concat_audio_mode_old(dir=CONCAT_SONG_DIR,merged_dir=MERGED_SAVE_DIR):
    oneMore=input('just enter for defualt or  any key choose pathes\n')==''
    pathes=[]
    title_list=list()
    if oneMore:
        filesnames = next(os.walk(CONCAT_SONG_DIR), (None, None, []))[2]  # [] if no file
        if filesnames == []:
            print("no files in concat defualt dir")
            exit
        for name in filesnames:
            title_list.append(name)
            pathes.append(CONCAT_SONG_DIR+"/"+name)
    while(not oneMore):
        path = input('enter song to be concat full path\n')
        pathes.append(path)
        title_list.append(path.split(sep='/')[-1])
        oneMore=input('enter for oneMore or any key for finish\n')!=''
    output = input('enter for defaualt dir or enter output path dir\n')
    mergedName= input("enter merged name\n")
    ###print("title_list")
    ###print(title_list)
    if output == '':
        return audio.concat_audio_files(pathes,MERGED_SAVE_DIR,mergedName),title_list
    else:
        return audio.concat_audio_files(pathes,output,mergedName),title_list
def start(mode,s,d,st_end,mp4_format=False,name="merged",html=False):
    title_list=list()
    print(mode,s,d,st_end,mp4_format,html)
    if mode == "DRIVE":
        if not get_drive_file():
            print("no need to download")
            return
        mode = "FILE"
        MODE="DRIVE"
    match mode:
        case "CONCAT":
            if(d is None):
                d=MERGED_SAVE_DIR
            if(s is None):
                s=CONCAT_SONG_DIR
            name,title_list=concat_audio_mode(s,d,name)
        case "CROP":
            if(d is None):
                d=SONG_DIR
            if(s is None):
                s=SONG_DIR
            name,title_list=crop_audio_mode(s,d,st_end,name)
        case "FILE":
            ###print("here")
            if(s is None):
                s=TEXT_FILE_PATH
            if(d is None):
                d=SONG_DIR
            if MODE == "DRIVE":
                d= TEMP_FOLDER_PATH
            title_list=file_mode(s,d,mp4_format)
        case "TEXT":
            if(d is None):
                d=SONG_DIR
            title_list=text_mode(s,d,mp4_format,html)
    if MODE == "DRIVE":
        upload_and_cleanup_temp_folder(TEMP_FOLDER_PATH)
        config_dict['youtube_config']['drive_song_file_last_edit'] =drive_access.get_file_metadata(
            file_name=drive_song_file).get('modifiedTime')
        ConfigUtil().save_config(config_dict)
    if mode!='CROP' and mode!='CONCAT':
        print("\nThe title that downloaded are :\n"+general.str_list(title_list))
        return title_list
    else:
        print("\nThe title that merged/cropped are :\n{}\nThe merged/cropped name is:\n{}".format(general.str_list(title_list),general.str_list(name)))
        return title_list

def main():

    parser = argparse.ArgumentParser(description='youtube downloader or mp3 concating')
    parser.add_argument('mode',choices=VALID_INPUT, help='which mode to start')
    parser.add_argument('--source',help='from which dir to take files')
    parser.add_argument('--dest',help='to which dir to save files')
    parser.add_argument('-MP4',action="store_true",
                        help='is the format you want is MP4 (default:False)')
    parser.add_argument('--name',
                        help='name for the audio file that been merged or cropped')
    parser.add_argument('--st_end',
                        help='start and ending in sec for the audio file to be cropped')
    args = parser.parse_args()
    args = parser.parse_args()
    c=args.mode
    mp4_format=args.MP4
    d=args.dest
    s=args.source
    st_end=args.st_end
    if(d is None and c!="CONCAT"):
        d= SONG_DIR
    merged_name=args.name if args.name!=None else "merged"
    print(c,args.source,args.dest,st_end,mp4_format,merged_name)
    #while(not check_input(c)):
    #   c=input('enter mode : concat, excel ,textFile or text :\n')
    #     c='text'
    start(c,s,d,st_end,mp4_format,merged_name)

   

if __name__ == "__main__":
    main()