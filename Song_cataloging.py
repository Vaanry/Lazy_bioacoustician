from clustimage import Clustimage
import matplotlib.pyplot as plt
import os
import pandas as pd
import shutil

def repertoire(home, img):
    os.chdir(home)
    # Прописываем названия будущих каталогов и создаём папки в основной рабочей директории

    '''Директория, куда будут сохранены звуковые файлы каталога 
    (при наличии этих файлов в рабочей директории)'''

    catalog_sound = home+'\\'+'catalog_sound' 
    if 'catalog_sound' not in os.listdir(home):
        os.mkdir('catalog_sound')

    catalog_img = home+'\\'+'catalog_img' # Директория, куда будут сохранены картинки каталога
    
    if 'catalog_img' not in os.listdir(home):
        os.mkdir('catalog_img')
        
    os.chdir(img) # Меняем рабочую директорию на ту, где лежат искомые картинки
    
    # Основной рабочий скрипт, классифицирующий картинки

    cl = Clustimage(method='hog', params_hog={'orientations':1, 'pixels_per_cell':(40,30), 'cells_per_block':(1,1)}, 
                    verbose=None)

    X = cl.import_data(img)
    # Fit and transform
    results = cl.fit_transform(X)

    # Создаём словарь с лейблами

    song_types = {}
    for i in range(len(results['pathnames'])):
        name = results['pathnames'][i].replace(img+'\\', '').replace('png', 'wav')
        song_types[name] = results['labels'][i]  
        
    # Создаём датафрейм с лейблами и сохраняем его в csv

    df = pd.DataFrame(list(song_types.items()), columns = ['Selection', 'Song type'])
    df.to_csv(home+'\\'+'song_types.csv')
    
    
    # Создаём лейблы для уникальных картинок и копируем их в каталоги с изображениями и звуками

    repertoire = {}
    for file in cl.unique()['pathnames']:
        name = file.replace(img+'\\', '').replace('png', 'wav')
        repertoire[name] = song_types[name]

    for key, value in repertoire.items():
        shutil.copyfile(f'{home}\\{key}', f"{catalog_sound}\\{value}.wav")

    images = {}
    for file in cl.unique()['pathnames']:
        name = file.replace(img+'\\', '')
        images[name] = song_types[name.replace('png', 'wav')]

    for key, value in images.items():
        shutil.copyfile(f'{img}\\{key}', f'{catalog_img}\\{value}.png')
    os.chdir(home)    
    return df, cl