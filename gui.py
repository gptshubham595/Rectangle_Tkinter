# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:42:48 2022

@author: ASUS
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
LARGE_FONT = ("Verdana", 12)
from PIL import ImageGrab,Image
import keyboard


class TwoDTransformationApp(tk.Tk):

    def __init__(self, height = 800, width = 800, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        frame = StartPage(container, self, height, width)
        self.frames[StartPage] = frame
        frame.grid(row=0, column = 0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise() 

class StartPage(tk.Frame):

    def __init__(self, parent, controller, height, width):
        tk.Frame.__init__(self, parent)
        self.height = height
        self.width = width
        self.clicks = []
        self.kx1=0
        self.ky1=0
        self.angle=0
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
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.shift_click_bind = self.canvas.bind("<Shift-Button-1>", self.shift_rect)
        self.shift_click_bind_release = self.canvas.bind("<Shift-ButtonRelease-1>", self.shift_rect_draw)
        #self.left_click_bind = self.canvas.bind("<Button-1>", self.show_point)
        #self.right_click_bind = self.canvas.bind("<Button-3>", self.make_polygon)
        buttonBG = self.canvas.create_rectangle(700, 0, 800, 30, fill="grey40", outline="grey60")
        buttonTXT = self.canvas.create_text(750, 15, text="SAVE")
        self.canvas.tag_bind(buttonBG, "<Button-1>", self.save_img) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonTXT, "<Button-1>", self.save_img) ## same, but for the text. 
        self.fresh()
        
    def fresh(self):
        self.canvas.delete("all")
        buttonBG = self.canvas.create_rectangle(700, 0, 800, 30, fill="grey40", outline="grey60")
        buttonTXT = self.canvas.create_text(750, 15, text="SAVE")
        self.canvas.tag_bind(buttonBG, "<Button-1>", self.save_img) ## when the square is clicked runs function "clicked".
        self.canvas.tag_bind(buttonTXT, "<Button-1>", self.save_img) ## same, but for the text. 
        
        
    def shift_rect(self,event):
        #self.canvas.unbind("<Shift-Button-1>", self.shift_click_bind)
        self.fresh()
        self.clicks=[]
        self.clicks.append((event.x - 1, event.y - 1))

    def shift_rect_draw(self,event):
        #self.canvas.unbind("<Shift-ButtonRelease-1>", self.shift_click_bind_release)
        self.clicks.append((event.x - 1, event.y - 1))
        #print(self.clicks)
        #self.canvas.create_rectangle(self.clicks,outline ="black",width = 2)
        self.poly = Polygon(self.canvas,self.clicks)
        x1=self.clicks[0]
        x4=self.clicks[1]
        x2=[x4[0],x1[1]]
        x3=[x1[0],x4[1]]
        self.clicks=[x1,x3,x4,x2]
        
        for i in self.clicks:
            self.canvas.create_oval(i[0]-2, i[1]-2, i[0]+2, i[1]+2, fill="")
            pt = (i[0]-self.width//2, i[1]-self.height//2)
            self.canvas.create_text(i[0]-4, i[1]-10, fill="black", font="Times 10", text="("+str(pt[0])+", "+str(pt[1])+")")
            
        print(self.clicks)
        self.poly = Polygon(self.canvas,self.clicks)
        self.poly.generate_polygon()        
       
        self.canvas.bind("<B1-Motion>", self.motion)
        self.canvas.bind("<Double-Button-1>", self.scale)
        self.canvas.bind("<Double-Button-2>", self.scale_d)
        # Check if b was pressed
        
        #self.transformation_input()
        
    def motion(self,event):
        #print("Mouse position: (%s %s)" % (event.x, event.y))
        self.fresh()
        x_i=self.clicks[0][0]-event.x/abs(self.clicks[0][0]-event.x)
        y_i=self.clicks[0][1]-event.y/abs(self.clicks[0][1]-event.y)
        self.poly.translate_poly((x_i)*event.x/500,(y_i)*event.y/500)
        
    def show_point(self, event):
        self.clicks.append((event.x - 1, event.y - 1))
        self.canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill="")
        pt = (event.x-self.width//2, event.y-self.height//2)
        self.canvas.create_text(event.x-4, event.y-10, fill="black", font="Times 10", text="("+str(pt[0])+", "+str(pt[1])+")")

    def make_polygon(self, event):
        self.canvas.unbind("<Button-1", self.left_click_bind)
        self.canvas.unbind("<Button-3", self.right_click_bind)
        self.poly = Polygon(self.canvas,self.clicks)
        self.poly.generate_polygon()
        self.transformation_input()
        
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
        val=2
        #lst = list(map(float,input("Enter the x and y scaling factors you desire: ").split()))
        self.poly.scale_poly(val,val, self.height/2, self.width/2)
        
    def scale_d(self,event):
        self.fresh()
        val=3
        #lst = list(map(float,input("Enter the x and y scaling factors you desire: ").split()))
        self.poly.scale_poly(val,val, self.height/2, self.width/2)
            

    def rotate(self):
        self.fresh()
        self.angle=self.angle_entry.get()
        #angle = float(input("Please provide the angle of rotation: "))
        self.angle = float(self.angle)*np.pi/180
        self.poly.rotate_poly(self.angle, self.height/2, self.width/2)
               
        

class Polygon(tk.Canvas):
    def __init__(self, canvas, vertices):
        self.vertices = vertices
        self.canvas = canvas
        
    def generate_polygon(self):
        #self.canvas.delete("all")
        #buttonBG = self.canvas.create_rectangle(700, 0, 800, 30, fill="grey40", outline="grey60")
        #buttonTXT = self.canvas.create_text(750, 15, text="SAVE")
        return self.canvas.create_polygon(self.vertices, outline = "black", fill="",width=2)
        
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
        self.generate_polygon()


app = TwoDTransformationApp(height= 800, width = 800)
app.mainloop()