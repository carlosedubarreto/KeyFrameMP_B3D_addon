#C:/Users/Pichau/AppData/Local/Programs/Python/Python37/python.exe
# some_file.py
import sys,time
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Downloads/0_Projetos/2020/0_addon/KeyFrameMP_connection')

from . maya_to_keyframe_mp import KeyframeMPClient



from subprocess import Popen
# Popen("C:/Program Files/Keyframe Pro/bin/KeyframePro.exe",shell=False, stdin=None, stdout=None, stderr=None)
kpro_client = KeyframeProClient()


if kpro_client.connect() and kpro_client.initialize():
    print('conectado')
else:
    print('nao conectado')

# #Cria Timeline e abre video
# filepath='D:/Downloads/Video/Drum Bateria/y2mate.com - Bring Me The Horizon - Mantra - Drum Cover_E6VwPUGGkL8_1080p.mp4'
# kpro_client.new_project(empty=True)
# timeline = kpro_client.add_timeline('My Timeline')
# sources = []
# sources.append(kpro_client.import_file(filepath))
# for source in sources:
#     kpro_client.insert_element_in_timeline(source['id'], timeline['id'])
# # Make the timeline active in viewer A
# kpro_client.set_active_in_viewer(timeline['id'], 0)


kpro_client.set_playing(True, play_forwards=True)

kpro_client.set_frame(200, audio=False, from_range_start=False)


kpro_client.is_connected()
kpro_client.initialize()
kpro_client.get_frame()


count_eq_frame=0
entrou=0
limit_frame=100


minut=2
frame_ant=0
ini_time_for_now = datetime.now() 
from datetime import datetime, timedelta 
while True:
    if entrou ==1:
        ini_time_for_now = datetime.now()
        entrou = 0
    time.sleep(0.20)
    print('1-frame_ant :',frame_ant, ' frame :',kpro_client.get_frame(), ' entrou :',entrou,' delta :',datetime.now()-ini_time_for_now)
    # print('count :',count_eq_frame)
    if frame_ant == kpro_client.get_frame():
        ini_time_for_now = datetime.now() 
        entrou=1
        while True:
            time.sleep(0.20)
            print('2-frame_ant :',frame_ant, ' frame :',kpro_client.get_frame(), ' entrou :',entrou,' delta :',datetime.now()-ini_time_for_now)
            if frame_ant != kpro_client.get_frame():
                break
            if datetime.now() > ini_time_for_now + timedelta(minutes=minut):
                break
    frame_ant = kpro_client.get_frame()
    if entrou == 1:
        if datetime.now() > ini_time_for_now + timedelta(minutes=minut):
            break



#pegar bookmarks
# kpro_client.get_bookmarks(id="", include_empty_timelines=True)
# acessando bookmarks
a = kpro_client.get_bookmarks(include_empty_timelines=True)
a[0]['bookmarks']

# primeiro elemento
a[0]['bookmarks'][0]

#tamanho da lista de favoritos
len(a[0]['bookmarks']) 