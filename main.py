#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MySQLdb


class main_window(object):
    """docstring for main_window."""
    def __init__(self):
        super(main_window, self).__init__()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui.glade")
        self.main_window = self.builder.get_object("main_window")
        self.main_window.connect('delete-event', Gtk.main_quit)
        self.store = self.builder.get_object("liststore_cliente")
        self.treeview = self.builder.get_object("treeview_cliente")
        self.tree_selection = self.treeview.get_selection()
        self.populate_store(self.store)
        self.main_window.show_all()

        self.codigo_entry = self.builder.get_object("codigo_entry")
        self.nombre_entry = self.builder.get_object("nombre_entry")
        self.telefono_entry = self.builder.get_object("telefono_entry")
        self.ruc_entry = self.builder.get_object("ruc_entry")
        self.direccion_entry = self.builder.get_object("direccion_entry")

        self.builder.connect_signals(self)
        Gtk.main()


    # Add data to ListStore
    def populate_store(self, store):
        store.clear()
        try:
            connection = None
            connection = MySQLdb.connect('localhost', 'root', '')
            cursor = connection.cursor()
            #cursor.execute("Select * From `testochobits`.`cliente`")
            cursor.execute("call testochobits.listar_todo")
            rows = cursor.fetchall()

            for row in rows:

                self.store.append([row[0], row[1], row[2], row[3], row[4]])

        except MySQLdb.Error as e:
            self.store.append([str(e.args[0]), e.args[1], '', ''])

        finally:
            if connection != None:
                connection.close()

    def on_registrar_button_clicked(self, widget, data=None):
        codigo = self.codigo_entry.get_text()
        nombre = self.nombre_entry.get_text()
        telefono = self.telefono_entry.get_text()
        ruc = self.ruc_entry.get_text()
        direccion = self.direccion_entry.get_text()
        try:
            connection = None
            connection = MySQLdb.connect('localhost', 'root', '')
            cursor = connection.cursor()
            cursor.execute("call testochobits.registrar_cliente('12349', 'vampiri', '123456789', '1073064759', 'tututu')")
            connection.commit()

        except MySQLdb.Error as e:
            print(e)

        finally:
            if connection != None:
                connection.close()
        self.populate_store(self.store)

    def on_treeview_selection_changed(self, tree_selection, data=None):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,0)
            print (value)
            try:
                connection = None
                connection = MySQLdb.connect('localhost', 'root', '')
                cursor = connection.cursor()
                #cursor.execute("Select * From `testochobits`.`cliente`")
                result = cursor.execute('call testochobits.get_item({0})'.format(value))
                #print(result)
                rows = cursor.fetchone()

                self.codigo_entry.set_text(str(rows[0]))
                self.nombre_entry.set_text(rows[1])
                self.telefono_entry.set_text(rows[2])
                self.ruc_entry.set_text(rows[3])
                self.direccion_entry.set_text(rows[4])
            except MySQLdb.Error as e:
                print(e)

            finally:
                if connection != None:
                    connection.close()

    def enable_entry(self):
        self.codigo_entry.set_property("editable", True)
        self.nombre_entry.set_property("editable", True)
        self.telefono_entry.set_property("editable", True)
        self.ruc_entry.set_property("editable", True)
        self.direccion_entry.set_property("editable", True)
        self.nombre_entry.grab_focus()

    def clear_entry(self):
        self.nombre_entry.set_text("")
        self.telefono_entry.set_text("")
        self.ruc_entry.set_text("")
        self.direccion_entry.set_text("")


    def on_eliminar_button_clicked(self, widget, data=None):
        value = self.codigo_entry.get_text()
        if (value != ""):
            try:
                connection = None
                connection = MySQLdb.connect('localhost', 'root', '')
                cursor = connection.cursor()
                #cursor.execute("Select * From `testochobits`.`cliente`")
                result = cursor.execute('call testochobits.eliminar_cliente({0})'.format(value))
                connection.commit()
                print(result)

            except MySQLdb.Error as e:
                print(e)

            finally:
                if connection != None:
                    connection.close()
            self.populate_store(self.store)

        else:
            print("seleccione un registroB")

    def on_actualizar_button_clicked(self, widget, data=None):
        print("hola")

    def on_nuevo_button_clicked(self, widget, data=None):
        try:
            connection = None
            connection = MySQLdb.connect('localhost', 'root', '')
            cursor = connection.cursor()
            #cursor.execute("Select * From `testochobits`.`cliente`")
            #value = [3,2,0]
            cursor.execute('call testochobits.generar_codigo')
            result = cursor.fetchone()
            self.codigo_entry.set_text(str(result[0]))
            self.enable_entry()
            self.clear_entry()

        except MySQLdb.Error as e:
            print(e)

        finally:
            if connection != None:
                connection.close()

window = main_window()



#import MySQLdb
#
# db = MySQLdb.connect(host="localhost",    # your host, usually localhost
#                      user="root",         # your username
#                      passwd="",  # your password
#                      db="testochobits")        # name of the data base
#
# # you must create a Cursor object. It will let
# #  you execute all the queries you need
# cur = db.cursor()
#
# # Use all the SQL you like
# cur.execute("SELECT * FROM medico")
#
# # print all the first cell of all the rows
# for row in cur.fetchall():
#     print (row[0] + row[1])
#
# db.close()
