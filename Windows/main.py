import subprocess
import psutil
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter.messagebox import askyesno


class KeylogDetector:

    def __init__(self, master):
        self.whitelist = []
        self.whitelist_ip = ['127.0.0.1', '0.0.0.0']
        self.blacklist = []
        self.blacklist_ip = []
        self.source_ip = []
        self.grouped_output = None
        self.skip_print = False
        self.output = None
        self.stop_gui = None
        self.gui = master
        self.timer = 1
        gui.geometry('700x460')
        master.title("Keylog Detector")

        self.l1 = Label(master, text="Click To Start")
        self.l1.pack()

        self.out_btn = Button(master, text="Listen", command=self.show_output)
        self.out_btn.place(x=150, y=25)

        self.out_stp = Button(master, text="Stop", command=self.stop_output)
        self.out_stp.place(x=550, y=25)

        self.out_box = scrolledtext.ScrolledText(master, height=20, width=80)
        self.out_box.pack(pady=40)

        self.clear_chat = Button(master, text="Clear", command=self.new_window)
        self.clear_chat.pack()

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
            # group output by whitespace to extract data (IP, port, etc.)
            self.grouped_output = self.output.split(" ")
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
        my_list = self.grouped_output
        # delete empty array elements
        my_list = list(filter(None, my_list))
        # obtain IP with port number
        ip_addr = my_list[-3]
        # separate IP from port
        get_ip = ip_addr.split(":")
        # assign IP to check if this exists in whitelist_ip
        ip = [get_ip[0]]
        # if yes, do not print output or go to run_keylog and continue scanning
        if set(ip).issubset(set(self.whitelist_ip)):
            self.skip_print = True

    def stop_output(self):
        self.out_box.insert(INSERT, "\nScanning stopped.\n\n")
        gui.after_cancel(self.stop_gui)
        self.timer = 1
        self.out_box.see(END)

    def run_keylog(self):
        my_list = self.grouped_output
        # delete empty array elements
        my_list = list(filter(None, my_list))
        # PID will be the last number once split
        pid = my_list[-1]
        # get application name using PID
        cmd_output = subprocess.getoutput(f'tasklist /fi "pid eq {pid}"')
        # split to obtain process name
        process_name = cmd_output.split()
        # identify source_ip to prevent the same application from showing twice in output
        if my_list[-3] not in self.source_ip:
            self.source_ip.append(my_list[-3])
        # get the full IP address with port number from the last element from output
        ip_addr = my_list[-3]
        # split at the ':' to get port number at last index of array
        get_port = ip_addr.split(":")
        port = get_port[-1]
        # process name is always 13th element in array.
        process_name = process_name[13]
        p = psutil.Process(int(pid))

        if process_name not in self.whitelist:
            self.out_box.insert(INSERT, "\nKeylogger Detected.\n\n")
            # terminate process if it exists in blacklist
            if process_name in self.blacklist:
                p.kill()
                self.out_box.insert(INSERT, "Blacklist application found running.\nProcess automatically "
                                            "terminated.\n\n")
                self.timer = 1
                self.show_output()

            # if process is not in whitelist, check if it should be
            else:
                self.out_box.insert(INSERT, "Pausing application...\n\n")
                p.suspend()
                self.out_box.insert(INSERT, f'Application name: {process_name}\n'
                                            f'Process ID (PID): {pid}'
                                            f'Trying to communicate on port {port}\n')
                self.out_box.see(END)

                is_safe = askyesno(title='Confirmation',
                                   message="Process marked as dangerous.\nWould you like to add this application to "
                                           "your whitelist?")
                if is_safe:
                    self.out_box.insert(INSERT, "Resuming process...\n")
                    p.resume()
                    self.out_box.insert(INSERT, "Adding to whitelist...\n\n")
                    self.whitelist.append(process_name)
                    self.whitelist_ip.append(ip_addr)
                else:
                    self.out_box.insert(INSERT, "Terminating process...\n")
                    p.kill()
                    self.out_box.insert(INSERT, "Adding to blacklist...\n\n")
                    self.blacklist.append(process_name)
                    self.blacklist_ip.append(ip_addr)

                self.out_box.insert(INSERT, f'whitelist: {self.whitelist}\n')
                self.out_box.insert(INSERT, f'blacklist: {self.blacklist}\n\n')
                self.out_box.see(END)
                self.timer = 1
                self.show_output()

        # whitelisted program needs to go back to showing output
        else:
            self.show_output()


gui = Tk()
run_app = KeylogDetector(gui)
gui.mainloop()
