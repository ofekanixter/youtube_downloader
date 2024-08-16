import pandas as pd
import pytube
from youtube_audio import general,audio as aud 


COL_HEAD='name'
SPEICIAL_CHAR=['?','@','#','$','*','"','&','|','//','/','(official video)','(Official Music Video)','(Official Video)','(OFFICIAL VIDEO)','(Video Oficial)','(video oficial)','(VIDEO OFICIAL)','(Official Video)']
MP4_SAVE_DIR="C:/Users/SmadarENB3/Desktop/songs/MP4"
MP3_SAVE_DIR="C:/Users/SmadarENB3/Desktop/songs"


def excel_to_titleList(excel_path):
    df=pd.read_excel(excel_path)
    result=df[COL_HEAD].tolist()
    general.print_msg("excel to list completed!",True)
    return result

def titleList_to_reasultsList(titleList):
    reasultsList=list()
    for i in range(len(titleList)):
        reasultsList.append(input_to_pytube(titleList[i]))
    general.print_msg("title list to results list completed!",True)
    return reasultsList


def fix_title(title):
    for i in range(len(SPEICIAL_CHAR)):
        title=title.replace(SPEICIAL_CHAR[i],"")
    title=title.strip()
    title=title.replace("  "," ")
    title=title.replace("   "," ")
    title=title.replace("    "," ")
    title=title.replace("     "," ")
    title=title.title()
    # title=general.hebrew_fix(title)
    return title

def download_resultList(resultsList,dest=MP3_SAVE_DIR ,mp4_format=False):
    i=0
    download_list=list()
    for tubeObj in resultsList:
        i+=1
        general.print_msg("start downloading : "+str(i)+"/"+str(len(resultsList)),True)
        filename=fix_title(tubeObj.title)
        download_list.append(filename)
        print("title is: "+filename)
        if mp4_format:
            dest=MP4_SAVE_DIR
            print("\nMP4\n****************************")
            print(filename,dest)
            tubeObj.streams.get_highest_resolution().download(output_path=dest,filename=filename+".mp4")
            general.print_msg("finish downloading number "+str(i)+"/"+str(len(resultsList)),True,True)
            continue
        print(filename)
        print(dest)
        #@tubeObj.streams.get_audio_only().download(output_path=dest+"/MP4",filename=filename+".mp4")
        tubeObj.streams.filter(only_audio=True).first().download(output_path=dest,filename=filename+".mp3")
        general.print_msg("finish downloading number "+str(i)+"/"+str(len(resultsList)),True,True)
        #@mp3Path=dest+"/"+filename+".mp3"
        #@mp4Path=dest+"/MP4/"+filename+".mp4"
        #@aud.mp4_to_mp3(mp4Path,mp3Path)
        #@general.deleteFile(mp4Path)
    return download_list

            
def input_to_pytube(link_or_title):
    if link_or_title.startswith(("https", "youtube")):
        return pytube.YouTube(link_or_title)
    else:
        return pytube.Search(link_or_title).results[0]

  
def fix_file_text_from_youtube(titleList,path):
    if titleList[0]!='\n':
        return titleList
    try:
        text_file =open(path[:-4]+'_draft.txt','w')
        ret_list=[]
        for i in range(2,len(titleList),6):
            ret_list.append(titleList[i])
        ret_list_str=general.str_list(ret_list,False)
        text_file.write(ret_list_str)
        text_file.close
        return ret_list
    except Exception as err:
        print("priblem with convert playlist to title list")
        exit(1)
    
