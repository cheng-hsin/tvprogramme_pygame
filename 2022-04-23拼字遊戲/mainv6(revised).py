#1920*1080
import pygame
# coding=utf-8


black = (12, 15, 10)
white = (255, 255, 255)
gray = (45,45,45)
M = 4
red = (251, 75, 78)
yellow = (251, 255, 18)
blue = (0, 126, 167)
WIDTH = 19 * M #一個格子寬度
HEIGHT = 19 * M #一個格子高度
MARGIN = 3 * M #縫隙寬度
FONTSIZE = 15 * M #文字大小
text_margin = 2.5 * M #文字微調
window_size = [1920, 1080]  #視窗大小
hint_size=60 #提示文字大小

grid = []
textarr=[]
start=[]
titlearr=[]
hints=[]
hint= ""
chap="main"
count=0
letter=""


#顯示標題的陣列
for row in range(10):
    titlearr.append([])
    for column in range(11):
        titlearr[row].append("")

#一開始的方塊顏色
for row in range(10):
    start.append([])
    for column in range(11):
        start[row].append("0")

#一開始的提示
for row in range(10):
    hints.append([])
    for column in range(11):
        hints[row].append("0") 


#呼叫open函式開啟一個檔案
file =open(chap+".txt","r",encoding="utf-8")
all_data = file.readlines()
for line in all_data:
    #print(line.strip())
    arr=line.split(',')
    column = int(arr[2])
    row = int(arr[3])
    if arr[4].strip() == "H":
      text=arr[1]
      titlearr[row][column-1]= arr[0]
      for i in text:
        #print(i)
        start[row][column] = i
        column+=1
    if arr[4].strip() == "V":
      text=arr[1]
      titlearr[row-1][column]= arr[0]
      for i in text:
        #print(i)
        start[row][column] = i
        row+=1
    #print(arr[1])

#在完成操作後要將檔案關閉
file.close()

def show_text(surface_handle, pos, text, color, font_size = 13, font_bold = False, font_italic = False):
    # cur_font = pygame.font.SysFont('宋體', font_size)		# 獲取系統字型
    cur_font = pygame.font.Font('./TWSung.otf', font_size)		 # 獲取字型，並設定大小
    cur_font.set_bold(font_bold)							 # 設定是否加粗
    cur_font.set_italic(font_italic)						 # 設定是否斜體
    text_fmt = cur_font.render(text, 1, color)				 # 設定文字內容
    surface_handle.blit(text_fmt, pos)# 繪製文字


#按下按鈕後的方塊
for row in range(10):
    grid.append([])
    for column in range(11):
        grid[row].append(0) 
#grid[1][5] = 1

#顯示文字的陣列
for row in range(10):
    textarr.append([])
    for column in range(11):
        textarr[row].append("0")






pygame.init()

#聲音
#crash_sound = pygame.mixer.Sound("./crash.wav")
def crash():
    ####################################
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    ####################################

#隱藏標題:在window_size後加上", pygame.NOFRAME"
scr = pygame.display.set_mode(window_size)
pygame.display.set_caption("字詞填空")
done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # 按下 "Esc" 鍵，則結束
                done = True
            
            for line in all_data:
              arr=line.split(',')
              if arr[0] == pygame.key.name(event.key).upper():
                #crash()
                #print(arr[1])
                column = int(arr[2])
                row = int(arr[3])
                hint= arr[5].strip() #設定提示文字
                if count==1 and letter == event.key:
                    if arr[4].strip() == "H":
                      text=arr[1]
                      for i in text:
                        #print(i)
                        start[row][column] = "0"
                        grid[row][column] = 1
                        textarr[row][column] = i
                        column+=1
                    if arr[4].strip() == "V":
                      text=arr[1]
                      for i in text:
                        #print(i)
                        start[row][column] = "0"
                        grid[row][column] = 1
                        textarr[row][column] = i
                        row+=1
                    count=0
                elif count==1 and letter != event.key:
                    letter = event.key

                if count==0 and letter!= event.key:
                    letter= event.key
                    count+=1
                print("KEY: ", pygame.key.name(event.key).upper(), " Grid coordinates: ", row, column)
            
    scr.fill(black)
    for row in range(10):
        for column in range(11):
            color = white
            #如果格線陣列欄位等於1，顯示文字，背景為黃色
            if grid[row][column] == 1:
                
                color = yellow
                pygame.draw.rect(scr,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN*10,
                              (MARGIN + HEIGHT) * row + MARGIN*8,
                              WIDTH,
                              HEIGHT],0,9)
                
                text=textarr[row][column]
                show_text(scr, ((MARGIN + WIDTH) * column + MARGIN*10 + text_margin -2,(MARGIN + HEIGHT) * row + MARGIN*8 - text_margin), text, (0, 128, 255),FONTSIZE, True, False)
                
            #如果格線陣列欄位不等於1，顯示灰色方塊      
            if grid[row][column] != 1:
              color = gray
              pygame.draw.rect(scr,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN*10,
                              (MARGIN + HEIGHT) * row + MARGIN*8,
                              WIDTH,
                              HEIGHT],0,9)
              title=titlearr[row][column]
              show_text(scr, ((MARGIN + WIDTH) * column + MARGIN*11,(MARGIN + HEIGHT) * row + MARGIN*8 - text_margin), title, red, FONTSIZE, True)
              
            #如果初始方塊不等於0，顯示紅色方塊
            if start[row][column] != "0":
              color = red
              pygame.draw.rect(scr,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN*10,
                              (MARGIN + HEIGHT) * row + MARGIN*8,
                              WIDTH,
                              HEIGHT],0,9)
        
    #hint_img = pygame.image.load(chap+".jpg") # 提示圖片
    #scr.blit(hint_img, (1110, MARGIN*7)) # 繪製提示圖片
    # 顯示提示文字
    n_hint_rows = int(len(hint)/10) + int(len(hint)%10 != 0)
    for i in range(n_hint_rows):
        show_text(scr, (1200,500+i*90), hint[i*10:(i+1)*10], (255, 255, 255), hint_size, True, False)
    clock.tick(50)
    pygame.display.flip()
pygame.quit()
