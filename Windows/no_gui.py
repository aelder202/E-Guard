import os
import shutil
import subprocess
from os.path import exists

import psutil
import getopt
import sys

time = 1
black_list = []
white_list = []
short_options = "har"
long_options = ["help", "add-to-startup", "remove-from-startup"]
# remove 1st argument from list of arguments
argumentList = sys.argv[1:]

if argumentList:
    try:
        arguments, values = getopt.getopt(argumentList, short_options, long_options)
        for opt, arg in arguments:
            if opt in ('-h', "--help"):
                print("Available arguments:\n"
                      "-h/--help  Shows this menu\n"
                      "-a/--add-to-startup  Adds program to startup directory\n"
                      "-r/--remove-from-startup  Removed program from startup.")
            elif opt in ('-a', "--add-to-startup"):
                file_exists = exists("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\E-Guard.exe")
                if not file_exists:
                    # get current path of file
                    src_path = f'{os.getcwd()}\\GUI\\E-Guard.exe'
                    dest_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\E-Guard.exe"
                    # copy source to destination
                    shutil.copy(src_path, dest_path)
                    # re-check if file exists, then print to screen results
                    file_exists = exists("C:\\ProgramData\\Microsoft\\Windows\\Start "
                                         "Menu\\Programs\\StartUp\\E-Guard.exe")
                    if file_exists:
                        print("Program successfully added to startup.")
                    else:
                        print("Error: Program did not load into startup folder.")
                else:
                    print("Error: Program already exists in startup.")
            elif opt in ('-r', "--remove-from-startup"):
                file_exists = exists("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\E-Guard.exe")
                if file_exists:
                    os.remove("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\E-Guard.exe")
                    file_exists = exists("C:\\ProgramData\\Microsoft\\Windows\\Start "
                                         "Menu\\Programs\\StartUp\\E-Guard.exe")
                    if not file_exists:
                        print("File removed successfully.")
                    else:
                        print("Error: File was not removed from startup.")
                else:
                    print("Error: Program does not exist in startup directory.")

    except (getopt.error, IOError) as err:
        # output error and return error code
        print("Error: Make sure you are running the terminal as an administrator.")
else:
    while True:
        if time == 1:
            print("\nScanning in progress...")
        proc = subprocess.Popen('netstat -ano -p tcp | findStr "587 465 2525"', shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        out, err = proc.communicate()

        output = out.decode()

        my_list = output.split(" ")
        # PID will be the last number once split
        pid = my_list[-1]
        # obtain output from checking the application name of PID
        cmd_output = subprocess.getoutput(f'tasklist /fi "pid eq {pid}"')
        # to make finding process name easier, split cmd_output
        process_name = cmd_output.split()

        time += 1
        if "ESTABLISHED" in output:
            # delete empty array elements
            my_list = list(filter(None, my_list))
            # get the full IP address with port number from the last element from output
            port_num = my_list[-3]
            # split at the ':' to get port number at last index of array
            get_port = port_num.split(":")
            port = get_port[-1]

            # debugging
            # print(my_list)
            # print(pid)
            # print(process_name)

            # 13th element in process_name will always be application name
            process_name = process_name[13]
            p = psutil.Process(int(pid))

            if process_name not in white_list:
                print("KEYLOGGER DETECTED!")

                # terminate process if it exists in blacklist
                if process_name in black_list:
                    p.kill()
                    print("Blacklist application found running.\nProcess automatically terminated.")
                    time = 1
                # if process is not in whitelist, check if it should be
                elif process_name not in white_list:
                    print("Pausing application...\n")
                    p.suspend()
                    print("Information on application identified in your system to be potential threat...")
                    print(f'Application name: {process_name}\n'
                          f'Process ID (PID): {pid}'
                          f'Trying to communicate on port {port}\n')
                    selected = False
                    while not selected:
                        is_safe = input("Would you like to whitelist this application? (Y/N): ").lower()
                        if is_safe == 'n':
                            print("Terminating process...")
                            p.kill()
                            print("Adding to blacklist...")
                            black_list.append(process_name)
                            selected = True
                            time = 1
                        elif is_safe == 'y':
                            print("Resuming process...")
                            p.resume()
                            print("Adding to whitelist...")
                            white_list.append(process_name)
                            selected = True
                            time = 1

                        print("whitelist:", white_list)
                        print("blacklist:", black_list)
