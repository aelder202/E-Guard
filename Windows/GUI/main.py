"""
Main GUI class to run E-Guard Keylogger Detector.
Creates simple GUI using tkinter to listen for applications
communicating with popular SMTP servers. Once an application
is detected as a potential threat, the user is notified and
given the option to add the program to a trusted whitelist to
continue running as normal or added to a blacklist, terminating
the application instantly and any other time it is detected.
"""
import ctypes
import sys
import os
from os.path import exists
import shutil
import subprocess
import psutil
from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from tkinter.messagebox import askyesno
import os.path


class KeyloggerDetector:

    def __init__(self, master):
        self.whitelist = []
        self.whitelist_ip = ['127.0.0.1', '0.0.0.0']
        self.blacklist = []
        self.blacklist_ip = []
        self.source_ip = ['127.0.0.1', '0.0.0.0']
        self.process_name = None
        self.grouped_output = None
        self.skip_print = False
        self.output = None
        self.stop_gui = None
        self.p = psutil.Process()
        self.gui = master
        self.timer = 1
        gui.geometry('700x530')
        master.title("E-Guard Keylogger Detector")

        self.out_btn = Button(master, text="Listen", command=self.show_output)
        self.out_btn.place(x=150, y=25)

        self.out_stp = Button(master, text="Stop", command=self.stop_output)
        self.out_stp.place(x=550, y=25)

        self.out_stp = Button(master, text="Add Program to Startup", command=startup)
        self.out_stp.place(x=305, y=0)

        self.out_stp = Button(master, text="Remove Program from Startup", command=remove)
        self.out_stp.place(x=285, y=30)

        self.out_box = scrolledtext.ScrolledText(master, height=25, width=80)
        self.out_box.pack(padx=10, pady=10, expand=True)

        self.clear_chat = Button(master, text="Clear", command=self.new_window)
        self.clear_chat.place(x=350, y=480)

        gui.after(1000)

    def new_window(self):
        self.out_box.delete('1.0', END)
        self.timer = 1

    def show_output(self):
        self.skip_print = False

        if self.timer == 1:
            self.out_box.insert(INSERT, "Scanning in progress...\n\n")
            self.timer += 1
        # main powershell command
        proc = subprocess.Popen('netstat -ano -p tcp | findStr "587 465 2525"', shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        out, err = proc.communicate()
        # decode() loads single character from output into list
        self.output = out.decode()
        # stop show_output for 1 second before calling itself again  << double check this
        self.stop_gui = gui.after(100, self.show_output)
        if "ESTABLISHED" in self.output:
            self.grouped_output = self.output.split(" ")
            # delete empty array elements
            self.grouped_output = list(filter(None, self.grouped_output))
            # let application terminate if it exists in blacklist
            if self.process_name in self.blacklist:
                self.stop_output()
                self.run_keylog()
            # make sure the source_ip hasn't been printed to console more than once
            if not any(x in self.source_ip for x in self.grouped_output):
                # check if the IP has been logged in whitelist_ip
                self.check_list()
                if not self.skip_print:
                    self.out_box.insert(INSERT, self.output)
                    self.stop_output()
                    self.run_keylog()
        # autoscroll feature
        self.out_box.see(END)

    def check_list(self):
        # if IP is in whitelist, go back to the beginning of show_output
        ip_addr = self.grouped_output[-3]
        # separate IP from port
        get_ip = ip_addr.split(":")
        # assign IP to check if this exists in whitelist_ip
        ip = [get_ip[0]]
        # if yes, do not print output or go to run_keylog and continue scanning
        if any(x in ip for x in self.whitelist_ip):
            self.skip_print = True

    def stop_output(self):
        self.out_box.insert(INSERT, "\nScanning stopped.\n\n")
        gui.after_cancel(self.stop_gui)
        self.timer = 1
        self.out_box.see(END)

    def run_keylog(self):
        pid = self.grouped_output[-1]
        # get application name using PID
        cmd_output = subprocess.getoutput(f'tasklist /fi "pid eq {pid}"')
        # split to obtain process name
        self.process_name = cmd_output.split()
        # identify source_ip to prevent the same application from showing twice in output
        if self.grouped_output[-3] not in self.source_ip:
            self.source_ip.append(self.grouped_output[-3])
        # get the full IP address with port number from the last element from output
        ip_addr = self.grouped_output[-3]
        # split at the ':' to get port number at last index of array
        get_port = ip_addr.split(":")
        port = get_port[-1]
        # process name is always 13th element in array.
        self.process_name = self.process_name[13]
        self.p = psutil.Process(int(pid))

        if self.process_name not in self.whitelist:
            try:
                self.out_box.insert(INSERT, "\nKeylogger Detected.\n\n")
                # terminate process if it exists in blacklist
                if self.process_name in self.blacklist:
                    self.p.kill()
                    self.out_box.insert(INSERT, "Blacklist application found running.\nProcess automatically "
                                                "terminated.\n\n")
                    self.timer = 1
                    self.show_output()

                # if process is not in whitelist, check if it should be
                else:
                    self.out_box.insert(INSERT, "Pausing application...\n\n")
                    self.p.suspend()
                    self.out_box.insert(INSERT, f'Application name: {self.process_name}\n'
                                                f'Process ID (PID): {pid}'
                                                f'Trying to communicate on port {port}\n')
                    self.out_box.see(END)

                    is_safe = askyesno(title='Confirmation',
                                       message="Process marked as dangerous.\nWould you like to add this application "
                                               "to your whitelist?")
                    if is_safe:
                        self.out_box.insert(INSERT, "Resuming process...\n")
                        self.p.resume()
                        self.out_box.insert(INSERT, "Adding to whitelist...\n\n")
                        self.whitelist.append(self.process_name)
                        self.whitelist_ip.append(ip_addr)
                    else:
                        self.out_box.insert(INSERT, "Terminating process...\n")
                        self.p.kill()
                        self.out_box.insert(INSERT, "Adding to blacklist...\n\n")
                        self.blacklist.append(self.process_name)
                        self.blacklist_ip.append(ip_addr)

                    self.out_box.insert(INSERT, f'whitelist: {self.whitelist}\n')
                    self.out_box.insert(INSERT, f'blacklist: {self.blacklist}\n\n')
                    self.out_box.see(END)
                    self.timer = 1
                    self.show_output()

            except psutil.AccessDenied:
                self.out_box.insert(INSERT, "\nApplication requires administrator privileges to stop. Unable to "
                                            "continue.\n")
                self.out_box.insert(INSERT, "Adding to whitelist...\n\n")
                self.whitelist.append(self.process_name)
                self.whitelist_ip.append(ip_addr)
                self.timer = 1
                self.show_output()

        # whitelisted program needs to go back to showing output
        else:
            self.show_output()


# static methods
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def startup():
    file_exists = exists("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\E-Guard.exe")
    if not file_exists:
        # get current path of file
        src_path = f'{os.getcwd()}\E-Guard.exe'
        dest_path = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\E-Guard.exe"
        # copy source to destination
        shutil.copy(src_path, dest_path)
        # re-check if file exists, then print to screen results
        file_exists = exists("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\E-Guard.exe")
        if file_exists:
            messagebox.showinfo("Information", "Program successfully added to startup.")
        else:
            messagebox.showerror("Error", "Program did not load into startup folder.\nPlease try again.")
    else:
        messagebox.showinfo("Information", "Program already exists in startup.")


def remove():
    file_exists = exists("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\E-Guard.exe")
    if file_exists:
        os.remove("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\E-Guard.exe")
        file_exists = exists("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\E-Guard.exe")
        if not file_exists:
            messagebox.showinfo("Information", "File removed successfully.")
        else:
            messagebox.showerror("Error", "Error: File was not removed from startup.")
    else:
        messagebox.showerror("Error", "Error: Program does not exist in startup directory.")


# run program
if is_admin():
    gui = Tk()
    run_app = KeyloggerDetector(gui)
    gui.mainloop()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    # terminate program not ran as admin
    sys.exit(0)
