import os
from tkinter import *
from tkinter.ttk import *
from tkinter import font,colorchooser,filedialog,messagebox
import tempfile
from datetime import datetime

# -----Functionality of Menu Bar-----

url=''
fontSize=12
fontStyle='arial'
# 1. Font Style
def font_style(event):
    global fontStyle
    fontStyle=font_family_variable.get()
    textarea.config(font=(fontStyle,fontSize))
# 2. Font Size
def font_size(event):
    global fontSize
    fontSize=size_variable.get()
    textarea.config(font=(fontStyle,fontSize))
# 3. Bold text
def bold_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['weight']=='normal':
        textarea.config(font=(fontStyle,fontSize,'bold'))
    if text_property['weight']=='bold':
        textarea.config(font=(fontStyle,fontSize,'normal'))
# 4.Italic text
def italic_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['slant']=='roman':
        textarea.config(font=(fontStyle,fontSize,'italic'))
    if text_property['slant']=='italic':
        textarea.config(font=(fontStyle,fontSize,'roman'))
# 5. Underline text
def underline_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['underline']==0:
        textarea.config(font=(fontStyle,fontSize,'underline'))
    if text_property['underline']==1:
        textarea.config(font=(fontStyle,fontSize))
# 6. Select color
def color_select():
    color=colorchooser.askcolor()
    textarea.config(fg=color[1])
# 7. Right alignment
def right_align():
    data=textarea.get(1.0,END)
    textarea.tag_config('right',justify=RIGHT)
    textarea.delete(1.0,END)
    textarea.insert(INSERT,data,'right')
# 7. Left alignment
def left_align():
    data=textarea.get(1.0,END)
    textarea.tag_config('left',justify=LEFT)
    textarea.delete(1.0,END)
    textarea.insert(INSERT,data,'left')
# 7. Center alignment
def center_align():
    data=textarea.get(1.0,END)
    textarea.tag_config('center',justify=CENTER)
    textarea.delete(1.0,END)
    textarea.insert(INSERT,data,'center')
# 8. New File
def new_file(abc=None):
    global url
    url=''
    textarea.delete(1.0,END)
# 9. Open File
def open_file(abc=None):
    global url
    url=filedialog.askopenfilename(initialdir=os.getcwd,title='Select File',filetypes=(('Text File','.txt'),('All Files','*.*')))
    if url !='':
        data=open(url,'r')
        textarea.insert(1.0,data.read())
    root.title(os.path.basename(url))
# 10. Save File
def save_file(abc=None):
    if url=='':
        save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(("Text File",'.txt'),('All Files','*.*')))
        if save_url is not None:
            content=textarea.get(1.0,END)
            save_url.write(content)
            save_url.close()
    else:
        content=textarea.get(1.0,END)
        file=open(url,'w')
        file.write(content)
# 11. Save as File
def saveas_file():
    content=textarea.get(1.0,END)
    save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(("Text File",'.txt'),('All Files','*.*')))
    save_url.write(content)
    save_url.close()
    if url !='':
        os.remove(url)
# 12. Exit
def exit_file():
    if textarea.edit_modified():
        res=messagebox.askyesnocancel('Warning','Do you want to save the file?')
        if res is True:
            if url !='':
                content=textarea.get(1.0,END)
                file=open(url,'w')
                file.write(content)
                root.destroy()
            else:
                content=textarea.get(1.0,END)
                save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(("Text File",'.txt'),('All Files','*.*')))
                save_url.write(content)
                save_url.close()
                root.destroy()
        elif res is False:
            root.destroy()
        else:
            pass
    else:
        root.destroy()

# 13. Find and Replace
def find():

    def find_words():
        textarea.tag_remove('match',1.0,END)
        start_pos='1.0'
        fword=findentryfield.get()
        if fword:
            while True:
                start_pos=textarea.search(fword,start_pos,stopindex=END)
                if not start_pos:
                    break
                end_pos=f'{start_pos}+{len(fword)}c'
                textarea.tag_add('match',start_pos,end_pos)
                textarea.tag_config('match',foreground='Red',background='Yellow')
                start_pos=end_pos

    def replace_words():
        fword=findentryfield.get()
        rword=replaceentryfield.get()
        content=textarea.get(1.0,END)
        new_content=content.replace(fword,rword)
        textarea.delete(1.0,END)
        textarea.insert(1.0,new_content)

    find=Toplevel()
    find.title('Find')
    find.geometry('500x300+200+200')
    find.resizable(0,0)
    labelFrame=LabelFrame(find,text='Find/Replace')
    labelFrame.pack(pady=50)
    
    findlabel=Label(labelFrame,text='Find')
    findlabel.grid(row=0,column=0,padx='5px',pady='5px')
    findentryfield=Entry(labelFrame)
    findentryfield.grid(row=0,column=1,padx='5px',pady='5px')

    replacelabel=Label(labelFrame,text='Replace')
    replacelabel.grid(row=1,column=0,padx='5px',pady='5px')
    replaceentryfield=Entry(labelFrame)
    replaceentryfield.grid(row=1,column=1,padx='5px',pady='5px')

    findbtn=Button(labelFrame,text='FIND',command=find_words)
    findbtn.grid(row=2,column=0,padx='5px',pady='5px')

    replacebtn=Button(labelFrame,text='REPLACE',command=replace_words)
    replacebtn.grid(row=2,column=1,padx='5px',pady='5px')
    def remove_highlight():
        textarea.tag_remove('match',1.0,END)
        find.destroy()
    find.protocol('WM_DELETE_WINDOW',remove_highlight)
    find.mainloop()

# 14. Tool Bar
def toolbarfunc():
    if show_toolbar.get()==False:
        toolbar.pack_forget()
    else:
        textarea.pack_forget()
        toolbar.pack(fill=X)
        textarea.pack(fill=BOTH,expand=1)

# 15. themes
def themes(bg_color,fg_color):
    textarea.config(bg=bg_color,fg=fg_color)

# 16. Print File
def print_file():
    file=tempfile.mktemp('.txt')
    open(file,'w').write(textarea.get(1.0,END))
    os.startfile(file,'print')

# 17. Date and Time
def date_time(abc=None):
    curr=datetime.now()
    curr1=curr.strftime('%b %d, %Y %H:%M:%S')
    textarea.insert(1.0,curr1)

    
# -----GUI-----

root = Tk()
root.title('Text Editor')
root.geometry('1000x600+10+10')
root.resizable(0,0)

# -----MENU BAR-----

menubar=Menu()
root.config(menu=menubar)

# -----Toolbar-----

toolbar=Label(root)
toolbar.pack(side=TOP,fill=X)

# 1.Fonts
fonts=font.families()
font_family_variable=StringVar()
fontfamily_Combobox=Combobox(toolbar,width=30,values=fonts,state='readonly',textvariable=font_family_variable)
fontfamily_Combobox.current(fonts.index('Arial'))
fontfamily_Combobox.grid(row=0,column=0,padx=3)

# 2.Font-size
size_variable=IntVar()
font_size_Combobox=Combobox(toolbar,width=14,textvariable=size_variable,state='randomly',values=tuple(range(8,73)))
font_size_Combobox.current(4)
font_size_Combobox.grid(row=0,column=1,padx=3)
fontfamily_Combobox.bind('<<ComboboxSelected>>',font_style)
font_size_Combobox.bind('<<ComboboxSelected>>',font_size)

# 3.Buttons

# 3.1 Bold
boldImg=PhotoImage(file='bold.png')
boldbtn=Button(toolbar,image=boldImg,command=bold_text)
boldbtn.grid(row=0,column=2,padx=3)
# 3.2 Italic
italicImg=PhotoImage(file='italic.png')
italicbtn=Button(toolbar,image=italicImg,command=italic_text)
italicbtn.grid(row=0,column=3,padx=3)
# 3.3 Underline
underlineImg=PhotoImage(file='underline.png')
underlinebtn=Button(toolbar,image=underlineImg,command=underline_text)
underlinebtn.grid(row=0,column=4,padx=3)
# 3.4 Font color
fontcolorImg=PhotoImage(file='font_color.png')
fontcolorbtn=Button(toolbar,image=fontcolorImg,command=color_select)
fontcolorbtn.grid(row=0,column=5,padx=3)
# 3.5 left align
leftalignImg=PhotoImage(file='left.png')
leftalignbtn=Button(toolbar,image=leftalignImg,command=left_align)
leftalignbtn.grid(row=0,column=6,padx=3)
# 3.6 right align
rightalignImg=PhotoImage(file='right.png')
rightalignbtn=Button(toolbar,image=rightalignImg,command=right_align)
rightalignbtn.grid(row=0,column=7,padx=3)
# 3.7 center align
centeralignImg=PhotoImage(file='center.png')
centeralignbtn=Button(toolbar,image=centeralignImg,command=center_align)
centeralignbtn.grid(row=0,column=8,padx=3)

# ---Scrollbar---

scrollbar=Scrollbar(root)
scrollbar.pack(side=RIGHT,fill=Y)
textarea=Text(root,yscrollcommand=scrollbar.set,font=('arial',12),undo=True)
textarea.pack(fill=BOTH,expand=True)
scrollbar.config(command=textarea.yview)

# 1.File
filemenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='New',accelerator='Ctrl+N',compound=LEFT,command=new_file)
filemenu.add_command(label='Open',accelerator='Ctrl+O',compound=LEFT,command=open_file)
filemenu.add_command(label='Save',accelerator='Ctrl+S',compound=LEFT,command=save_file)
filemenu.add_command(label='Save as',accelerator='Ctrl+Alt+S',compound=LEFT,command=saveas_file)
filemenu.add_command(label='Print',accelerator='Ctrl+P',compound=LEFT,command=print_file)
filemenu.add_separator()
filemenu.add_command(label='Exit',accelerator='Ctrl+Q',compound=LEFT,command=exit_file)

# 2.Edit
editmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='Edit',menu=editmenu)
editmenu.add_command(label='Cut',accelerator='Ctrl+X',compound=LEFT,command=lambda :textarea.event_generate('<Control x>'))
editmenu.add_command(label='Copy',accelerator='Ctrl+C',compound=LEFT,command=lambda : textarea.event_generate('<Control c>'))
editmenu.add_command(label='Paste',accelerator='Ctrl+V',compound=LEFT,command=lambda : textarea.event_generate('<Control v>'))
editmenu.add_command(label='Select All',accelerator='Ctrl+A',compound=LEFT)
editmenu.add_command(label='Undo',accelerator='Ctrl+Z',compound=LEFT)
editmenu.add_command(label='Find',accelerator='Ctrl+F',compound=LEFT,command=find)
editmenu.add_command(label='Date/Time',accelerator='Ctrl+D',compound=LEFT,command=date_time)
editmenu.add_command(label='Clear',accelerator='Ctrl+Alt+X',compound=LEFT,command=lambda :textarea.delete(1.0,END))

# 3.View
show_toolbar=BooleanVar()
viewmenu=Menu(menubar,tearoff=False)
viewmenu.add_checkbutton(label='Tool Bar',variable=show_toolbar,onvalue=True,offvalue=False,compound=LEFT,command=toolbarfunc)
show_toolbar.set(True)
menubar.add_cascade(label='View',menu=viewmenu)

# 4.Themes
theme_choice=StringVar()
themesmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='Themes',menu=themesmenu) 
lightImage=PhotoImage(file='light_default.png')
themesmenu.add_radiobutton(label='Light Default',image=lightImage,variable='theme_choice',compound=LEFT,command=lambda : themes('white','black'))
monokaiImage=PhotoImage(file='monokai.png')
themesmenu.add_radiobutton(label='Monokai',image=monokaiImage,variable='theme_choice',compound=LEFT,command=lambda : themes('orange','white'))
darkImage=PhotoImage(file='dark.png')
themesmenu.add_radiobutton(label='Dark',image=darkImage,variable='theme_choice',compound=LEFT,command=lambda : themes('darkgray','white'))
pinkImage=PhotoImage(file='red.png')
themesmenu.add_radiobutton(label='Pink',image=pinkImage,variable='theme_choice',compound=LEFT,command=lambda : themes('pink','blue'))


root.bind("<Control-o>",open_file)
root.bind("<Control-n>",new_file)
root.bind("<Control-s>",save_file)
root.bind("<Control-Alt-s>",saveas_file)
root.bind("<Control-q>",exit_file)
root.bind("<Control-p>",print_file)
root.bind("<Control-d>",date_time)

root.mainloop()