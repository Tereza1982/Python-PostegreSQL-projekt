from tkinter import * 
import psycopg2
from tkinter import messagebox


root = Tk()
root.title("Teachers")
root.geometry('500x500')
root.configure(bg='#C7B299')
root.resizable(False, False)

def get_connection():
    conn =  psycopg2.connect(
        dbname="student",
        user="postgres",
        password="admin",
        host="localhost",
        port='5432'
    )
    return conn


def insert_data(name, age, address):
    entry_name.delete(0,END)
    entry_age.delete(0,END)
    entry_address.delete(0,END)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO teacher (name, age, address) VALUES (%s, %s, %s)", (name, age, address))
    conn.commit()
    cur.close()
    conn.close()
    
    messagebox.showinfo("Informace", "Jméno přidáno do databáze")
    display_all() # aby se okno refreshovalo pri kazdem vlozeni novych dat



def search(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM teacher WHERE id = (%s)''', (id,))
    row = cur.fetchone()
    if row:
        display_search(row)
    else:
        messagebox.showinfo("Informace", "ID nenalezeno")
    conn.commit()
    cur.close()
    conn.close()

def display_search(data):
    listbox = Listbox(root, width=20, height=1)
    listbox.grid(row=8, column=1)
    listbox.insert(0, data[1::])
    
def display_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM teacher''')
    seznam = cur.fetchall()
    listbox = Listbox(root, width=30, height=5)
    listbox.grid(row=9, column=1)
    
    scrollbar = Scrollbar(root)
    scrollbar.grid(row=9, column=2, sticky='ns') # posouvani scrollbaru podle svetovych stran
    
    # propojeni Scrollbaru s Listboxem
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    

    
    for jeden_radek in seznam:
        listbox.insert(0,jeden_radek)
    
       
display_all()
      

label_general = Label(root, text= 'Add data',bg='#C7B299')
label_general.grid(row=0, column=1)

label_name = Label(root, text=' Name ',bg='#C7B299')
label_name.grid(row=1, column=0)

entry_name = Entry(root)
entry_name.grid(row=1, column=1)

label_age = Label(root, text="Age ",bg='#C7B299')
label_age.grid(row=2, column=0)

entry_age = Entry(root)
entry_age.grid(row=2, column=1)

label_address = Label(root, text="Address ",bg='#C7B299')
label_address.grid(row=3, column=0)

entry_address = Entry(root)
entry_address.grid(row=3, column=1)

button = Button(root, text='Add', command=lambda:insert_data(entry_name.get(),entry_age.get(),entry_address.get()))
button.grid(row=4,column=1)

label_search = Label(root, text='Search data',bg='#C7B299')
label_search.grid(row=5,column=1)

label_id = Label(root, text='Search by ID',bg='#C7B299')
label_id.grid(row=6, column=0)

entry_id = Entry(root)
entry_id.grid(row=6, column=1)

button_search = Button(root, text='Search', command=lambda:search(entry_id.get()) if entry_id.get().strip() else None)
button_search.grid(row=7, column=1)

root.mainloop()


