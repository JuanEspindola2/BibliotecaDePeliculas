from calendar import c
from cgitb import text
from importlib import import_module
from logging import setLogRecordFactory
from os import stat
import tkinter as tk
from tkinter import messagebox
from turtle import color, onclick
from tkinter import ttk, messagebox
from model.pelicula_dao import Pelicula, eliminar, guardar, listar, editar, eliminar

from model.pelicula_dao import crear_tabla, borrar_tabla
def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu = barra_menu, width= 300, height= 300)

    menu_inicio = tk.Menu(barra_menu, tearoff = 0)
    barra_menu.add_cascade(label='Inicio', menu= menu_inicio)
    
    menu_inicio.add_command(label='Create a register in database', command=crear_tabla)
    menu_inicio.add_command(label='Delete a register in database', command=borrar_tabla)
    menu_inicio.add_command(label='exit', command=root.destroy)

    barra_menu.add_cascade(label='queries')
    barra_menu.add_cascade(label='Config')
    barra_menu.add_cascade(label='Help')

class Frame(tk.Frame):
    def __init__(self,root = None):
        super().__init__(root, width=480, height=320 )
        self.root = root
        self.pack()
        self.id_pelicula = None

        self.campos_pelicula()
        self.deshabilitar_campos()
        self.tabla_peliculas()

    def campos_pelicula(self):
        #labels
        self.label_nombre = tk.Label(self, text = 'Name: ')
        self.label_nombre.config(font=('Arial', 12, 'bold'))
        self.label_nombre.grid(row=0,column=0, padx=10, pady= 10)
        
        self.label_duracion = tk.Label(self, text = 'Duration: ')
        self.label_duracion.config(font=('Arial', 12, 'bold'))
        self.label_duracion.grid(row=1,column=0, padx=10, pady= 10)

        self.label_genero = tk.Label(self, text = 'Gender: ')
        self.label_genero.config(font=('Arial', 12, 'bold'))
        self.label_genero.grid(row=2,column=0, padx=10, pady= 10)

        #entrys
        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self,textvariable= self.mi_nombre)
        self.entry_nombre.config(width=50, font=('Arial',12))
        self.entry_nombre.grid(row=0,column=1, padx=10, pady= 10, columnspan=2)

        self.mi_duration = tk.StringVar()
        self.entry_duration = tk.Entry(self, textvariable= self.mi_duration)
        self.entry_duration.config(width=50, font=('Arial',12))
        self.entry_duration.grid(row=1,column=1, padx=10, pady= 10, columnspan=2)

        self.mi_genero = tk.StringVar()
        self.entry_genero = tk.Entry(self, textvariable=self.mi_genero)
        self.entry_genero.config(width=50, font=('Arial',12))
        self.entry_genero.grid(row=2,column=1, padx=10, pady= 10, columnspan=2)

        #botones
        self.boton_nuevo = tk.Button(self, text='New: ', command=self.habilitar_campos)
        self.boton_nuevo.config(width=20,font=('Arial',12,'bold'),fg='#DAD5D6', bg='#158546', cursor='hand2', activebackground='#35BD6F')
        self.boton_nuevo.grid(row=3,column=0, padx=10, pady= 10)

        self.boton_guardar = tk.Button(self, text='Save: ', command=self.guardar_datos)
        self.boton_guardar.config(width=20,font=('Arial',12,'bold'),fg='#DAD5D6', bg='#1658A2', cursor='hand2', activebackground='#3586DF')
        self.boton_guardar.grid(row=3,column=1, padx=10, pady= 10)

        self.boton_cancelar = tk.Button(self, text='Cancel: ', command=self.deshabilitar_campos)
        self.boton_cancelar.config(width=20,font=('Arial',12,'bold'),fg='#DAD5D6', bg='#BD152E', cursor='hand2', activebackground='#E15370')
        self.boton_cancelar.grid(row=3,column=2, padx=10, pady= 10)

    def habilitar_campos(self):
        self.mi_nombre.set('')
        self.mi_duration.set('')
        self.mi_genero.set('')

        self.entry_nombre.config(state='normal')
        self.entry_genero.config(state='normal')
        self.entry_duration.config(state='normal')

        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def deshabilitar_campos(self):
        self.id_pelicula = None
        self.mi_nombre.set('')
        self.mi_duration.set('')
        self.mi_genero.set('')

        self.entry_nombre.config(state='disable')
        self.entry_genero.config(state='disable')
        self.entry_duration.config(state='disable')

        self.boton_guardar.config(state='disable')
        self.boton_cancelar.config(state='disable')

    def guardar_datos(self):

        pelicula = Pelicula(
            self.mi_nombre.get(),
            self.mi_duration.get(),
            self.mi_genero.get(),
        )

        if self.id_pelicula == None:
            guardar(pelicula)
        else:
            editar(pelicula, self.id_pelicula)

        self.tabla_peliculas()
        self.deshabilitar_campos()

    def tabla_peliculas(self):


        self.lista_peliculas = listar()
        self.lista_peliculas.reverse()


        self.tabla = ttk.Treeview(self, column=('Name','Duration','Gener'))
        self.tabla.grid(row=4, column=0, columnspan=4, sticky='nse')

        self.scroll = ttk.Scrollbar(self, orient = "vertical" , command= self.tabla.yview)
        self.scroll.grid(row = 4, column=4, sticky='nse')
        self.tabla.configure(yscrollcommand= self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='NAME')
        self.tabla.heading('#2', text='DURATION')
        self.tabla.heading('#3', text='GENER')

        #iterar lista de peliculas
        for p in self.lista_peliculas:
            self.tabla.insert('',0,text=p[0],values=(p[1], p[2], p[3]))

        #boton editar
        self.boton_editar = tk.Button(self, text='Edit: ', command= self.editar_datos)
        self.boton_editar.config(width=20,font=('Arial',12,'bold'),fg='#DAD5D6', bg='#158546', cursor='hand2', activebackground='#35BD6F')
        self.boton_editar.grid(row=5,column=0, padx=10, pady= 10)

        #Boton Eliminar
        self.boton_eliminar = tk.Button(self, text='Delete: ', command=self.eliminar_datos)
        self.boton_eliminar.config(width=20,font=('Arial',12,'bold'),fg='#DAD5D6', bg='#BD152E', cursor='hand2', activebackground='#E15370')
        self.boton_eliminar.grid(row=5,column=1, padx=10, pady= 10)

    def editar_datos(self):
        try:
            self.id_pelicula = self.tabla.item(self.tabla.selection())['text']
            self.nombre_pelicula = self.tabla.item(
                self.tabla.selection())['values'][0]
            self.duracion_pelicula = self.tabla.item(
                self.tabla.selection())['values'][1]
            self.genero_pelicula = self.tabla.item(
                self.tabla.selection())['values'][2]

            self.habilitar_campos()

            self.entry_nombre.insert(0, self.nombre_pelicula)
            self.entry_duration.insert(0, self.duracion_pelicula)
            self.entry_genero.insert(0, self.genero_pelicula)

        except:
            titulo = 'Edicion de datos'
            mensaje = 'No ha seleccionado ningun registro'
            messagebox.showerror(titulo,mensaje)

    def eliminar_datos(self):
        try:
            self.id_pelicula = self.tabla.item(self.tabla.selection())['text']
            eliminar(self.id_pelicula)

            self.tabla_peliculas()
            self.id_pelicula = None
        except:
            titulo = 'Eliminar un registro'
            mensaje = 'No ha seleccionado ningun registro'
            messagebox.showerror(titulo,mensaje)
