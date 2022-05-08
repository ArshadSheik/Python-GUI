import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import os, cv2

def app():
    root = Tk()
    root.geometry("600x400")
    bg = "#FF5733"
    root.configure(bg=bg)
    root.title('Video Frames Generator')

    Title = Label(root,text="Upload The Video Below", font=("bold",28), bg=bg)
    Title.pack(padx=25, pady=25, side=TOP)

    global upload
    upload = Button(root, text="Upload Video", font=("bold",11), width=20, bg='green', fg='white', command=lambda:uploadVid())
    upload.pack(padx=15, pady=15, side=TOP)

    Title_2 = Label(root,text="Choose Path To Save The Frames", font=("bold",25), bg=bg)
    Title_2.pack(padx=25, pady=25, side=TOP)

    global choose
    choose = Button(root, text="Choose Destination Path", font=("bold",11), width=25, bg='green', fg='white', command=lambda:setPath())
    choose.pack(padx=15, pady=15, side=TOP)

    gen = Button(root, text="Generate Frames", font=("bold",11), width=30, bg='blue', fg='white', command=lambda:GenFrames())
    gen.pack(padx=25, pady=25, side=TOP)

    root.mainloop()

def uploadVid():
    try:
        global file
        filetyps = (('MP4 files', '*.mp4'), ('MKV files', '*.mkv'))
        file = filedialog.askopenfilename(filetypes=filetyps)
        if file:
            upload['text'] = "Uploaded !!"
        else:
            print(showerror("ERROR", "Upload valid video !!"))
    except Exception as e:
        print(showerror("ERROR", e))

def setPath():
    try:
        global dstPath
        dstPath = filedialog.askdirectory()
        if dstPath:
            choose['text'] = str(dstPath)
        else:
            print(showerror("ERROR", "Choose valid path !!"))
    except Exception as e:
        print(showerror("ERROR", e))

def GenFrames():
    try:
        if file and dstPath:
            capture = cv2.VideoCapture(str(file))
            frameNr = 0
            while (True):
                success, frame = capture.read()
                if success:
                    os.chdir(dstPath)
                    cv2.imwrite(f'{frameNr}.jpg', frame)
                else:
                    break
                frameNr = frameNr+1

            capture.release()
            frameList()
        else:
            print(showerror("ERROR", "Input Missing !!"))
    except Exception as e:
        print(showerror("ERROR", e))

def frameList():
    global frm_set
    frm_set = list()
    for frm in os.listdir(dstPath):
        if frm.endswith(".jpg"):
            frm_set.append(str(frm))
    showFrames()

def showFrames():
    frm_tk = Toplevel()
    frm_tk.title("Frames Generated {Few}")
    frm_tk.geometry("620x615")
    frm_tk.configure(bg='cyan')

    img_name = 0
    row, col = 4, 4
    for i in range(row):
        frm_tk.grid_rowconfigure(i,  weight = 1)
        for j in range(col):
            frm_tk.grid_columnconfigure(i,  weight = 1)

            img = Image.open(frm_set[img_name])
            img = img.resize((450, 350), Image.Resampling.LANCZOS) # Resize images responsive to wondow size
            img = ImageTk.PhotoImage(img)
            lbl = tk.Label(frm_tk)
            lbl.grid(row=i, column=j, padx=5, pady=5)
            lbl.image = img
            lbl['image'] = img

            img_name = img_name + 1

    # To Reset
    choose['text'] = "Choose Destination Path"
    upload['text'] = "Upload Video"

    frm_tk.mainloop()

if __name__ == "__main__":
    app()
