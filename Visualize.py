import librosa
import os
import matplotlib.pyplot as plt
import numpy as np


def visualize(home):
    os.chdir(home)
    img = home+'\\'+'img' # записываем имя для папки с картинками и следом создаём её
    
    if 'img' not in os.listdir(home):
        os.mkdir('img')
        
    sound_files = [i for i in os.listdir(home) if 'wav' in i]   
    # Ищем файлы wav в директории.
    
    for sound in sound_files:
        name = sound.replace('.wav', '') #собираем имя файла

        y, sr = librosa.load(sound, sr=44100)
        fig = plt.plot()
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        png = librosa.display.specshow(D, hop_length=512, y_axis='linear', x_axis='time',
                                       sr=sr, cmap='Greys')
        plt.savefig(f'{img}\\{name}.png') # сохраняем файл в папке с картинками
    return img