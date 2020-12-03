# -*- coding: utf-8 -*-
#HowardXue20190816
from tkinter import *
from tkinter import ttk
import serial
import serial.tools.list_ports
import subprocess
import os
import tkinter.filedialog



wl = "wl.exe"
serialCmdStr = " --serial "
portCmdStr = "0"

print('Wait for GUI start...')
def GetComPortList():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) == 0:
       print('找不到串口')
       #port_list[0] = '找不到串口'
    else:
        for i in range(0,len(port_list)):
            # print(port_list[i])
            pass
    return port_list

def OnCmSelected(*args): 
    global portCmdStr
    CurSelected = comboxlist.get()
    portCmdStr = CurSelected[3:4]
    CportLable_text.set("COM Select:" + portCmdStr)
    print("ComPortSelect: " + CurSelected)  

def DoWlCommands(cmd = 'ver'):
    if os.path.exists(wl):
        wlcmd = wl + serialCmdStr + portCmdStr +' '+ cmd
        # print(wlcmd)
        ShowSendtoDUT(wlcmd)
        try:
            rst = subprocess.getstatusoutput(wlcmd)
        except subprocess.CalledProcessError as exc:
            rst = exc.output
            print(exc.returncode)
            print(exc.output)
        # print(rst)
        return rst
    else:
        inputData.insert(END, "wl.exe Not found in folder")

def ShowSendtoDUT(wlcmd):
    SendDut = '\n\r >>[Send to DUT] >>:\n\r'
    inputData.insert(END, SendDut)
    inputData.insert(END, wlcmd)

def ShowRcvfromDUT(rst):
    RcvDut = ' \n\r >>[Rcv from DUT] >>:\n\r'
    txt.insert(END, RcvDut)
    txt.insert(END, rst)

def OnComTest_GetVersion():
     rst = DoWlCommands()
     ShowRcvfromDUT(rst)
     #inputData.delete(0.0, END)

def OnCommandInput():
    InputCmd = Et_CommandInput.get()
    if(len(InputCmd) == 0):
        print("未输入命令")
    else:
        rst = DoWlCommands(InputCmd)
        ShowRcvfromDUT(rst)

def clearSendContent():
     inputData.delete(1.0, END)

def clearRcvContent():
     txt.delete(1.0, END)

def executeBatchfile(filepath):
    try:
        rst = subprocess.Popen("cmd.exe /c" + filepath, shell=False)
    except subprocess.CalledProcessError as exc:
        rst = exc.output
        print(exc.returncode)
        print(exc.output)
    return rst

def OnBatchCmd():
    File_Batch = tkinter.filedialog.askopenfilename()
    if File_Batch != '':
        Filelog = "\nStart Execute Batch file: \n" + File_Batch+'\n\n\r'
        inputData.insert(END, Filelog)
        print(Filelog)
        rst = executeBatchfile(File_Batch)
        print(rst)

    #    root.destory()
    else:
        Filelog = "\nPlease select Batch file! \n"
        inputData.insert(END, Filelog)
        print(Filelog)

def OnRefreshCom():
    PortList = GetComPortList()
    if len(PortList) != 0:
        comboxlist["values"] = PortList
        comboxlist.current(0)
        CurSelected = comboxlist.get()
        print("CurSelected:" + CurSelected)
        ComPortSelected = CurSelecte5d[3:4]
        print("ComPortSelected:" + ComPortSelected)
        global portCmdStr
        portCmdStr = ComPortSelected
        CportLable_text.set("COM Select:" + portCmdStr)
    else:
        CportLable_text.set("COM Not Found")
        inputData.insert(END, "\n未找到可用串口，请检查接线！")
        comboxlist.set('')

#Tkinter code below
root = Tk()
root.geometry('1000x600')
root.title('WiFi WL Commands Test Tools from HowieXue')
root.config(bg='#f0ffff')

#Lable
intro = Label(root,text='请先选择串口，然后点击相应按钮进行WL测试',\
                       bg='#d3fbfb',\
                       fg='red',\
                       font=('华文新魏',14),\
                       width=20,\
                       height=2,\
                       relief=RIDGE)

intro.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

CportLable_text = StringVar()
CportLable = Label(root, textvariable = CportLable_text,\
                      # bg='#d3fbfb',\
                       fg='red',\
                       font=('华文新魏',14),\
                       width=20,\
                       height=2,\
                       relief=RIDGE)
CportLable.place(relx=0.1, rely=0.03, relwidth=0.15, relheight=0.05)

ContactLable = Label(root, text='联系方式：HowieXue@163.com',\
                      # bg='#d3fbfb',\
                       fg='red',\
                       font=('',12),\
                       width=20,\
                       height=2,\
                       relief=RIDGE)
ContactLable.place(relx=0.7, rely=0.03, relwidth=0.25, relheight=0.05)

#Input
inputData = Text(root, font = ('',10))
inputData.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.625)

#Output
txt = Text(root, font = ('',10))
txt.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.625)

#lable
Lb_CommandInput = Label(root,text='输入WL CMD:',\
                      # bg='#d3fbfb',\
                       fg='red',\
                       font=('华文新魏',14),\
                       width=20,\
                       height=2,\
                       relief=RIDGE)

Lb_CommandInput.place(relx=0.425, rely=0.337, relwidth=0.15, relheight=0.05)

Lb_CommandBatch = Label(root,text='执行Batch文件：',\
                      # bg='#d3fbfb',\
                       fg='red',\
                       font=('华文新魏',14),\
                       width=20,\
                       height=2,\
                       relief=RIDGE)

Lb_CommandBatch.place(relx=0.425, rely=0.59, relwidth=0.15, relheight=0.05)

#Entry
Et_CommandInput = Entry(root, bd =5, relief=GROOVE)

Et_CommandInput.place(relx=0.425, rely=0.4, relwidth=0.15, relheight=0.05)

#Button
bt_json2bin = Button(root, text='连接测试: Get WL Version', command=OnComTest_GetVersion, fg ='blue')
bt_json2bin.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.1)

bt_bin2json = Button(root, text='执行WL Command', command=OnCommandInput, fg ='blue')
bt_bin2json.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.1)

bt_batch = Button(root, text='选择要执行的Batch文件', command=OnBatchCmd, fg ='blue')
bt_batch.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.1)

bt_clear = Button(root, text='Clear Send Data', command=clearSendContent, fg ='blue')
bt_clear.place(relx=0.15, rely=0.825, relwidth=0.2, relheight=0.1)

bt_clear_rcv = Button(root, text='Clear Receive Data', command=clearRcvContent, fg ='blue')
bt_clear_rcv.place(relx=0.65, rely=0.825, relwidth=0.2, relheight=0.1)

bt_refresh = Button(root, text='刷新', command=OnRefreshCom, fg ='blue')
bt_refresh.place(relx=0.5, rely=0.03, relwidth=0.05, relheight=0.05)

#Combobox
comvalue = StringVar()
comboxlist = ttk.Combobox(root, textvariable=comvalue, width =20)  # 初始化
comboxlist.place(relx=0.25, rely=0.03, relwidth=0.25, relheight=0.05)

#refresh

OnRefreshCom()

comboxlist.bind("<<ComboboxSelected>>", OnCmSelected)

#comboxlist.pack()

root.mainloop()

