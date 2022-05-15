#==================================================================================#
# 九宮格遊戲(v6):                                                                   #
# 新增 (1)答錯刪除記號，(2)按錯還原功能。 (111/3/19, Wen-Bing Horng, TKU)            #
#      (3)調整九宮個寬度，(4)載入題類圖片。   (111/4/23)                             #
#      (5)調整字體大小(font_size)為48，並改進顯示答案需要斷行的需求。 (111/5/2)        #
#==================================================================================#
import pygame

# 全域變數(Global Variables)
black = (0, 0, 0) #縫隙
white = (255, 255, 255)#方塊顏色
red = (251, 75, 78)#線的顏色
yellow = (251, 255, 18)
deep_blue = (0, 0, 255)#選項藍色
team1 = (251, 75, 78)#隊伍紅色
team2 = (0, 126, 167)#隊伍藍色
window_size = [1920, 1080]

WIDTH  = 620
HEIGHT = 340
MARGIN = 30
win_width  = 1920
win_height = 1080
x_offset = int((win_width - (WIDTH*3 + MARGIN*2)) / 2)
y_offset = int((win_height - (HEIGHT*3 + MARGIN*2)) / 2)

state       = [] # 目前狀態 (0:題類，1:題目，2:選項，3:正確，4:錯誤，5:結束)
category    = [] # 題類
problem     = [] # 題目
answer      = [] # 答案選項
result      = [] # 結果(R:紅，B:藍)
selected    = [] # 已選擇題號
correct_ans = [] # 正確的答案選項
wrong_ans   = [] # 答錯的答案選項歷史紀錄
state_hist  = [] # 狀態歷史紀錄
grid_index  = [] # 九宮格題號索引(column, row)
image_name  = [] # 圖片名稱

#------------------------------------------------------------------------------
# 顯示文字，並傳回 text 的 (width, height)
#------------------------------------------------------------------------------
def show_text(surface_handle, pos, text, color, font_size, font_bold=True, font_italic=False):
    # cur_font = pygame.font.SysFont('宋體', font_size) # 獲取系統字型
    cur_font = pygame.font.Font('./TWSung.otf', font_size) # 獲取字型，並設定大小
    cur_font.set_bold(font_bold)               # 設定是否加粗
    cur_font.set_italic(font_italic)           # 設定是否斜體
    text_fmt = cur_font.render(text, 1, color) # 設定文字內容
    surface_handle.blit(text_fmt, pos)         # 繪製文字
    size = cur_font.size(text)                 # (width, height)
    return size

#------------------------------------------------------------------------------
# 顯示答案選項
#------------------------------------------------------------------------------
def show_answer(screen, text, x, y, wrong_ans=[], font_size=48):
    # 初始位置
    x = x + 0.5*font_size
    y = y + 0.5*font_size
    chars_line = 13 # 每行 13 個字，包含(n)序號 3 個符號
    for i in range(4):
        if len(text[i]) <= chars_line: # 若答案 <= 13 個字
            w, h = show_text(screen, (x, y), text[i], deep_blue, font_size = 48)
            if i in wrong_ans:
                pygame.draw.line(screen, (255,0,0), (x,y+h/2), (x+w,y+h/2), 5)
            y += font_size+10
        else: # 答案 > 13 個字，假設最多只有兩行
            # 第一行答案
            n = chars_line
            t1 = text[i][:n]
            w, h = show_text(screen, (x, y), t1, deep_blue, font_size = 48)
            if i in wrong_ans:
                pygame.draw.line(screen, (255,0,0), (x,y+h/2), (x+w,y+h/2), 5)
            y += font_size+10
            # 第二行答案
            t2 = text[i][n:]
            x2 = x + 65
            w, h = show_text(screen, (x2, y), t2, deep_blue, font_size = 48)
            if i in wrong_ans:
                pygame.draw.line(screen, (255,0,0), (x2,y+h/2), (x2+w,y+h/2), 5)
            y += font_size+10

#------------------------------------------------------------------------------
# 顯示正確答案
#------------------------------------------------------------------------------
def show_correct(screen, text, x, y, correct, font_size=48):
    chars_line = 13 # 每行 13 個字，包含(n)序號 3 個符號
    m = 0 # 累計正確答案前面行數
    for i in range(correct):
        if len(text[i]) <= chars_line:
            m += 1
        else:
            m += 2
    # 第一行答案
    n = chars_line
    t1 = text[correct][:n]
    x = x + 0.5*font_size
    y = y + 0.5*font_size + m*(font_size+10)
    show_text(screen, (x, y), t1, (255,0,0), font_size = 48)
    y += font_size+10
    # 第二行答案
    t2 = text[correct][n:]
    x2 = x + 65
    show_text(screen, (x2, y), t2, (255,0,0), font_size = 48)
    
#------------------------------------------------------------------------------
# 畫九宮格
#------------------------------------------------------------------------------
def draw_grid(screen, color):
    # (1) 將螢幕變黑
    screen.fill(black)
    # (2) 重畫九宮格
    for row in range(3):
        for column in range(3):
            x = x_offset + (WIDTH + MARGIN) * column
            y = y_offset + (HEIGHT + MARGIN) * row
            pygame.draw.rect(screen, color, [x, y, WIDTH, HEIGHT])
            
            # 顯示題類: 0
            if state[row][column] == 0:
                file = "images\\" + image_name[row][column]
                image = pygame.image.load(file)
                image.convert()
                screen.blit(image, (x, y))
            
            # 顯示題目: 1
            elif state[row][column] == 1:
                font_size = 48
                n_chars = 12  # chars/line: 每行顯示字元數
                text = problem[row][column]
                n_rows = int(len(text) / n_chars) + 1
                for i in range(n_rows):
                    x1 = x + 0.5*font_size
                    y1 = y + 0.5*font_size + i*(font_size+10)
                    text1 = text[i*n_chars:(i+1)*n_chars]
                    show_text(screen, (x1, y1), text1, deep_blue, font_size=font_size)
            
            # 顯示答案選項: 2
            elif state[row][column] == 2:
                text = answer[row][column]
                wrong = wrong_ans[row][column]
                show_answer(screen, text, x, y, wrong)
            
            # 顯示正確選項: 3
            elif state[row][column] == 3:
                text = answer[row][column]
                wrong = wrong_ans[row][column]
                show_answer(screen, text, x, y, wrong)
                correct = correct_ans[row][column]
                show_correct(screen, text, x, y, correct)
            
            # 顯示錯誤選項: 4
            elif state[row][column] == 4:
                text = answer[row][column]
                wrong = wrong_ans[row][column]
                print('wrong:', wrong)
                show_answer(screen, text, x, y, wrong)
            
            # 顯示結果(獲勝隊伍顏色): 5
            elif state[row][column] == 5:
                color_type = result[row][column]
                color1 = team1 if color_type == 'R' else team2
                pygame.draw.rect(screen, color1, [x, y, WIDTH, HEIGHT])

#------------------------------------------------------------------------------
# 找出題號 n 所對應的九宮格索引
#------------------------------------------------------------------------------
def find_grid_index(n, grid_index):
    for item in grid_index:
        num, column, row = item
        if n == num: 
            break
    return column, row
    
# ----- main() ----------------------------------------------------------------
# 啟動 pygame
pygame.init()

# 建立繪圖視窗做為圖形顯示區域
window_size = [1920, 1080]
screen = pygame.display.set_mode(window_size)

# 設定視窗標題
pygame.display.set_caption("Grid")

# 建立畫布
background = pygame.Surface(screen.get_size())

# 建立畫布副本 加速顯示
background = background.convert()

# 將畫布填滿顏色(黑色)
background.fill(black)

# 將畫布繪製於視窗中 從(0,0)開始繪製
screen.blit(background, (0,0))

# 建立空串列: 題類(category)、題目(problem)、選項(answer)、結果(result)
for row in range(3):
    category.append([])
    problem.append([])
    answer.append([])
    result.append([])
    state.append([])
    wrong_ans.append([])
    correct_ans.append([])
    state_hist.append([])
    for column in range(3):
        category[row].append("0") 
        problem[row].append("0")
        answer[row].append("0")
        result[row].append("0")
        state[row].append(0)       # 初始狀態=0
        correct_ans[row].append(0) # 正確答案
        wrong_ans[row].append([])  # 錯誤選項歷史紀錄
        state_hist[row].append([0]) # 狀態歷史紀錄

# 讀取題目檔案與解析
file = open("topic(v1).txt", "r", encoding="utf-8")
all_data = file.readlines()
for line in all_data:
    arr = line.split('&')       # 以 '&' 字元分割字串: 題號[0]&題目類別[1]&col[2]&row[3]&題目[4]
    column = int(arr[2])-1                # arr[2]: col
    row = int(arr[3])-1                   # arr[3]: row
    category[row][column] = arr[1]        # arr[1]: 題目類別
    problem[row][column] = arr[4].strip() # arr[4]: 題目
    answer[row][column] = arr[5:9]        # arr[5:10]: 答案選項
    grid_index.append([arr[0], column, row])      # 九宮格的索引
    correct_ans[row][column] = int(arr[9][0]) - 1 # 正確的答案選項

image_name = [['Left-1.jpg', 'Center-1.jpg', 'Right-1.jpg'],
              ['Left-2.jpg', 'Center-2.jpg', 'Right-2.jpg'],
              ['Left-3.jpg', 'Center-3.jpg', 'Right-3.jpg']]

#在完成操作後要將檔案關閉
file.close()

draw_grid(screen, white)

# 更新視窗 才能顯示繪製圖形
pygame.display.update()

done = False
clock = pygame.time.Clock()  # 建立時間元件

problem_end = True

while not done:
    clock.tick(30)  # 每秒執行30次
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 點選標題列(Title Bar)右上角的 "X" 關閉時窗按鈕，則結束
            done = True 
        elif event.type == pygame.KEYDOWN:   # 鍵盤事件: 鍵盤被按下
            print('event.key:', event.key)
            print('pygame.key.name():', pygame.key.name(event.key))
            print('type:', type(event.key))
            if event.key == pygame.K_ESCAPE: # 按下 "Esc" 鍵，則結束
                done = True
            else:
                keyname = pygame.key.name(event.key)
                if keyname[0] == '[':  # 右邊數字鍵盤
                    key = keyname[1]   # 取出所按的鍵(str)
                    print('key:', key)
                    if ord('1') <= ord(key) <= ord('9'): # 按鍵為 '1' ~ '9'
                        if key in selected: # 所選題目已選過，則跳過不管
                            continue
                        column, row = find_grid_index(key, grid_index) # 找出對應的 column, row
                        current_state = state[row][column]
                        if current_state == 0 and problem_end == True:   # 0: 顯示題類
                            selected.append(key) # 將所選題目加入已選題中
                            print('after append(), selected:', selected)
                            current_select = key # 設定目前所選題號
                            next_state = 1       # 顯示題目
                            state[row][column] = next_state
                            state_hist[row][column].append(next_state)
                            draw_grid(screen, white)
                            problem_end = False
                elif event.key == pygame.K_UP: # 按下"向上鍵"，則復原前一個動作
                    current_state = state[row][column]
                    print("current state (UP):", current_state)
                    if current_state == 1: # 1: 顯示題類
                        state_hist[row][column].pop()
                        prev_state = state_hist[row][column][-1] # 取出上一個狀態
                        state[row][column] = prev_state
                        draw_grid(screen, white)
                        print('before pop(), selected:', selected)
                        selected.pop()
                        problem_end = True
                    elif current_state == 2: # 2: 顯示答案選項
                        state_hist[row][column].pop()
                        prev_state = state_hist[row][column][-1] # 取出上一個狀態
                        state[row][column] = prev_state
                        draw_grid(screen, white)
                    elif current_state == 3: # 3: 選擇正確答案
                        state_hist[row][column].pop()
                        prev_state = state_hist[row][column][-1] # 取出上一個狀態
                        state[row][column] = prev_state
                        draw_grid(screen, white)
                    elif current_state == 4: # 4: 選擇錯誤答案
                        wrong_ans[row][column].pop()
                        state_hist[row][column].pop()
                        prev_state = state_hist[row][column][-1] # 取出上一個狀態
                        state[row][column] = prev_state
                        draw_grid(screen, white)
                    elif current_state == 5: # 5: 獲勝隊伍顏色
                        print("before pop(), state_hist:", state_hist[row][column])
                        state_hist[row][column].pop()
                        prev_state = state_hist[row][column][-1] # 取出上一個狀態
                        state[row][column] = prev_state
                        draw_grid(screen, white)
                        problem_end = False
                elif event.key == pygame.K_DOWN: # 按下"向下鍵"，則顯示答案選項
                    current_state = state[row][column]
                    if current_state == 1: # 1: 顯示題類
                        next_state = 2 # 2: 顯示答案選項
                        state[row][column] = next_state
                        state_hist[row][column].append(next_state)
                        draw_grid(screen, white)
                elif event.key == pygame.K_LEFT: # 按下"向左鍵"，則顯示結果(紅色)
                    current_state = state[row][column]
                    if current_state == 3: # 3: 選擇正確答案
                        next_state = 5 # 5: 顯示獲勝隊伍顏色
                        state[row][column] = next_state
                        state_hist[row][column].append(next_state)
                        result[row][column] = 'R'
                        draw_grid(screen, white)
                        problem_end = True
                elif event.key == pygame.K_RIGHT: # 按下"向右鍵"，則顯示結果(藍色)
                    current_state = state[row][column]
                    if current_state == 3: # 選擇正確答案
                        next_state = 5 # 顯示獲勝隊伍顏色
                        state[row][column] = next_state
                        state_hist[row][column].append(next_state)
                        result[row][column] = 'B'
                        draw_grid(screen, white)
                        problem_end = True
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]: # '1'~'4': 答案選項
                    current_state = state[row][column]
                    if current_state in [2, 4]: # 答題中
                        print('correct:', correct_ans[row][column])
                        choice = event.key - ord('1')
                        print('choice:', choice)
                        if choice != correct_ans[row][column]: # 選擇錯誤
                            wrong_ans[row][column].append(choice) # 增加至錯誤選擇串列
                            next_state = 4 # 4: 顯示錯誤選項
                            state[row][column] = next_state
                            state_hist[row][column].append(next_state)
                            draw_grid(screen, white)
                        else: # 選擇正確
                            next_state = 3 # 3: 顯示正確選項
                            state[row][column] = next_state 
                            state_hist[row][column].append(next_state)
                            draw_grid(screen, white)

    # 更新視窗(與pygame.display.update()相同)
    pygame.display.flip()
pygame.quit()
