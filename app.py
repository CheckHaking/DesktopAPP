from tkinter import ttk
from tkinter import *
import sqlite3

class Product:

    db = "database/productos.db"

    def __init__(self, root):
        self.window = root
        self.window.title("App Gestor de productos")
        self.window.resizable(1,1)
        self.window.wm_iconbitmap("resources/cube.ico")

        # Creacion del contenedor Frame Principal
        frame = LabelFrame(self.window, text="Registrar un nuevo Producto")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        #Label Nombre
        self.label_name = Label(frame, text="Nombre: ")
        self.label_name.grid(row=1, column=0)

        #Entry name
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Label Precio
        self.label_price = Label(frame, text="Precio: ")
        self.label_price.grid(row=2, column=0)

        #Entry price
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        # Label Stok
        self.label_stok = Label(frame, text="Stok: ")
        self.label_stok.grid(row=3, column=0)

        #Entry price
        self.stok = Entry(frame)
        self.stok.grid(row=3, column=1)

        #Button add product
        self.button_add = ttk.Button(frame, text="Guardar Producto", command=self.add_product)
        self.button_add.grid(row=4, columnspan=2, sticky=W+E)


        #Mensaje
        self.message = Label(text="", fg="red")
        self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)

        #Table of Products
        #Estyle for the table

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=("Calibri", 11))
        style.configure("mystyle.Treeview.Heading",
                        font=("Calibri", 13, "bold"))
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {'sticky':'nswe'})])

        self.table = ttk.Treeview(height=20, columns=(0,1), style="mystyle.Treeview")
        self.table.grid(row=4, column=0, columnspan=2)
        self.table.heading("#0", text="Nombre", anchor=CENTER)
        self.table.heading("#1", text="Precio", anchor=CENTER)
        self.table.heading("#2", text="Stok", anchor=CENTER)

        #Botones para eliminar
        button_del = ttk.Button(text="ELIMINAR", command=self.del_product)
        button_del.grid(row = 5, column=0, sticky=W+E)
        button_del = ttk.Button(text="EDITAR", command=self.edit_product)
        button_del.grid(row = 5, column=1, sticky=W+E)

        self.get_products()



    def db_query(self, consult, params=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            res = cursor.execute(consult, params)
            con.commit()
        return res

    def get_products(self):

        registros = self.table.get_children()
        for fila in registros:
            self.table.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_query(query)
        for fila in registros:
            print(fila)
            self.table.insert("", 0, text=fila[1], values=(fila[2], fila[3]))

    def validation_name(self):
        return len(self.name.get()) != 0

    def validation_price(self):
        return len(self.price.get()) != 0

    def validation_stok(self):
        return len(self.stok.get()) != 0



    def add_product(self):
        if self.validation_name() and self.validation_price() and self.validation_stok():

            consult = "INSERT INTO producto VALUES(NULL, ? , ? , ?)"
            params = (self.name.get(), self.price.get(), self.stok.get())
            self.db_query(consult, params)
            self.message['text'] = "Producto {} añadido con éxito".format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0,END)
            self.stok.delete(0, END)

        elif( self.validation_name()) and (self.validation_price() == False)  and (self.validation_stok()):
            self.message['text'] = "El precio es obligatorio"
        elif (self.validation_name()) and (self.validation_price() == False) and (self.validation_stok()==False):
            self.message['text'] = "El Precio y el Stok son obligatorios"
        elif (self.validation_name()) and (self.validation_price()) and (self.validation_stok() == False):
            self.message['text'] = "El Stok es obligatorio"
        elif( self.validation_name() == False) and (self.validation_price())  and (self.validation_stok()):
            self.message['text'] = "El Nombre es obligatorio"
        else:
            self.message['text'] = "Todos los datos son obligatorios"
        self.get_products()

    def del_product(self):
        self.message['text'] = ''
        name = self.table.item(self.table.selection())['text']
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_query(query, (name,))
        self.message['text'] = f'Producto {name} se a eliminado'
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''

        name = self.table.item(self.table.selection())["text"]
        price = self.table.item(self.table.selection())["values"][0]
        stok = self.table.item(self.table.selection())['values'][1]
        self.edit_window = Toplevel() #crear una ventana nueva
        self.edit_window.title = "Editar Producto"
        self.edit_window.resizable(1,1)
        self.edit_window.wm_iconbitmap("resources/cube.ico")

        title = Label(self.edit_window, text="Edicion de Producto", font=("Calibri", 20, "bold"))
        title.grid(row=0, column=0)

        frame_ep = LabelFrame(self.edit_window, text="Editar Producto")
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        #Label nombre anterior
        self.last_label_name = Label(frame_ep, text="Nombre anterior: ", font=("Calibri", 13))
        self.last_label_name.grid(row=2, column=0)
        # Entry old Name
        self.input_old_name = Entry(frame_ep, textvariable=StringVar(self.edit_window, value=name), state="readonly", font=("Calibri", 13)  )
        self.input_old_name.grid(row=2, column=1)

        #Label nombre nuevo
        self.new_name = Label(frame_ep, text="Nombre nuevo: ", font=("Calibri", 13))
        self.new_name.grid(row=3, column=0)

        # Entry new Name
        self.input_new_name = Entry(frame_ep, textvariable=StringVar(self.edit_window, value=name), font=("Calibri", 13)  )
        self.input_new_name.grid(row=3, column=1)

        ###########
        #Label precio anterior
        self.last_label_price = Label(frame_ep, text="Precio anterior: ", font=("Calibri", 13))
        self.last_label_price.grid(row=4, column=0)
        # Entry old precio
        self.input_old_price = Entry(frame_ep, textvariable=StringVar(self.edit_window, value=price), state="readonly", font=("Calibri", 13)  )
        self.input_old_price.grid(row=4, column=1)

        #Label precio nuevo
        self.new_price = Label(frame_ep, text="Precio nuevo: ", font=("Calibri", 13))
        self.new_price.grid(row=5, column=0)

        # Entry new price
        self.input_new_price = Entry(frame_ep, textvariable=StringVar(self.edit_window, value=price), font=("Calibri", 13)  )
        self.input_new_price.grid(row=5, column=1)

        ########
        #Label stok anterior
        self.last_label_stok = Label(frame_ep, text="Stok anterior: ", font=("Calibri", 13))
        self.last_label_stok.grid(row=6, column=0)
        # Entry old Name
        self.input_old_stok = Entry(frame_ep, textvariable=StringVar(self.edit_window, value=stok), state="readonly", font=("Calibri", 13)  )
        self.input_old_stok.grid(row=6, column=1)

        #Label nombre nuevo
        self.new_stok = Label(frame_ep, text="Stok nuevo: ", font=("Calibri", 13))
        self.new_stok.grid(row=7, column=0)

        # Entry new Name
        self.input_new_stok = Entry(frame_ep, textvariable=StringVar(self.edit_window, value=stok), font=("Calibri", 13)  )
        self.input_new_stok.grid(row=7, column=1)

        self.button_update = ttk.Button(frame_ep, text="Actualizar Producto", command=lambda: self.update_product(
                                                                                              self.input_new_name.get(),
                                                                                              self.input_old_name.get(),
                                                                                              self.input_new_price.get(),
                                                                                              self.input_old_price.get(),
                                                                                              self.input_new_stok.get(),
                                                                                              self.input_new_stok.get()
                                                                                                ))
        self.button_update.grid(row=8, columnspan=2, sticky=W+E)

    def update_product(self, a_name, n_name, a_price, n_price, a_stok, n_stok):
        query = "UPDATE producto SET nombre = ?, precio = ?, stok = ? WHERE nombre = ? AND precio = ? AND stok = ?"
        params = (n_name, n_price, n_stok, a_name, a_price, a_stok)
        self.db_query(query, params)
        self.edit_window.destroy()
        self.message["text"]='El producto {} ha sido actualizado!!'.format(a_name)



if __name__ == "__main__":
    root = Tk()
    app = Product(root)
    root.mainloop()



