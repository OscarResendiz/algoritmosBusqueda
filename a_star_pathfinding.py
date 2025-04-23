import tkinter as tk
from queue import PriorityQueue, Queue

ROWS=20
COLS=20
CELL_SIZE=30

class Cell:
    def __init__(self,row,col):
         self.row=row
         self.col=col
         self.is_start=False
         self.is_end=False
         self.is_wall=False
         self.color="white"

    def draw(self,canvas):
          x1=self.col * CELL_SIZE
          y1=self.row * CELL_SIZE
          x2=x1 + CELL_SIZE
          y2=y1 + CELL_SIZE
          canvas.create_rectangle(x1,y1,x2,y2,fill=self.color, outline="gray")

    def __lt__(self,other):
          return False


def create_grid():
     return[[Cell(r,c) for c  in range (COLS)] for r in range(ROWS)]

def draw_grid(canvas,grid):
    canvas.delete("all")
    for row in grid:
        for cell in row:
            cell.draw(canvas)

def get_cell(event):
    row=event.y // CELL_SIZE
    col=event.x // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return grid[row] [col]
    return None

def clear_paths():
     for row in grid:
         for cell in row:
              if not (cell.is_start or cell.is_end or cell.is_wall):
                  cell.color="white"

def on_click(event):
    global start_cell, end_cell
    cell= get_cell(event)
    if cell:
        if not start_cell and not cell.is_wall:
             cell.is_start=True
             cell.color="green"
             start_cell=cell
        elif  not end_cell and not cell.is_wall and cell != start_cell:
              cell.is_end= True
              cell.color="red"
              end_cell=cell
        elif cell !=start_cell and cell != end_cell:
             cell.is_wall= not cell.is_wall
             cell.color="black" if cell.is_wall else "white"
        clear_paths()    #Limpiar caminos al cambiar obstáculos                
        draw_grid(canvas,grid)

def h(a,b):
    return abs(a.row -b.row) + abs(a.col -b.col)

def get_neighbors(cell):
    neighbors=[]
    for dr, dc in [(-1,0), (1,0),(0,-1),(0,1)]:
        r,c=cell.row + dr, cell.col + dc
        if 0<=r < ROWS and 0<= c < COLS:
            neighbor=grid[r][c]
            if  not neighbor.is_wall:
                neighbors.append(neighbor)
    return neighbors

def reconstruct_path(came_from, current,color):
    steps=0
    while current in came_from:
        current=came_from[current]
        if not current.is_start:
            current.color=color
            steps += 1
    return steps

def run_a_start():
    clear_paths()
    open_set=PriorityQueue()
    open_set.put((0,start_cell))
    came_from={}
    g_score={cell: float("inf") for row in grid for cell in row}
    g_score[start_cell]=0
    f_score={cell: float("inf") for row in grid for cell in row}
    f_score[start_cell]=h(start_cell, end_cell)
    open_set_hash={start_cell}
    explored=0
    while not open_set.empty():
        current=open_set.get()[1]
        open_set_hash.remove(current)
        explored +=1
        if current==end_cell:
            steps=reconstruct_path(came_from,end_cell,"lightseagreen")
            draw_grid(canvas,grid)
            stats_astar.config(text=f"A*:Nodos:{explored},Pasos:{steps}")
            return          
        for neighbor in get_neighbors(current):
            tem_g_score=g_score[current] + 1
            if tem_g_score < g_score[neighbor]:
                came_from[neighbor]=current
                g_score[neighbor]=tem_g_score
                f_score[neighbor]=tem_g_score + h(neighbor,end_cell)
                if neighbor not in open_set_hash:
                    tmp=f_score[neighbor]
                    open_set_hash.add(neighbor)
                    open_set.put((tmp,neighbor))

def run_dijkstra():
     clear_paths()
     queue=PriorityQueue()
     queue.put((0,start_cell))
     came_from={}
     distance={cell:float("inf") for row in grid for cell in row}
     distance[start_cell]=0
     visited=set()
     explored=0
     while not queue.empty():
        dist, current=queue.get()
        if current in visited:
            continue
        visited.add(current)
        explored += 1
        if current== end_cell:
            steps=reconstruct_path(came_from, end_cell, "purple")
            draw_grid(canvas,grid)
            stats_dijkstra.config(text=f"Dijkstra:Nodos:{explored}, Pasos:{steps}")
            return            
        for neighbor in get_neighbors(current):
            new_dist=distance[current] + 1
            if new_dist < distance[neighbor]:
                distance[neighbor]=new_dist
                came_from[neighbor]=current
                queue.put((new_dist,neighbor))

def run_bfs():
     clear_paths()
     queue=Queue()
     queue.put(start_cell)
     came_from={}
     visited= set([start_cell])
     explored=0        
     while not queue.empty():
        current=queue.get()
        explored +=1
        if current ==end_cell:
            steps= reconstruct_path(came_from, end_cell,"skyblue")
            draw_grid(canvas,grid)
            stats_bfs.config(text=f"BFS:Nodos:{explored}, Pasos:{steps}")
            return
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
             visited.add(neighbor)
             came_from[neighbor]=current
             queue.put(neighbor)

def reset_grid():       
    global start_cell, end_cell
    start_cell=None
    end_cell=None
    for row in grid:
        for cell in row:
            cell.is_start=False
            cell.is_end=False
            cell.is_wall=False
            cell.color="white"
        draw_grid(canvas,grid)
        stats_astar.config(text="A*: ")
        stats_dijkstra.config(text="Dijksta: ")
        stats_bfs.config(text="BFS: ")

#---------------------------------------------------------------------------------------------------------------------------    


    
        
 #Interfaz Tkinter
root=tk.Tk()
root.title("Comparación de algoritmos")
   
canvas=tk.Canvas(root,width=COLS*CELL_SIZE,height=ROWS*CELL_SIZE)
canvas.pack()

grid= create_grid()
    
    
start_cell=None
end_cell=None

canvas.bind("<Button-1>",on_click)
draw_grid(canvas,grid)

btn_frame=tk.Frame(root)
btn_frame.pack(pady=5)

btn_astar=tk.Button(btn_frame,text="Ejecutar A*",command=run_a_start)
btn_astar.pack(side="left",padx=5)
btn_dijkstra=tk.Button(btn_frame,text="Ejecutar Dijkstra",command=run_dijkstra)
btn_dijkstra.pack(side="left",padx=5)
btn_bfs=tk.Button(btn_frame,text="Ejecutar BFS",command=run_bfs)
btn_bfs.pack(side="left",padx=5)

reset_button=tk.Button(btn_frame,text="Reiniciar",command=reset_grid)
reset_button.pack(side="left",padx=5)

stats_astar=tk.Label(root,text="A*:")
stats_astar.pack()
stats_dijkstra=tk.Label(root,text="Dijkstra:")
stats_dijkstra.pack()
stats_bfs=tk.Label(root,text="BFS:")
stats_bfs.pack()
root.mainloop()



            

        
                
