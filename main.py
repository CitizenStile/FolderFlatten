import os
import shutil
import subprocess
import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import filedialog
from tkinter.ttk import Checkbutton, Combobox

import numpy as np
from tomlkit import dumps as tdumps
from tomlkit import loads as tloads


class Config:
    isInit = False
    toml = {}

    def __init__(self, pth="config.toml"):
        if not "".__eq__(pth):
            self.load(pth)

    def load(self, pth="config.toml"):
        print("initializing...")
        self.isInit = True
        with open(str(pth)) as f:
            data = f.read()
        self.toml = tloads(data)

    @property
    def runBuild(self):
        return self.toml["basic"]["auto_amumss"]

    @property
    def path_build(self):
        return self.toml["paths"]["amumss_script"]

    @property
    def path_mo_nms(self):
        return str(self.toml["paths"]["mo"])

    @property
    def path_amumss(self):
        return self.toml["paths"]["amumss"]

    @property
    def path_amumss_extra_files(self):
        return os.path.join(self.path_amumss, "GlobalMEFTI")

    @property
    def path_nms(self):
        return self.toml["paths"]["nms"]

    @property
    def isOverwrite(self):
        return self.isclobber

    @property
    def clobber(self):
        res = str(self.toml["basic"]["clobber"]).lower()

        if res in ("yes", "y", "true"):
            return True
        if res in ("no", "n", "false"):
            return False
        return "ask"
        # return self.toml["basic"]["clobber"]

    @clobber.setter
    def clobber(self, value):
        self.toml["basic"]["clobber"] = "y" if value else "n"


def init():
    global cfg
    cfg = Config()


# create directory tree if missing and overwrite file if exists
def doCopy(srcPth, dstPth):
    os.makedirs(os.path.dirname(dstPth), exist_ok=True)
    shutil.copyfile(srcPth, dstPth)
    return


def select_folder(title="Select a folder"):
    return filedialog.askdirectory(title=title)


def select_src_folder():
    global svSrc
    svSrc.set(select_folder("Select a source folder"))


def select_dst_folder():
    global svDst
    svDst.set(select_folder("Select a destination folder"))


def main():
    global cfg, root, svSrc, svDst

    # Create the rootdow
    root = tk.Tk()
    root.title("Flatten folder structure")
    root.geometry("{}x{}".format(546, 250))

    # define our grid
    fInput = tk.LabelFrame(root, labelwidget=tk.Label(root, text="Folders"))
    # fOptions = tk.Frame(root)
    fOptions = tk.LabelFrame(root, labelwidget=tk.Label(root, text="Options"))
    fOutput = tk.Frame(root)

    # Set the layout of our frames
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    fInput.grid(row=0, sticky="new", padx=3)
    fOptions.grid(row=1, sticky="nsew", padx=3, pady=3)
    fOutput.grid(row=2, sticky="nsew", padx=3)

    # Create the widgets in our input frame
    lblSrc = tk.Label(fInput, text="Source folder")
    svSrc = tk.StringVar(root, "")
    entSrc = tk.Entry(fInput, width=80, textvariable=svSrc)
    btnSrc = tk.Button(fInput, text="Browse", command=select_src_folder)

    lblDst = tk.Label(fInput, text="Destination folder")
    svDst = tk.StringVar(root, "")
    entDst = tk.Entry(fInput, width=80, textvariable=svDst)
    btnDst = tk.Button(fInput, text="Browse", command=select_dst_folder)

    # Set the layout of our input frame
    lblSrc.grid(row=0, sticky="w")
    entSrc.grid(row=1, columnspan=2, sticky="we")
    btnSrc.grid(row=1, column=2, sticky="e")
    lblDst.grid(row=3, sticky="w")
    entDst.grid(row=4, columnspan=2, sticky="we")
    btnDst.grid(row=4, column=2, sticky="e")

    # Create the widgets in our Options frame
    lblAction = tk.Label(fOptions, text="Action")
    svAction = tk.StringVar(root, "Copy")
    cbxAction = Combobox(fOptions, textvariable=svAction)
    cbxAction["values"] = ("Copy", "Move", "Symlink")
    lblClobber = tk.Label(fOptions, text="If file exists")
    svClobber = tk.StringVar(root, "Overwrite")
    cbxClobber = Combobox(fOptions, textvariable=svClobber)
    cbxClobber["values"] = ("Ask", "Skip", "Overwrite")
    cbxClobber["state"] = "disabled"

    # Set the layout of our options frame
    lblAction.grid(row=0, column=0, sticky="w")
    cbxAction.grid(row=0, column=1, sticky="w")
    lblClobber.grid(row=0, column=2, sticky="w")
    cbxClobber.grid(row=0, column=3, sticky="w")

    # fRow1 = tk.Frame(root)
    # tk.Label(fRow1, text="Select  folder to flatten").pack()
    # fRow2 = tk.Frame(root).pack()
    # tbSrc = tk.Text(fRow2).pack
    # btnSrcBrowse = tk.Button(fRow2)

    # fRow1.pack()
    # frame = tk.Frame(root)
    # frame.pack(side=tk.LEFT)

    # tk.Label(root, text="Select folder to flatten").pack()
    # tk.Label(
    #     root, text="Click the button to select a file", font=("Arial 18 bold")
    # ).pack(pady=20)
    # button = tk.Button(root, text="Select", command=select_src_folder)
    # button.pack(ipadx=5, pady=15)
    root.mainloop()

    # init()

    # print(cfg.path_amumss())

    # for subdir, dirs, files in os.walk(cfg.path_mo_nms):
    #     for file in files:
    #         p = Path(os.path.relpath(subdir, cfg.path_mo_nms))
    #         parts = p.parts
    #         subPth = "\\".join(p.parts[1:])

    #         srcPth = os.path.join(subdir, file)
    #         basePath = cfg.path_amumss
    #         if subPth != "":
    #             # need to place in a sub folder
    #             basePath = cfg.path_amumss_extra_files

    #         dstPth = os.path.join(basePath, subPth, file)

    #         if not os.path.exists(dstPth) or cfg.clobber == True:
    #             doCopy(srcPth, dstPth)
    #             continue
    #         elif cfg.clobber == "ask":
    #             print("Extension: {}".format(p.parts[0]))
    #             print("File: {}".format(os.path.join(subPth, file)))
    #             nerootput = True
    #             clob = ""
    #             while clob not in ("y", "n", "a"):
    #                 if not nerootput:
    #                     print("Invalid input, valid input is y/n/a ")
    #                 nerootput = False

    #                 clob = input(
    #                     "Can I overwrite the file? [Y]es/[N]o/[A]lways: "
    #                 ).lower()

    #                 if clob in ("yes", "no", "always"):
    #                     clob = clob[0]
    #             if clob == "n":
    #                 print("Skipping file '{}'".format(file))
    #                 continue
    #             if clob in ("y", "a"):
    #                 doCopy(srcPth, dstPth)

    #             if clob == "a":
    #                 cfg.clobber = True

    # if cfg.runBuild:
    #     p = subprocess.Popen(
    #         cfg.path_build,
    #         cwd=os.path.dirname(cfg.path_build),
    #         creationflags=subprocess.CREATE_NEW_CONSOLE,
    #     )


if __name__ == "__main__":
    main()
