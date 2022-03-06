import subprocess
import psutil

time = 1
black_list = []
white_list = []

while True:
    if time == 1:
        print("\nScanning in progress...")

    # example from secure python scripting:
    # proc = subprocess.Popen(["ls -sail sample/" + filename], stdout=subprocess.PIPE, shell=True)
    proc = subprocess.Popen('lsof -nP -iTCP:587 -iTCP:465 -iTCP:2525', stdout=subprocess.PIPE,
                            shell=True)
    out, err = proc.communicate()
    output = out.decode()

    my_list = output.split(" ")

    time += 1
    if "ESTABLISHED" in output:
        # delete empty array elements
        my_list = list(filter(None, my_list))
        # get the full IP address with port number from the last element from output
        port_num = my_list[-2]
        # split at the ':' to get port number at last index of array
        get_port = port_num.split(":")
        port = get_port[-1]

        # debugging
        print(my_list)
        print(port)

        # 13th element in process_name will always be application name
        process_name = my_list[8]
        process_n = process_name.split("\n")
        process_name = process_n[-1]
        pid = my_list[9]
        print(process_n)
        print(pid)

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
