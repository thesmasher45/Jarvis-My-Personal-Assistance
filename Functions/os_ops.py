import os 
import subprocess as sp


paths = {
    'notepad': "C:\\Windows\\System32\\notepad.exe"
}



def open_notepad():
    os.startfile(paths['notepad'])

def open_cmd():
    os.system('start cmd')

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_vscode():
    codePath = "C:\\Users\\ADARSH MORE\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    os.startfile(codePath)

def play_music():
    music_dir = 'D:\Music\Favsongs'
    songs = os.listdir(music_dir)
    print(songs)
    os.startfile(os.path.join(music_dir, songs[0]))