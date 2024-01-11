import tkinter as tk
import tkinter.font as tkFont
import win32gui
import win32con
import time
import subprocess
#pip install pyinstaller --- pyinstaller --onefile filename.py -> export to exe
#pip install pywin32
#pip install pygetwindow pyautogui
#pip install --upgrade pygetwindow
#pip install tk

class App:
    def __init__(self, root):
        #setting title
        root.title("SortWindowYulgang")
        #setting window size
        width=376
        height=385
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_186=tk.Label(root)
        ft = tkFont.Font(family='Times',size=23)
        GLabel_186["font"] = ft
        GLabel_186["fg"] = "#333333"
        GLabel_186["justify"] = "center"
        GLabel_186["text"] = "Sort Windows Yulgang"
        GLabel_186.place(x=40,y=10,width=300,height=30)

        Btn_Sort=tk.Button(root)
        Btn_Sort["anchor"] = "center"
        Btn_Sort["bg"] = "#ff7800"
        Btn_Sort["borderwidth"] = "0px"
        ft = tkFont.Font(family='Times',size=14)
        Btn_Sort["font"] = ft
        Btn_Sort["fg"] = "#fad400"
        Btn_Sort["justify"] = "center"
        Btn_Sort["text"] = "SORT"
        Btn_Sort.place(x=30,y=50,width=136,height=46)
        Btn_Sort["command"] = self.Btn_Sort_command

        Btn_open=tk.Button(root)
        Btn_open["bg"] = "#cc0000"
        Btn_open["borderwidth"] = "0px"
        ft = tkFont.Font(family='Times',size=14)
        Btn_open["font"] = ft
        Btn_open["fg"] = "#fad400"
        Btn_open["justify"] = "center"
        Btn_open["text"] = "OPEN YG"
        Btn_open.place(x=210,y=50,width=133,height=44)
        Btn_open["command"] = self.Btn_open_command

        self.Listname = tk.Text(root, wrap='none')
        ft = tkFont.Font(family='Times', size=10)
        self.Listname["font"] = ft
        self.Listname["fg"] = "#333333"
        self.Listname["insertbackground"] = "#333333"
        self.Listname["height"] = 15  # Set the number of visible lines
        self.Listname["width"] = 60   # Set the width of the visible area
        self.Listname.place(x=5, y=110)

        scrollbar = tk.Scrollbar(root, command=self.Listname.yview)
        scrollbar.place(x=340, y=120, height=229)
        self.Listname["yscrollcommand"] = scrollbar.set

        self.Listname.insert(tk.END, "Process:\n")

    def Btn_Sort_command(self):
        windows = []
        win32gui.EnumWindows(lambda hwnd, windows: windows.append((hwnd, win32gui.GetWindowText(hwnd))), windows)
        non_empty_windows = [(hwnd, title) for hwnd, title in windows if title]
        sorted_windows = App.sort_windows_by_title(non_empty_windows)  # Use the class to call the static method
        App.move_windows_to_right(sorted_windows)  # Use the class to call the static method

        # Update the Listname label with the list of processes
        process_list = '\n'.join(title for _, title in sorted_windows)
        self.Listname.delete(2.0, tk.END)  # Clear previous content
        self.Listname.insert(tk.END, f"\n{process_list}")

    def Btn_open_command(self):
        # open process
        try:
            subprocess.Popen([r"C:\Playpark\Yulgang\launcher.exe"])
            self.Listname.insert(tk.END, f"\nOpen YG")
        except:
            self.Listname.insert(tk.END, f"\nAn exception occurred")

    @staticmethod
    def sort_windows_by_title(windows):  # Make it a static method
        return sorted(windows, key=lambda x: x[1])

    @staticmethod
    def move_windows_to_right(windows):  # Make it a static method
        title_windows = "YGOnline"
        current_x = 0
        current_y = 0
        for hwnd, title in windows:
            if title_windows in title:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, current_x, current_y, 0, 0,
                                      win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                current_x += 50
                current_y += 25
                time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
