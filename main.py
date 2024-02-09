import time
from Source.Read_input import ReadSettings
from Source.Reelset import Reelset
start_time = time.time()
from Source.CF_replace_symbols import CF_Reel, CF_Reelset, Insert_CF_Symbols_instead_of_11

###################################### НАДО ВОТ ЭТО ЗАДАТЬ ######################################
GAME_NAME = "SFS_vit"
INNER_DIRECTORY = ""   # Имя папки внутри основной папки GAME_NAME, если таковой нет, то просто оставляй пустую строчку ""
SETTING_FILE_NAME = "blocker_even"             # Только имя файла в папке Settings, путь и расширение не надо
REELS_FILE_NAME = ""                       # Только имя файла в папке Reels, путь и расширение не надо
#################################################################################################



reel_data = ReadSettings(SETTING_FILE_NAME, INNER_DIRECTORY, REELS_FILE_NAME, GAME_NAME)
reelset = Reelset(reel_data)
#reelset = CF_Reelset(reel_data)
reelset.MakeReelSet()

for reel in reelset.reels:
    for i in range(len(reel.symbols)):
        window = reel.TakeWindow(i,3)
        if 8 in window:
            reel.weights[i] = 0


#Insert_CF_Symbols_instead_of_11(reelset)

reelset.PrintReelset()

print("\nTime:", '{:.3f}'.format(time.time() - start_time), "seconds")




