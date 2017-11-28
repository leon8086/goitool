#coding=utf-8

import _winreg
import os,re,sys
from Tkinter import *

def IntKeyToNode( soup, key, subkey ):
    node = soup.new_tag( "key" )
    v, t = _winreg.QueryValueEx(key,subkey)
    node.attrs['name'] = subkey
    node.attrs['type'] = t
    node.string = str(v)
    return node

def BinaryEncode( s ):
    ret = ""
    for c in s:
        ret+="/"+str(hex(ord(c)))
    return ret[1:]

def BinaryDecode(s):
    ret = ""
    for c in s.split("/"):
        ret += chr(int(c,16))
    return ret

def SaveKey(out):
    key = _winreg.OpenKey( _winreg.HKEY_CURRENT_USER,r"Software\Bennett Foddy\Getting Over It")
    v, t = _winreg.QueryValueEx(key,"NumSaves_h765021473")
    out.write("%d\n"%v)
    v, t = _winreg.QueryValueEx(key,"SaveGame0_h1867918426")
    out.write("%s\n"%BinaryEncode(v))
    v, t = _winreg.QueryValueEx(key,"SaveGame1_h1867918427")
    out.write("%s\n"%BinaryEncode(v))

def LoadKey(out):
    values = out.read().split("\n")
    key = _winreg.OpenKey( _winreg.HKEY_CURRENT_USER,r"Software\Bennett Foddy\Getting Over It",0,_winreg.KEY_SET_VALUE)
    _winreg.SetValueEx(key,"NumSaves_h765021473",0,_winreg.REG_DWORD,int(values[0]))
    _winreg.SetValueEx(key,"SaveGame0_h1867918426",0,_winreg.REG_BINARY,BinaryDecode(values[1]))
    _winreg.SetValueEx(key,"SaveGame1_h1867918427",0,_winreg.REG_BINARY,BinaryDecode(values[2]))

def Save( ):
    dlg = Toplevel(root)
    rwid, rhei = root.winfo_x(), root.winfo_y()
    geo = "250x50+%d+%d"%(rwid+25,rhei+120)
    dlg.geometry(geo)
    dlg.filename=""
    dlg.resizable(width=False,height=False)
    name = Entry(dlg,width=35)
    name.grid(row=0)
    def Close():
        filename = name.get()
        dlg.destroy()
        if filename != "":
            filename=filename+".dat"
            SaveKey(open(filename,"w"))
            UpdateList(listb)
    btn = Button(dlg,text=u"确定", font=(u"宋体",12),command=lambda:Close())
    btn.grid(row=1)
    root.wait_window(dlg)

def Load():
    index = listb.curselection()
    if index == ():
        return
    filename = listb.get(listb.curselection())
    filename += ".dat"
    LoadKey(open(filename))

def UpdateList( lb ):
    listb.delete(0,listb.size()-1)
    for filename in os.listdir(u"."):
        if filename[-4:] != ".dat":
            continue
        filename = filename[:-4]
        lb.insert(0,filename)

root = Tk()

listb = Listbox(root,font=(u"宋体",12),width=37)
UpdateList(listb)

listb.grid( row=0, column=0, columnspan=2)
b_save = Button( root, text=u"存盘", font=(u"宋体",12), width=10, command=Save )
b_save.grid( row=1, column=0 )
b_load = Button( root, text=u"读取", font=(u"宋体",12), width=10, command=Load )
b_load.grid( row=1, column=1 )
root.title("Get Over It Save/Load")
width = root.winfo_vrootwidth()+root.winfo_vrootx()
height = root.winfo_vrootheight()+root.winfo_vrooty()
root.geometry( "300x210+%d+%d"%(width/2-150,height/2-100) )
root.resizable(width=False,height=False)
root.mainloop()
