# E-Guard Keylogger Detector
E-Guard is an open-source keylogger detection application which alerts users to applications attempting to send out 
information through popular SMTP servers.

## How It Works
This program focuses on combating keylogger software by monitoring all running applications, 
targeting those attempting to communicate through popular SMTP ports for Gmail, Yahoo, ATT, 
Microsoft, and AOL for both Windows and Linux machines. 

Once the software has targeted an application that is communicating through specific SMTP ports, 
the process will be paused, and the user will be notified of the potential threat. Then, the 
user will be asked if this process should be added to a trusted whitelist to continue running 
as normal or kill the process immediately and be added to a blacklist so that any other time this 
process is detected it will be automatically terminated.

## Monitored SMTP Ports
| **SMTP Ports** | **E-mail Service**    |
|----------------|-----------------------|
| 587            | Gmail, Microsoft, AOL |
| 465            | Yahoo, Live           |
| 2525           | Other                 |

## How to Run

### Windows - *Requires administrator privileges*


**Important note**

*Trojan:Win32/Wacatac.B!ml false positives*

* In order to add 'Add/Remove Program to Startup' feature for Windows, auto_py_to_exe was used to convert `main.py` into an executable file. This process is creating a file that is being mark as malicious by most antivirus software. I am currently looking into other ways to create an executable file from the python file, or another way to launch a python file at startup on Windows.

* Feel free to use [VirusTotal](https://www.virustotal.com) to check the python file yourself before execution.


1. Download and install [python](https://www.python.org/downloads/)
2. Install any python package-management system, such as `pip`. To install `pip`, follow the commands below:
   ```
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   ```
   ```
   python get-pip.py
   ```
   Confirm installation using the following command:
   ```
   pip --version
   ```
3. Visit [psutil](https://pypi.org/project/psutil/) to download and install this package, or use any python package-management system, such as pip, to install using the following command:
   ```
   pip install psutil
   ```
4. Clone this repository using GitHub Desktop application.
5. Navigate to `Windows/GUI` directory
6. Execute `E-Guard` application and select `Listen` to begin running the application.

### Linux
1. Ensure Python 3.x is installed by checking 
   ```
   python3 --version
   ```
   Install by using the following command:
   ```
   sudo apt install python3.x
   ```
2. Install ``psuitl`` by using the following command: 
   ```
   sudo apt install python3-psutil
   ```
3. Clone this repository by using the following command:
   ```
   git clone https://github.com/aelder202/E-Guard.git
   ```
4. Navigate to `Linux` directory
5. To begin running the application, use the following command:
   ```
   python3 no_gui_linux.py
   ```

## Arguments

#### Windows
Open a command prompt window and navigate to the directory containing the cloned repository. Next,
`cd` into `Windows` and use 
```
python no_gui.py -h
```
or
```
python no_gui.py --help
```
for a list of available arguments.

### Linux
Open a terminal window and navigate to the directory containing the cloned repository. Next,
`cd` into `Linux` and use
```
python3 no_gui_linux.py -h
```
or
```
python3 no_gui_linux.py --help
```
for a list of available arguments.

## Screenshots

### Windows
 ![Threat Detected](screenshots/gui_threat.png "Threat Detected")
 ![Blacklist](screenshots/gui_show_blacklist.png "Blacklist")
 ![Whitelist](screenshots/gui_show_whitelist.png "Whitelist")
 ![Add To Startup](screenshots/gui_startup.png "Add To Startup")
 ![Save Output](screenshots/gui_save_output.png "Save Output")

### Linux
 ![Threat Detected](screenshots/linux_threat.png "Threat Detected")
 ![Add to startup](screenshots/linux_startup.png "Add program to startup")
