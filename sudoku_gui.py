import pygame, time
pygame.font.init()

class Grid():

    board = [
        [0,0,0,8,0,1,0,6,0],
        [1,0,4,0,0,2,8,5,0],
        [0,0,0,6,0,0,7,0,1],
        [0,0,0,0,9,0,6,0,0],
        [0,0,9,5,0,6,1,0,0],
        [0,0,7,0,2,0,0,0,0],
        [9,0,2,0,0,5,0,0,0],
        [0,4,5,3,0,0,2,0,9],
        [0,3,0,2,0,9,0,0,0]
        ]

    def __init__(self, rows, cols, width, height, screen):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.screen = screen

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, value):
        row, col = self.selected # this is going to cause problems
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(value)
            self.update_model()

            if valid(self.model, value, (row, col)) and self.solve():# line has the wrong parameters
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self,value):
        row, col = self.selected
        self.cubes[row][col].set_temp(value)

    def draw(self):
        # Draw grid lines 
        gap = self.width / 9
        for i in range(1,self.rows + 1):
            if i % 3 == 0:
                thick = 4
            else:
                thick =1
            pygame.draw.line(self.screen, (0,0,0), (0, i *gap), (self.width, i *gap), thick)
            pygame.draw.line(self.screen, (0,0,0), (i *gap,0), (i *gap, self.height), thick)
        
        # Draw cubes 
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.screen)
         
    def select(self, row, col):
        # reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        
        self.cubes[row][col].selected = True
        self.selected = (row,col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        # input a position, output a (row,col)
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        # else:
        #     return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    
    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if valid(self.model, i, (row,col)):
                self.model[row][col] = i
                if self.solve():
                    return True
                self.model[row][col] = 0
        return False

    def solve_gui(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if valid(self.model, i, (row,col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.screen, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(1)
                
                if self.solve_gui():
                    return True
                
                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.screen, False)
                pygame.display.update()
                pygame.time.delay(1)
        
        return False


class Cube():
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    
    def draw(self, screen):
        fnt = pygame.font.SysFont('comicsans', 40)

        gap = self.width/9
        x = self.col *gap
        y = self.row *gap 

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            screen.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value),1,(0,0,0))
            screen.blit(text, (x+((gap - text.get_width())/2), y +((gap - text.get_height())/2)))
        
        if self.selected:
            pygame.draw.rect(screen, (255,0,0), (x,y,gap,gap),3)
    
    def draw_change(self, screen, draw):
        fnt = pygame.font.SysFont('comicsans', 40)
        gap = self.width/9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(screen, (255,255,255), (x,y,gap,gap), 0)
        text = fnt.render(str(self.value), 1, (0,0,0))
        screen.blit(text, (x + (gap-text.get_width())/2, y + ((gap - text.get_height())/2)))

        if draw:
            pygame.draw.rect(screen, (0,255,0), (x,y,gap,gap), 3)
        else:
            pygame.draw.rect(screen, (255,0,0), (x,y,gap,gap), 3)


    def set(self, val):
        self.value = val
    
    def set_temp(self, val):
        self.temp = val

def redraw_screen(screen, board, time, strikes):
    screen.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont('comicsans', 40)
    text = fnt.render('Time: ' + format_time(time), 1, (0,0,0))
    screen.blit(text, (380,560))
    # Draw strikes
    text = fnt.render('X '* strikes, 1,(255,0,0))
    screen.blit(text, (20, 560))
    # Draw grid and board
    board.draw()

def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60
    if len(str(minute)) == 1 and len(str(sec))==1:
        return '0'+ str(minute)+':0'+str(sec)
    elif len(str(minute)) == 1:
        return '0'+str(minute)+':'+str(sec)
    else:
        return ' '+str(minute)+':'+str(sec)


def valid(board, num, pos):
    # check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    
    # check col
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    
    # check box
    box_x = pos[1]//3
    box_y = pos[0]//3

    for i in range(box_y*3, box_y*3 +3):
        for j in range(box_x * 3, box_x *3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
    
    return True

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i,j)
    #return None

def main():
    screen = pygame.display.set_mode((540, 600))
    pygame.display.set_caption('Sudoku')
    board = Grid(9,9,540,540, screen)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:

        play_time= round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                    key =1
                if event.key == pygame.K_KP2 or event.key == pygame.K_2:
                    key =2
                if event.key == pygame.K_KP3 or event.key == pygame.K_3:
                    key =3
                if event.key == pygame.K_KP4 or event.key == pygame.K_4:
                    key =4
                if event.key == pygame.K_KP5 or event.key == pygame.K_5:
                    key =5
                if event.key == pygame.K_KP6 or event.key == pygame.K_6:
                    key =6
                if event.key == pygame.K_KP7 or event.key == pygame.K_7:
                    key =7
                if event.key == pygame.K_KP8 or event.key == pygame.K_8:
                    key =8
                if event.key == pygame.K_KP9 or event.key == pygame.K_9:
                    key =9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None 
                if event.key == pygame.K_INSERT:
                    board.solve_gui()
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    i,j = board.selected
                    if board.cubes[i][j].temp != 0:
                        print('Success!')
                    elif board.cubes[i][j].temp == 0:
                        continue
                    else:
                        print('Wrong')
                        strikes += 1
                    key = None

                    if board.is_finished():
                        print('Game over')
                        run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
        
        if board.selected and key != None:
            board.sketch(key)
        
        redraw_screen(screen, board, play_time, strikes)
        pygame.display.update()

def possible(i,j,z):
    '''
    i is an integer (x value?)
    j is an integer (y value?)
    z is the chosen integer
    '''
    #if board.shape!=(9,9):  checks the dimensions of the board are correct
        #raise(Exception("Sudokumatrix not valid"));
    global board
    if 8 < i < 0:
        raise(Exception("i not valid"));
    if 8 < j < 0:
        raise(Exception("j not valid"));
    if 9 < z < 1:
        raise(Exception("z not valid"));

    if(board[i][j]!=0):
        return False;

    for x in range(0,9):
        if(board[x][j]==z):
            return False;

    for y in range(0,9):
        if(board[i][y]==z):
            return False;

    row = int(i/3) * 3;
    col = int(j/3) * 3;
    for ii in range(0,3):
        for jj in range(0,3):
            if(board[ii+row][jj+col]==z):
                return False;

    return True;

def print_board(board):
    '''
    prints the board
    :param board: 2d list of integers
    :return: None
    '''
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print('-----------------------')
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(' | ', end= '')

            if j == 8:
                print(board[i][j], end = '\n')
            else:
                print(str(board[i][j]) + ' ', end = '')

def possibleNums(i ,j):
    '''
    returns a list of numbers that could go in board[i][j]
    '''
    potential = []
    ind = 0
    for k in range(1,10):
        if possible(i,j,k):
            potential.insert(ind,k)
            ind+=1
    return potential

def solve(board):
    zeroFound = 0;
    for i in range(9):
        for j in range(9):
            if(board[i][j]==0):
                zeroFound=1;
                break;
        if(zeroFound==1):
            break;
    if(zeroFound==0):
        print("The solution I came up with: ")
        empty = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
        ]
        for x in range(9):
            for y in range(9):
                empty[x][y] = board[x][y]
        print_board(empty)
        return empty


    a_list = possibleNums(i,j)

    for k in range(len(a_list)):
        board[i][j]=a_list[k]
        solve(board)
    board[i][j] = 0

main()
pygame.quit()
