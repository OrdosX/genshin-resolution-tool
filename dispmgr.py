from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from winreg import *
from configparser import ConfigParser
from functools import partial

root = Tk()
nameWidth = ""
nameHeight = ""
nameFullscreen = ""
varWidth = StringVar()
varHeight = StringVar()
varFullscreen = StringVar()

def readRegistry():
    with OpenKeyEx(HKEY_CURRENT_USER, "SOFTWARE\\miHoYo\\原神") as key:
        global nameWidth, nameHeight, nameFullscreen
        global varWidth, varHeight, varFullscreen
        keyInfo = QueryInfoKey(key)
        for i in range(0, keyInfo[1]):
            valueName = EnumValue(key, i)[0]
            if valueName.startswith("Screenmanager"):
                if valueName.find("Width") != -1:
                    nameWidth = valueName
                    varWidth.set(QueryValueEx(key, valueName)[0])
                elif valueName.find("Height") != -1:
                    nameHeight = valueName
                    varHeight.set(QueryValueEx(key, valueName)[0])
                elif valueName.find("Fullscreen") != -1:
                    nameFullscreen = valueName
                    varFullscreen.set(QueryValueEx(key, valueName)[0])
def writeRegistry():
    with OpenKeyEx(HKEY_CURRENT_USER, "SOFTWARE\\miHoYo\\原神", access=KEY_SET_VALUE) as key:
        if nameFullscreen != "":
            SetValueEx(key, nameWidth, 0, REG_DWORD, int(varWidth.get()))
            SetValueEx(key, nameHeight, 0, REG_DWORD, int(varHeight.get()))
            SetValueEx(key, nameFullscreen, 0, REG_DWORD, int(varFullscreen.get()))
            messagebox.showinfo(title="成功", message="显示设置已更新")

root.title("原神显示设置工具")
root.eval('tk::PlaceWindow . center')
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="宽度").grid(column=0, row=0, padx=(0,20), pady=(0,20))
ttk.Label(frm, text="高度").grid(column=0, row=1, padx=(0,20), pady=(0,20))
ttk.Label(frm, text="全屏").grid(column=0, row=2, padx=(0,20))
ttk.Entry(frm, textvariable=varWidth).grid(column=1, row=0, pady=(0,20))
ttk.Entry(frm, textvariable=varHeight).grid(column=1, row=1, pady=(0,20))
frmFullscreen = ttk.Frame(frm)
frmFullscreen.grid(column=1, row=2)
ttk.Radiobutton(frmFullscreen, text="是", value="1", variable=varFullscreen).grid(column=0, row=0)
ttk.Radiobutton(frmFullscreen, text="否", value="0", variable=varFullscreen).grid(column=1, row=0, padx=(40, 0))
readRegistry()

config = ConfigParser()
frmPreset = ttk.Labelframe(frm, text="预设")
frmPreset.grid(column=0, columnspan=2, row=3, pady=(10, 10))
frmPresetButtons = ttk.Frame(frmPreset)
frmPresetButtons.grid(column=0, row=0)

def readPreset():
    global frmPresetButtons
    config.read('config.ini', encoding="UTF-8")
    for index,preset in enumerate(config.sections()):
        def apply(preset):
            global config, varWidth, varHeight, varFullscreen
            varWidth.set(config[preset]["width"])
            varHeight.set(config[preset]["height"])
            varFullscreen.set(config[preset]["fullscreen"])
        ttk.Button(frmPresetButtons, text=preset, command=partial(apply,preset)).grid(column=index%3, row=int(index/3))
def savePreset():
    varPresetName = StringVar(value="%sx%s%s" % (varWidth.get(), varHeight.get(), "全屏" if varFullscreen.get() == "1" else "窗口"))
    dlgPresetName = Toplevel(root)
    dlgPresetName.title("请输入预设名称")
    root.eval("tk::PlaceWindow %s center" % dlgPresetName)
    def writePreset():
        if not config.has_section(varPresetName.get()):
            config.add_section(varPresetName.get())
        config[varPresetName.get()]["width"] = varWidth.get()
        config[varPresetName.get()]["height"] = varHeight.get()
        config[varPresetName.get()]["fullscreen"] = varFullscreen.get()
        with open("config.ini", "w", encoding="UTF-8") as f:
            config.write(f)
        dlgPresetName.destroy()
        for item in frmPresetButtons.winfo_children():
            item.destroy()
        readPreset()
    ttk.Label(dlgPresetName, text="预设名称").grid(column=0, row=0, padx=(10,10), pady=(10,10))
    ttk.Entry(dlgPresetName, textvariable=varPresetName).grid(column=1, row=0, padx=(10,10), pady=(10,10))
    ttk.Button(dlgPresetName, text="确定", command=writePreset).grid(column=0, row=1, padx=(10,10), pady=(10,10))
    ttk.Button(dlgPresetName, text="取消", command=dlgPresetName.destroy).grid(column=1, row=1, padx=(10,10), pady=(10,10))
    dlgPresetName.transient(root)
    dlgPresetName.wait_visibility()
    dlgPresetName.grab_set()
    dlgPresetName.wait_window()
readPreset()
ttk.Button(frmPreset, text="添加预设", command=savePreset, width=40).grid(pady=(10, 0))

frmButtons = ttk.Frame(frm)
frmButtons.grid(column=0, columnspan=2, row=4)
ttk.Button(frmButtons, text="重置为当前", command=readRegistry).grid(column=0, row=0)
ttk.Button(frmButtons, text="提交", command=writeRegistry).grid(column=1, row=0)
ttk.Button(frmButtons, text="退出", command=root.destroy).grid(column=2, row=0)

root.mainloop()