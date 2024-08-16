from moviepy.editor import AudioFileClip,concatenate_audioclips
import os
def mp4_to_mp3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

def concat_audio_files(pathes,output_path,mergedName="merged"):
    clips = [AudioFileClip(c) for c in pathes]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path+"/"+mergedName+".mp3")
    return mergedName+".mp3"

def crop_audio_files(pathes,output_path,cropName,start=5,end=5):
    audio_clip = [AudioFileClip(c) for c in pathes]
    duration=[clip.duration for clip in audio_clip]
    print(duration)
    title_names=[]
    for i in range (len(pathes)):
        cropped_audio_clip = audio_clip[i].subclip(start, duration[i]-end)
        # Export cropped clip to a new file
        dir,file_name=os.path.split(pathes[i])
        print(dir,file_name)
        if cropName is None:
            cropped_audio_clip.write_audiofile(output_path+f'/cropped_{file_name}')
            title_names.append(f'cropped_{file_name}')
        else:
            cropped_audio_clip.write_audiofile(output_path+f'/{cropName}.mp3')
            title_names.append(f'{cropName}.mp3')
            cropName=None
    return title_names


    
'''dir_path = "C:/Users/SmadarENB3/Desktop/songs/concat"

# Get list of all files in directory
file_list = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

# Print list of all files in directory
print(file_list[0])
print(file_list[1])
print(file_list[2])
input("continue")
concat_audio_files(file_list,"C:/Users/SmadarENB3/Desktop/songs/concat/merged","לכרמי-הדר קניאל ויובל דיין חתוך")
'''