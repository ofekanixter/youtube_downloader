from flask import Flask, render_template, request
import main_script
from main_script import SONG_DIR
import pandas as pd
import os
app = Flask(__name__)
DEAFULT="default"
DELETE=True
@app.route('/')
def index():
    name = ""
    return render_template('index.html', name=name)

@app.route('/downloader')
def downloader():
    return render_template('downloader.html')

@app.route('/song')
def song():
    return render_template('song.html')

@app.route('/pdf')
def pdf():
    return render_template('pdf.html')
@app.route('/submit', methods=['POST'])
def submit():
    mode = request.form.get('mode')
    file_doc = request.files['choose-file']
    s_folder = request.form.get('source-folder')
    t_folder = request.form.get('target-folder')
    text = request.form.get('text')
    mp3_4 = request.form.get('file-type')
    crop_start=request.form.get("crop-start")
    crop_end=request.form.get("crop-end")
    concat_name=request.form.get("concat-name")
    name, file_extension = os.path.splitext(file_doc.filename)
    # Save the file to a temporary location with the correct file extension
    file_path = 'temp/temp' + file_extension
    file_doc.save(file_path)
    print(mp3_4,concat_name)
    print(mode,file_path,text,s_folder,t_folder,mp3_4,crop_start,crop_end,concat_name)
    if(input("con?")=="N"):
        exit(1)
    start_inputs=input_process(mode,file_path,text,s_folder,t_folder,mp3_4,crop_start,crop_end,concat_name)
    print(start_inputs)
    result=main_script.start(*start_inputs)
    msg=gen_msg(mp3_4)
    if DELETE:
        delete_media_files_from_dir(SONG_DIR)
        delete_media_files_from_dir(SONG_DIR+"/MP4")
    return render_template('/submit.html',mode=mode,  result=result , msg=msg)



def error_input(a,b,c):
    return str(a)+str(b)+str(c)
def input_process(mode,file_path,text,s,t,mp3_4,start,end,concat_name):
    if s==DEAFULT:
        s=None
    if t==DEAFULT:
        t=None
    if mode=="FILE":
        s=file_path
    elif mode=="TEXT" :
        s=text
    return mode,s,t,(start,end),mp3_4=="mp4",concat_name,True
        
def gen_msg(mp3_4):
    file_type="Songs" if mp3_4=="mp3" else "Videos"
    msg="The"+file_type+" you downloaded are:"
    return msg
def delete_media_files_from_dir(directory):
    if input("are you sur you want to delete all media files in the directory: \n"+directory+"\n(Y)")!="Y":
        return "no"
    for file in os.listdir(directory):
        if file.endswith(".mp4") or file.endswith(".mp3"):
            file_path = os.path.join(directory, file)
            os.remove(file_path)
            print(f"Deleted file: {file}") 
if __name__ == '__main__':
    app.run(debug=True)
