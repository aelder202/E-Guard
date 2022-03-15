# E-Guard - Keylogger Detector
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

## SMTP servers monitored by E-Guard
| **Popular SMTP Ports** |
|------------------------|
| 587                    |
| 465                    |
| 2525                   |

## How to Run

### Windows - *Requires administrator privileges*
1. Clone this repository using GitHub Desktop application.
2. Navigate to `Windows/GUI` directory
3. Execute `E-Guard` application and select `Listen` to begin running the application.

### Linux
1. Clone this repository
2. Navigate to `Linux` directory
3. Run `python3 no_gui_linux.py` to begin running the application.

## Screenshots


## Arguments

#### Windows
Open a command prompt window and navigate to the directory containing the cloned repository. Next,
`cd` into `Windows` and type `python no_gui.py -h` or `python no_gui.py --help` for a list of 
available arguments.

### Linux
Open a terminal windows and navigate to the directory containing the cloned repository. Next,
`cd` into `Linux` and type `python3 no_gui_linux.py -h` or `python3 no_gui_linux.py --help` for 
a list of available arguments.