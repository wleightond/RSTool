#!/usr/bin/env python

from Tkinter import Tk, Frame, Toplevel, Menu, IntVar, StringVar, Label, Button,Checkbutton, Text, N, W, END
import Tkinter, Tkconstants, tkFileDialog, os

# This `if` just enables collapsing these in an an IDE
if True:
  from tests.helpers import read_data, func_data, LengthError
  from tests.Frequency import Frequency
  from tests.BlockFrequency import BlockFrequency
  from tests.Runs import Runs
  from tests.LongestRunOfOnes import LongestRunOfOnes
  from tests.Rank import Rank
  from tests.DiscreteFourierTransform import DiscreteFourierTransform
  from tests.NonOverlappingTemplateMatching import NonOverlappingTemplateMatching
  from tests.OverlappingTemplateMatching import OverlappingTemplateMatching
  from tests.Universal import Universal
  from tests.LinearComplexity import LinearComplexity
  from tests.Serial import Serial
  from tests.ApproximateEntropy import ApproximateEntropy
  from tests.CumulativeSums import CumulativeSums
  from tests.RandomExcursions import RandomExcursions
  from tests.RandomExcursionsVariant import RandomExcursionsVariant

# try:
#   # from testvisuals import RandomWalkPlot
#   pass
# except Exception as e:
#   print "Failed to import testvisuals:", e

class App(Frame):
  results_window = False
  def __init__(self, *args, **kwargs):
    Frame.__init__(self, *args, **kwargs)
    self.__init_main(*args, **kwargs)

  def __init_main(self, *args, **kwargs):
    self.root = args[0]
    self.root.filename = ""
    self.root.wm_title("RSTool")
    self.root.protocol("WM_DELETE_WINDOW", self.__delete_root_window)
    self.root.bind("<Destroy>", self.__destroy_root_window)

    self.menubar = Menu(self.root)
    self.filemenu = Menu(self.menubar)
    self.filemenu.add_command(label="Save as...", command=self.save_to_file)
    self.filemenu.add_separator()
    self.filemenu.add_command(label="Exit", command=self.root.destroy)
    self.menubar.add_cascade(label="File", menu=self.filemenu)

    self.root.config(menu=self.menubar)

    self.tests = [
                  Frequency,
                  BlockFrequency,
                  Runs,
                  LongestRunOfOnes,
                  Rank,
                  DiscreteFourierTransform,
                  Universal,
                  Serial,
                  ApproximateEntropy,
                  CumulativeSums,
                  RandomExcursions,
                  RandomExcursionsVariant,
                  ]
    self.slowtests = [
                      NonOverlappingTemplateMatching, # Slow
                      OverlappingTemplateMatching,  # Slow
                      LinearComplexity  # Slow
                      ]
    # self.run_RandomWalkPlot = IntVar(self.root)

    rcounter = 0

    # Create and pack the title row:
    title = "NYUAD\nCenter for Cyber Security\nRandomness Testing Tool\nv0.9.0"
    self.l1 = Label(self.root, text=title)
    self.l1.grid(column=0, row=rcounter, columnspan=2, sticky=N)
    # self.l1.pack()
    rcounter += 1

    # Create and pack the "Open File" button and bind the loadFile method:
    self.b1 = Button(self.root, text="Open File", command=self.loadFile)
    self.b1.grid(column=0, row=rcounter, columnspan=1, pady=5)
    # rcounter += 1
    # self.b1.pack()

    # Create and pack the filename:
    self.l2 = Label(self.root, text=self.root.filename)
    self.l2.grid(column=1, row=rcounter, columnspan=2, sticky=W, padx=(5, 10))
    # self.l1.pack()
    rcounter += 1

    # Create textbox for bit-limit
    self.nl = Label(self.root, text="Number of bits to test: (0 to test all)")
    self.nl.grid(column=0, row=rcounter, columnspan=1)
    rcounter += 1
    self.nt = Text(self.root, state="normal", width="15", height="1")
    self.nt.insert(END, "0")
    self.nt.grid(column=0, row=rcounter, columnspan=1, padx=10, pady=(0,5))
    rcounter += 1

    # Create and pack the "Select/Deselect All" button and bind the checkAll method:
    self.b2 = Button(self.root, text="Select/Deselect All Tests", command=self.checkAll)
    self.b2.grid(column=0, row=rcounter, columnspan=1, pady=(0,5))
    rcounter += 1
    # self.b2.pack()

    # Create and pack the "Select/Deselect Fast" button and bind the checkFast method:
    self.b3 = Button(self.root, text="Select/Deselect Fast Tests", command=self.checkFast)
    self.b3.grid(column=0, row=rcounter, columnspan=1, pady=(0,5))
    rcounter += 1
    # self.b2.pack()

    # Create and pack the "Select/Deselect Slow" button and bind the checkSlow method:
    self.b4 = Button(self.root, text="Select/Deselect Slow Tests", command=self.checkSlow)
    self.b4.grid(column=0, row=rcounter, columnspan=1, pady=(0,5))
    rcounter += 1
    # self.b2.pack()

    # Set IntVars for each test to check if it is selected to run:
    for test in self.tests + self.slowtests:
      setvar = "self.run_%s = IntVar(self.root)" % (test.__name__)
      exec(setvar)
      setvar = ""
      for i in range(func_data[test.__name__][1]):
        setvar = "self.%s_arg_%s = IntVar(self.root)" % (test.__name__, func_data[test.__name__][2][i])
      
      # Example:
        # self.run_Frequency = IntVar(self.root)

    # Create and pack the checkbutton for each test and bind its IntVar to it:
    for test in self.tests + self.slowtests:
      make = [
              "self.cb_%s = " % (test.__name__),
              "Checkbutton(self.root, ",
              "text='%s ', " % (func_data[test.__name__][0]),
              "variable=self.run_%s)" % (test.__name__)
              ]
      make = "".join(make)
      grid = [
              "self.cb_%s.grid(" % (test.__name__),
              "column=0, row=%d, sticky=W)" % rcounter
              ]
      grid = "".join(grid)
      # args stuff
      rcounter += 1
      # pack = "self.cb_%s.pack()" % (test.__name__)
      exec(make)
      exec(grid)
      # exec(pack)
      # Example:
        # self.cb1 = Checkbutton(self.root, text="Frequency",
        # variable=self.run_Frequency)
        # self.cb1.pack()

    # Create and pack the "Run Tests" button and bind the runTests method:
    self.rb = Button(self.root, text="Run Tests", command=self.runTests)
    self.rb.grid(column=0, row=rcounter, columnspan=2)
    rcounter += 1
    # self.rb.pack()

    self.root.resizable(0,0)
    self.root.lift()
    self.root.attributes('-topmost',True)
    self.root.after_idle(self.root.attributes,'-topmost',False)

  def __delete_root_window(self):
    # print "delete_root_window"
    try:
        self.root.destroy()
    except:
        pass

  def __destroy_root_window(self, event):
    # print "destroy_root_window", event
    pass

  def __delete_results_window(self):
    # print "delete_results_window"
    try:
        self.results_window.destroy()
    except:
        pass

  def __destroy_results_window(self, event):
    # print "destroy_results_window", event
    self.results_window = False

  def __make_results_window(self):
    # wname = "results_window"
    self.results_window = Toplevel(self, name="results_window")
    self.results_window.protocol("WM_DELETE_WINDOW",
                                 self.__delete_results_window)
    self.results_window.bind("<Destroy>", self.__destroy_results_window)
    self.results_window.wm_title("Test Results")
    self.results_window.config(menu=self.menubar)

    self.results_save_button = Button(self.results_window,
                                      text="Save to File",
                                      command=self.save_to_file)
    self.results_save_button.pack()

    self.results_text = Text(self.results_window, state="normal",
                             width="70", height="50")
    self.results_text.pack(fill="both", expand=True, padx=10)

  def loadFile(self):
    # print "loadFile called!"
    self.root.filename = tkFileDialog.askopenfilename(initialdir = ".",
                                                      title="Select file...")
    # print (self.root.filename)
    # self.l2.config(text=self.root.filename)

  def save_to_file(self):
    if self.results_window:
      self.root.outfile = tkFileDialog.asksaveasfile(mode='w',
                                                     defaultextension=".txt",
                                                     initialdir=".",
                                                     initialfile="output",
                                                     title="Save as...")
      data = str(self.results_text.get(0.0, END))
      self.root.outfile.write(data)
      self.root.outfile.close()

  def checkAll(self):
    all_checked = 1
    for test in self.tests + self.slowtests:
      if not eval('self.run_' + test.__name__ + '.get()'):
        all_checked = 0
    val = 1 - all_checked
    for test in self.tests + self.slowtests:
      eval('self.run_' + test.__name__).set(val)
  
  def checkFast(self):
    all_checked = 1
    for test in self.tests:
      if not eval('self.run_' + test.__name__ + '.get()'):
        all_checked = 0
    val = 1 - all_checked
    for test in self.tests:
      eval('self.run_' + test.__name__).set(val)
  
  def checkSlow(self):
    all_checked = 1
    for test in self.slowtests:
      if not eval('self.run_' + test.__name__ + '.get()'):
        all_checked = 0
    val = 1 - all_checked
    for test in self.slowtests:
      eval('self.run_' + test.__name__).set(val)

  def text_insert(self, text, noret=False):
    if not self.results_window:
      self.__make_results_window()
    place = 'end'
    if not self.results_text:
      raise Exception("results_text does not exist")
    if type(text) != str:
      raise TypeError("Expected str, got %s: %s" % (type(text), text))
    # self.results_text.configure(state="normal")  # enables changing content
    self.results_text.insert(place, text + ["\n", ""][noret])
    self.update_idletasks()
    # self.results_text.configure(state="disabled") # relocks the content
  
  def getn(self):
      return int(self.nt.get("1.0", END))

  def setn(self, n):
    self.nt.delete(1.0,END)
    self.nt.insert(END, str(int(n)))

  def runTests(self):
    if self.results_window:
      self.__delete_results_window()
    cont = True
    try:
      n = self.getn()
      if n < 0:
        raise ValueError
    except Exception as e:
      print 'Error:', e
      self.setn("0")
      cont = False
    if cont:
      try:
        if self.root.filename == "":
          raise ValueError("No file selected")
        e = read_data(self.root.filename)
        if n == 0:
          n = len(e)
        e = e[:n]
        if len(e) == 0:
          raise LengthError("No data in file")
        out = "Data read:\n"
        out += "e = "
        out += "".join([str(i) for i in e][:min(32, len(e))])
        out += ["", "..."][len(e) > 32] + "\n"
        out += "See test_results folder for detailed results\n"
        self.text_insert(out)
      except:
        self.text_insert("Failed to read data.")
        cont = False
    if cont:
      # for test in self.tests:
      #   self.text_insert("self.run_" + test.__name__ + " = " + str(eval(
      #                    "self.run_" + test.__name__ + ".get()")))
      test_dir = "./test_results"
      if not os.path.exists(test_dir):
        os.makedirs(test_dir)
      for test in self.tests + self.slowtests:
        try:
          if eval("self.run_" + test.__name__ + ".get()"):
            self.text_insert("Running " + test.__name__ + ":")
            output = test(e)
            self.text_insert(["Non-Random", "Random"][output])
            self.text_insert("\n")
        except Exception as e:
          self.text_insert("\nError in %s: %s\n" % (test.__name__, e.__str__()))

      self.text_insert("Tests completed.")

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
