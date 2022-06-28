# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:42:48 2022

@author: ASUS
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
LARGE_FONT = ("Verdana", 12)
from PIL import ImageGrab
glob_clicks=[]

class Rectangle(tk.Tk):

    def __init__(self, height = 800, width = 800, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tkcontainer = tk.Frame(self)
        tkcontainer.pack(side="top", fill="both", expand=True)
        tkcontainer.grid_rowconfigure(0, weight = 1)
        tkcontainer.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        frame = CanvasPage(tkcontainer, self, height, width)
        self.frames[CanvasPage] = frame
        frame.grid(row=0, column = 0, sticky="nsew")
        self.show_frame(CanvasPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise() 

class CanvasPage(tk.Frame):

    def __init__(self, parent, controller, height, width):
        tk.Frame.__init__(self, parent)
        self.height = height
        self.width = width
        self.clicks = []
        global glob_clicks
        glob_clicks=self.clicks
        self.kx1=0
        self.ky1=0
        self.angle=0
        self.color="white"
        self.kx2=0
        self.ky2=0
        label = tk.Label(self, text="Rectangle", font=LARGE_FONT)
        #label.pack(pady =10,padx=10)
        self.angle_entry = tk.Entry(self,textvariable = self.angle, font=('calibre',10,'normal'))
        sub_btn=tk.Button(self,text = 'Rotate', command = self.rotate)
        label.pack()
        self.angle_entry.pack()
        sub_btn.pack()
        self.canvas = tk.Canvas(height=self.height, width=self.width, bg='white')
        self.canvas.create_line(0, self.height/2, self.width, self.height/2)
        self.canvas.create_line(self.width/2, 0, self.width/2, self.height)
        self.make_axes(self.canvas, self.height, self.width)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.shift_click_bind = self.canvas.bind("<Shift-Button-1>", self.shift_rect)
        self.shift_click_bind_release = self.canvas.bind("<Shift-ButtonRelease-1>", self.shift_rect_draw)
        #self.left_click_bind = self.canvas.bind("<Button-1>", self.show_point)
        #self.right_click_bind = self.canvas.bind("<Button-3>", self.make_polygon)
        buttonBG = self.canvas.create_rectangle(450, 0, 550, 30, fill="grey40", outline="grey60")
        
        buttonRED = self.canvas.create_rectangle(595, 0, 625, 30, fill="red", outline="grey60")
        buttonBLUE = self.canvas.create_rectangle(700, 0, 730, 30, fill="blue", outline="grey60")
        buttonYELLOW = self.canvas.create_rectangle(735, 0, 765, 30, fill="yellow", outline="grey60")
        buttonGREEN = self.canvas.create_rectangle(665, 0, 695, 30, fill="green", outline="grey60")
        buttonWHITE = self.canvas.create_rectangle(630, 0, 660, 30, fill="white", outline="grey60")
        
        buttonTXT = self.canvas.create_text(500, 15, text="SAVE")
        self.canvas.tag_bind(buttonBG, "<Button-1>", self.save_img) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonTXT, "<Button-1>", self.save_img) ## same, but for the text. 
        
        self.canvas.tag_bind(buttonRED, "<Button-1>", self.color_red) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonBLUE, "<Button-1>", self.color_blue) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonYELLOW, "<Button-1>", self.color_yellow) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonGREEN, "<Button-1>", self.color_green) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonWHITE, "<Button-1>", self.color_white) ## when the square is clicked runs function "clicked".
        
        self.fresh()
        
    def fresh(self):
        self.canvas.delete("all")
        self.canvas.create_line(0, self.height/2, self.width, self.height/2)
        self.canvas.create_line(self.width/2, 0, self.width/2, self.height)
        self.make_axes(self.canvas, self.height, self.width)
        buttonBG = self.canvas.create_rectangle(450, 0, 550, 30, fill="grey40", outline="grey60")
        buttonTXT = self.canvas.create_text(500, 15, text="SAVE")
        
        self.canvas.tag_bind(buttonBG, "<Button-1>", self.save_img) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonTXT, "<Button-1>", self.save_img) ## same, but for the text. 
        
        
        
        buttonRED = self.canvas.create_rectangle(595, 0, 625, 30, fill="red", outline="grey60")
        buttonBLUE = self.canvas.create_rectangle(700, 0, 730, 30, fill="blue", outline="grey60")
        buttonYELLOW = self.canvas.create_rectangle(735, 0, 765, 30, fill="yellow", outline="grey60")
        buttonGREEN = self.canvas.create_rectangle(665, 0, 695, 30, fill="green", outline="grey60")
        buttonWHITE = self.canvas.create_rectangle(630, 0, 660, 30, fill="white", outline="grey60")
        
        
        self.canvas.tag_bind(buttonRED, "<Button-1>", self.color_red) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonBLUE, "<Button-1>", self.color_blue) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonYELLOW, "<Button-1>", self.color_yellow) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonGREEN, "<Button-1>", self.color_green) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonWHITE, "<Button-1>", self.color_white) ## when the square is clicked runs function "clicked".
        
    def color_red(self,event):
        self.color="red"
    
    def color_blue(self,event):
        self.color="blue"
    
    def color_yellow(self,event):
        self.color="yellow"
    
    def color_green(self,event):
        self.color="green"
    
    def color_white(self,event):
        self.color="white"
        
        
    def make_axes(self, canvas, height, width):
        for i in range(0, width//2, 50):
            #Negative X-axis
            canvas.create_line(i, height//2, i, height//2+3)
            canvas.create_text(i, height/2+10,fill="black",font="Times 10", text=str(-(width//2 - i)))

            #Positive X-axis
            canvas.create_line(i+width//2, height//2, i+width//2, height//2+3)
            canvas.create_text(i+width//2, height/2+10,fill="black",font="Times 10", text=str((i)))

        for i in range(50, height//2, 50):
            #Positive Y-axis
            canvas.create_line(width//2, i, width//2-5, i)
            canvas.create_text(width//2-17, i, fill="black",font="Times 10", text=str((height//2 - i)))

            #Negative Y-axis
            canvas.create_line(width//2, i+height//2, width//2-5, i+height//2)        
            canvas.create_text(width//2-17, i+height//2, fill="black",font="Times 10", text=str(-(height//2 - i)))    

    def shift_rect(self,event):
        #self.canvas.unbind("<Shift-Button-1>", self.shift_click_bind)
        self.fresh()
        self.clicks=[]
        self.clicks.append((event.x - 1, event.y - 1))
    
    def points(self):
        for i in self.clicks:
            self.canvas.create_oval(i[0]-2, i[1]-2, i[0]+2, i[1]+2, fill="")
            pt = (i[0]-self.width//2, i[1]-self.height//2)
            self.canvas.create_text(round(i[0]-4,1), round(i[1]-10,1), fill="black", font="Times 10", text="("+str(round(pt[0],1))+", "+str(round(pt[1],1))+")")
        
    def shift_rect_draw(self,event):
        #self.canvas.unbind("<Shift-ButtonRelease-1>", self.shift_click_bind_release)
        self.clicks.append((event.x - 1, event.y - 1))
        #print(self.clicks)
        #self.canvas.create_rectangle(self.clicks,outline ="black",width = 2)
        self.poly = Polygon(self.canvas,self.clicks,self.color)
        x1=self.clicks[0]
        x4=self.clicks[1]
        x2=[x4[0],x1[1]]
        x3=[x1[0],x4[1]]
        self.clicks=[x1,x3,x4,x2]
        
        self.points()
            
        print(self.clicks)
        self.poly = Polygon(self.canvas,self.clicks,self.color)
        self.poly.generate_polygon()        
       
        self.canvas.bind("<B1-Motion>", self.motion)
        self.canvas.bind("<Double-Button-1>", self.scale)
        #self.canvas.bind("<Double-Button-2>", self.scale_d)
        self.canvas.bind("<Shift-Up>", self.scale_d)
        #self.canvas.bind("<KeyRelease>", self.sacle_d)
        # Check if b was pressed
        
        #self.transformation_input()
        
    def motion(self,event):
        print("Mouse position: (%s %s)" % (event.x, event.y))
        self.fresh()
        x_i=self.clicks[0][0]-event.x
        y_i=-self.clicks[0][1]+event.y
        print(x_i)
        print(y_i)
        self.poly.translate_poly(-x_i/300,y_i/300)
        global glob_clicks
        self.clicks=glob_clicks
        self.points()
        
    def save_img(self,event):
        self.canvas.postscript(file = 'rectangle.eps') 
        # use PIL to convert to PNG 
        #img = Image.open('rectangle.eps') 
        #img.save('rectangle.png', 'png') 
        x=self.winfo_rootx()+50
        y=self.winfo_rooty()
        x1=x+self.canvas.winfo_width()
        y1=y+self.canvas.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save("rect.png")
        
    
    
    def scale(self,event):
        self.fresh()
        val=0.5
        #lst = list(map(float,input("Enter the x and y scaling factors you desire: ").split()))
        self.poly.scale_poly(val,val, self.height/2, self.width/2)
        global glob_clicks
        self.clicks=glob_clicks
        self.points()
        
    def scale_d(self,event):
        self.fresh()
        val=0.5
        #lst = list(map(float,input("Enter the x and y scaling factors you desire: ").split()))
        self.poly.scale_poly(val,val, self.height/2, self.width/2)
        global glob_clicks
        self.clicks=glob_clicks    
        self.points()
        print("i'/")

    def rotate(self):
        self.fresh()
        print("HELLOOLD")
        print(self.clicks)
        self.angle=self.angle_entry.get()
        #angle = float(input("Please provide the angle of rotation: "))
        self.angle = float(self.angle)*np.pi/180
        self.poly.rotate_poly(self.angle, self.height/2, self.width/2)
        global glob_clicks
        self.clicks=glob_clicks
        print("HELLO")
        print(self.clicks)
        self.points()
        
class Polygon(tk.Canvas):
    def __init__(self, canvas, vertices,color):
        self.vertices = vertices
        self.canvas = canvas
        self.color = color 
        
    def generate_polygon(self):
        #self.canvas.delete("all")
        #buttonBG = self.canvas.create_rectangle(700, 0, 800, 30, fill="grey40", outline="grey60")
        #buttonTXT = self.canvas.create_text(750, 15, text="SAVE")
        return self.canvas.create_polygon(self.vertices, outline = "black", fill=str(self.color),width=2)
        
    def add_vertex(self,vertex):
        self.vertices.append(vertex)

    def add_vertices(self,vertices):
        self.vertices.append(vertices)

    def get_vertices(self):
        return self.vertices   

    def translate_poly(self,tx,ty):
        trans = np.asarray([[1, 0, tx],
                        [0, 1, -ty,],
                        [0, 0, 1]])

        lst = []
        for stuff in self.vertices:
            lst.append([stuff[0],stuff[1],1])

        m_vertices  = np.transpose(np.asarray(lst))

        output_matrix = np.transpose(trans.dot(m_vertices))

        lst = []
        for stuff in output_matrix:
            lst.append((stuff[0], stuff[1]))

        self.vertices = lst
        global glob_clicks
        glob_clicks=self.vertices
        self.generate_polygon()

    def rotate_poly(self, theta, xr, yr):
        print(xr,yr)
        xr = self.vertices[0][0]
        yr = self.vertices[0][1]
        rotation = np.asarray([[np.cos(theta), -np.sin(theta), xr*(1-np.cos(theta)) + yr*np.sin(theta) ],
                            [np.sin(theta), np.cos(theta), yr*(1-np.cos(theta)) - xr*np.sin(theta)],
                            [0, 0, 1]])

        lst = []
        for stuff in self.vertices:
            lst.append([stuff[0],stuff[1],1])
        print(self.vertices)
        m_vertices  = np.transpose(np.asarray(lst))

        output_matrix = np.transpose(rotation.dot(m_vertices))

        lst = []
        for stuff in output_matrix:
            lst.append((stuff[0], stuff[1]))

        self.vertices = lst
        print(self.vertices)
        global glob_clicks
        glob_clicks=self.vertices
        self.generate_polygon()
    
    def scale_poly(self,sx, sy, xr, yr):
        xr = self.vertices[0][0]
        yr = self.vertices[0][1]

        scale = np.asarray([[sx, 0, xr*(1-sx)],
                        [0, sy, yr*(1-sy)],
                        [0, 0, 1]])
        
        lst = []
        for stuff in self.vertices:
            lst.append([stuff[0],stuff[1],1])
        print(self.vertices)
        m_vertices  = np.transpose(np.asarray(lst))

        output_matrix = np.transpose(scale.dot(m_vertices))

        lst = []
        for stuff in output_matrix:
            lst.append((stuff[0], stuff[1]))

        self.vertices = lst
        print(self.vertices)
        global glob_clicks
        glob_clicks=self.vertices
        self.generate_polygon()


app = Rectangle(height= 800, width = 800)
app.mainloop()