import tkinter as tk
from tkinter  import ttk, messagebox
import csv
import sqlite3
from datetime import datetime



conn = sqlite3.connect('To-Do4.sqlite3')

c = conn.cursor()  #สร้างตัวดำเนินการ (อยากได้อะไรใช้ตัวนี้เลย)

#สร้าง table ด้วยคำสั่ง SQL


# 'lists', TEXT

c.execute("""CREATE TABLE IF NOT EXISTS Todolist (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                listID TEXT,
                lists TEXT
            )""")

def insert_list(listID,lists):
    ID = None
    with conn:   #with เปิด db เเล้วก็ปิดอัตโนมัติให้
        c.execute("""INSERT INTO Todolist VALUES (?,?,?)""",
            (ID,listID,lists))
        conn.commit() # การบันทึกข้อมูลลงในฐานข้อมูล ถ้าไม่รันตัวนี้จะไม่บันทึก
        # print('Insert Success!')

def show_list():
    with conn:
        c.execute("SELECT * FROM Todolist")      
        lists = c.fetchall()  #คำสั่งให้ดึงข้อมูลเข้ามา
        # print('lists:',lists)

    return lists    #return เป็นการส่งข้อมูลที่เราดึงมา นำไปใช้งาน    

def update_list(listID,lists):
    with conn:
        c.execute("""UPDATE Todolist SET lists=? WHERE listID=? """,
            ([lists,listID]))
    conn.commit()
    # print('Data updated')

def delete_list(listID):
    with conn:
        c.execute("DELETE FROM Todolist WHERE listID=?",([listID]))
        conn.commit()
        # print('Data deleted')    

def delete_all(listID):
    with conn:
        c.execute("DELETE FROM Todolist")  
        conn.commit()  



#------------------------------- สร้างหน้าต่าง ---------------------------------------------------------------

GUI = tk.Tk()
GUI.title("Throw-Do List v.1.0.0")
# GUI['bg']='gray'

w = 550
h = 550

ws = GUI.winfo_screenwidth() #screen width
hs = GUI.winfo_screenheight() #screen height


x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 50

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

Tab = ttk.Notebook(GUI)
T1 = tk.Frame(Tab)

F1= tk.Frame(T1)
F1.pack()

#-----------main icon--------------------##
main_icon = tk.PhotoImage(file='Note.png')
Mainicon = tk.Label(GUI,image=main_icon)
Mainicon.pack()


# Listbox to display tasks  #กรอบสี่เหลี่ยมตรงกลาง 
'''
resulttable1 = tk.Listbox(GUI, width=65, height=10, font=('Angsana New', 16))
resulttable.pack(padx=50)
'''

#------------------scrollbar---------------
'''
scrollbar = tk.Scrollbar(GUI)
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
'''



#---------------------Columns----------------------

header = ['listID','lists']
resulttable = ttk.Treeview(GUI,columns=header,show='headings',height=10)
resulttable.column('lists')
#scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
#resulttable.insert(parent='', index=0, iid=0, text='', values=('1','Vineet'))
#scrollbar.pack(side="right",ipady=10, fill="both")
resulttable.pack()



for h in header:
    resulttable.heading(h,text=h)

headerwidth = [60,372] 
for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)



#----------------------------- ฟังชั่นเพิ่มรายการ --------------------------------------------
def add_task(event=None):
    task = v_add.get()
    if task=='':
        messagebox.showwarning("Warning", "กรุณากรอกข้อมูล")
    # try:
    # if task == '':
        # messagebox.showwarning('Error','กรุณากรอกข้อมูล')
        # return
        # resulttable.insert('', 'end', value = [task])  
        # entry_task.delete(0, tk.END)
    # elif task =='':
        # messagebox.showwarning("Warning", "กรุณากรอกข้อมูล")
    # try:
    try:
        lists= (task)
        #clear ข้อมูลเก่า
        v_add.set('')

        today = datetime.now().strftime('%a')
        # print(today) 
        stamp = datetime.now()
        # dt = stamp.now().strftime('%Y-%m-%d %H:%M:%S')   #strftime คือ string format time
        listID = stamp.strftime('%Y%m%d%H%M%f')
        # dt = days[today] + '-' + dt    

        insert_list(listID,lists)

        with open('savedata3.csv','a',encoding='utf-8',newline='') as f:
            #with คือคำสั่งเปิดไฟล์เเล้วปิดอัตโนมัติ
            # 'a' การบันทึกไปเรื่อยๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า
            fw = csv.writer(f) #สร้างฟังค์ชั่นสำหรับเขียนข้อมูล
            data = [listID,lists]  
            fw.writerow(data)

        entry_task.focus()
        update_table()    

    except: 
        messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        v_add.set('')



GUI.bind('<Return>',add_task)


# ----------------------------ฟังชั่นรายการที่ทำเเล้ว------------------------------------------
def complete_task():
    try:
        selected_index = resulttable.curselection()[0]
        resulttable.itemconfig(selected_index, {'bg': 'light green', 'fg': 'black'})
    except IndexError:
        messagebox.showwarning("Warning", "กรุณาเลือกรายการที่ทำสำเร็จ")
        

# -----------------------------------ฟังชั่นลบรายการ---------------------------------------------------

alltransaction = {}
# print(type(alltransaction))


def UpdateCSV():
    with open('savedata3.csv','w',newline='',encoding='utf-8') as f:
        fw = csv.writer(f)
        # เตรียมข้อมูลจาก alltransaction ให้กลายเป็น list
        data = list(alltransaction.values())
        # print(data)
        fw.writerows(data) # multiple line from nested list [[],[],[]]
        # print('Table was updated')

def UpdateSQL():
    data = list(alltransaction.values())
    # print('uddata:',data)
    # print('UPDATE SQL:',data[0])
    for d in data:
        #transactionid,title,expense,quantity,รวม
        #d[0]=202307172259407777', d[1]'จันทร์-2023-07-17 22:59:36', d[2]'Egg',d[3]10.0,d[4]1,d[5]10.0
        update_list(d[0],d[1])

def DeleteRecord(event=None):
    check = messagebox.askyesno('Delete','คุณต้องการลบข้อมูลนี้ใช่หรือไม่')
    # print('YES/NO',check)    

    if check == True:
        # print('delete')
        select = resulttable.selection()
        # print(select)
        data = resulttable.item(select)
        data = data['values']
        # print(data)
        listID = data[0]
        # print(listID)
        #print(transactionid)
        #print(type(transactionid))
        del alltransaction[str(listID)] #delete data in dict
        # print(alltransaction)
        UpdateCSV()
        delete_list(str(listID))  # Delete in DB 
        update_table()       
    else:
        print('cancel')

resulttable.bind('<Delete>',DeleteRecord)

#------------------Delete All ----------------------

def DeleteRecordAll():
    check2 = messagebox.askyesno('DeleteAll','คุณต้องการลบข้อมูลทั้งหมดใช่หรือไม่')
    # print('YES/NO',check2)

    if check2 == True:
        select = resulttable.selection()
        data = resulttable.item(select)
        data = data['values']
        listID = data[0]
        del alltransaction[str(listID)]
        UpdateCSV()
        delete_all(str(listID))  # Delete in DB 
        update_table()
    else:
        print('cancel')





    ###########Right Click Menu##############
def EditRecord(eveny=None):
    POPUP = tk.Toplevel() #คล้ายๆกับ Tk()
    POPUP.title('EditRecord')
    #POPUP.geometry('500x400')

    w = 500
    h = 400

    ws = POPUP.winfo_screenwidth() #screen width
    hs = POPUP.winfo_screenheight() #screen height


    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2) - 50

    POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

    v_add = tk.StringVar()
    entry_task = tk.Entry(POPUP, textvariable=v_add, width=31, font=('Arial', 16))
    entry_task.pack(pady=50)
    # button_add = tk.Button(POPUP,fg = 'Blue',text="เพิ่มรายการ", font=('Arial', 14),cursor='plus', command=add_task)
    # button_add.pack(side = tk.BOTTOM,pady = 10,padx = 15)
    # E1 = tk.Entry(POPUP, width=37, font=('Arial', 20))
    # E1.pack(pady=100)


    def Edit(event=None):
        olddata = alltransaction[str(listID)]
        v1 = v_add.get()
        # total = v1
        newdata = [olddata[0],v1]
        alltransaction[str(listID)] = newdata
        UpdateSQL()
        update_table()
        POPUP.destroy() #สั่งปิด popup

    POPUP.bind('<Return>',Edit)

    B1  = tk.Button(POPUP,fg = 'Blue',text="บันทึก", font=('Arial', 14),cursor='plus', command=Edit)
    B1.pack(ipadx=40,ipady=10,pady=10)

    select = resulttable.selection()
    data = resulttable.item(select)
    data = data['values']
    listID = data[0]
    v_add.set(data[1])

    POPUP.mainloop()

resulttable.bind('<F2>',EditRecord)


#-------------------------------------------------------------------------------

frame = tk.Frame(GUI,padx=85,pady=20)   #relief กำหนดลักษณะเฟรมในรูปแบบ 3 มิติ
frame.pack()

v_add = tk.StringVar()
entry_task = tk.Entry(frame, textvariable=v_add, width=31, font=('Arial', 16))
entry_task.pack(pady=10)
button_add = tk.Button(frame,fg = 'Blue',text="เพิ่มรายการ", font=('Arial', 14),cursor='plus', command=add_task)
button_add.pack(side = tk.LEFT,pady = 10,padx = 15)


button_remove_completed = tk.Button(frame,fg = 'red', text="ลบรายการ", font=('Arial', 14),cursor='pirate', command=DeleteRecord)
button_remove_completed.pack(side = tk.RIGHT,pady = 10,padx = 15)

button_complete = tk.Button(frame, text="ทำสำเร็จ",fg = 'green', font=('Arial', 14),cursor='gumby', command=complete_task)
button_complete.pack(side = tk.BOTTOM, pady = 10,padx = 15)

#----save csv-------------

def read_csv():
    with open('savedata3.csv' ,newline='',encoding='utf-8',) as f:
        fr = csv.reader(f)
        data = list(fr)        
    return data



#-----------------right click---------------------------------------------------



rightclick = tk.Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='Complete', command=complete_task)
rightclick.add_command(label='Delete', command=DeleteRecord)
rightclick.add_command(label='Delete All', command=DeleteRecordAll)


def show_menu(event):
    rightclick.post(event.x_root, event.y_root)

GUI.bind("<Button-3>", show_menu)


def update_table():

    resulttable.delete(*resulttable.get_children())     #ได้เหมือน for loop
    #for c in resulttable.get_children():
        #resulttable.delete(c)
    try:    
        data = show_list()           #read_csv()
        # print('DATA:', data)
        for d in data:
            #creat transaction data
            alltransaction[d[1]] = d[1:] #d[1] = transaction id 
            resulttable.insert('',0,value=d[1:])
        # print('TS:',alltransaction)
    except Exception as e:
        print('No File')
        print('ERROR:',e)
    '''    
    for c in resulttable.get_children():
        resulttable.delete(c)
    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)
    print(data)
    '''            







UpdateCSV()
UpdateSQL()
update_table()
# print('GET CHILD:',resulttable.get_children())
GUI.mainloop()
