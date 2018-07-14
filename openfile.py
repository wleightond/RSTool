from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
 
root = Tk()
root.filename = tkFileDialog.askopenfilename(initialdir = "$HOME",title = "Select file")
print (root.filename)
root.destroy()
