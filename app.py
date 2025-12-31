## === IMPORTS === ##
import eel
from pathlib import Path
import os
import json
import subprocess
import serial.tools.list_ports
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import traceback
import platform
import base64
from io import BytesIO
from PIL import Image
import signal
import sys
import pty
import select
import threading
import fcntl
import termios
import struct
import pexpect
import ptyprocess
import serial
import time
import getpass


## === GLOABAL VARS === ##

FOLDER = os.getcwd()
NFOLDER = os.path.join(FOLDER, 'Notes')
DFOLDER = os.path.join(FOLDER, 'Dict')
WFOLDER = 'web'
IFOLDER = os.path.join(WFOLDER, 'img')
os.makedirs(IFOLDER, exist_ok=True)
root = tk.Tk()
root.withdraw()
status = False
available = False
i = 0
si = 0
si_lock = threading.Lock()



#test

class idecmds():
    @staticmethod
    def pull(file):
        filepath = os.path.join(NFOLDER, file)
        if os.path.isfile(filepath):
            idecmds.pullJson_extract(filepath)
    @staticmethod
    def pullJson_extract(file):
        with open(file, 'r') as f:
            ....
            
## === FUNCTIONS === ##

def open_native_folder_dialog():
    system = platform.system()  # 'Linux', 'Windows', 'Darwin' (macOS)
    
    # --- Linux ---
    if system == "Linux":
        # Try GNOME
        if shutil.which("zenity"):
            result = subprocess.run(['zenity', '--file-selection', '--directory'], capture_output=True, text=True)
        # Try KDE
        elif shutil.which("kdialog"):
            result = subprocess.run(['kdialog', '--getexistingdirectory'], capture_output=True, text=True)
        else:
            # fallback to Tkinter
            root = tk.Tk()
            root.withdraw()
            result_path = filedialog.askdirectory()
            root.destroy()
            return result_path if result_path else None

        if result.returncode == 0:
            return result.stdout.strip()
        return None

    # --- Windows ---
    elif system == "Windows":
        root = tk.Tk()
        root.withdraw()
        result_path = filedialog.askdirectory()
        root.destroy()
        return result_path if result_path else None

    # --- macOS ---
    elif system == "Darwin":
        try:
            # AppleScript for native folder selection
            script = 'POSIX path of (choose folder)'
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            # fallback to Tkinter
            root = tk.Tk()
            root.withdraw()
            result_path = filedialog.askdirectory()
            root.destroy()
            return result_path if result_path else None

    else:
        # Unknown system → fallback to Tkinter
        root = tk.Tk()
        root.withdraw()
        result_path = filedialog.askdirectory()
        root.destroy()
        return result_path if result_path else None

def open_native_file_dialog():
    system = platform.system()  # 'Linux', 'Windows', 'Darwin' (macOS)
    
    # --- Linux ---
    if system == "Linux":
        # Try GNOME
        if shutil.which("zenity"):
            result = subprocess.run(['zenity', '--file-selection'], capture_output=True, text=True)
        # Try KDE
        elif shutil.which("kdialog"):
            result = subprocess.run(['kdialog', '--getopenfilename'], capture_output=True, text=True)
        else:
            # fallback to Tkinter
            root = tk.Tk()
            root.withdraw()
            result_path = filedialog.askopenfilename()
            root.destroy()
            return result_path if result_path else None

        if result.returncode == 0:
            return result.stdout.strip()
        return None

    # --- Windows ---
    elif system == "Windows":
        root = tk.Tk()
        root.withdraw()
        result_path = filedialog.askopenfilename()
        root.destroy()
        return result_path if result_path else None

    # --- macOS ---
    elif system == "Darwin":
        try:
            # Try using AppleScript for native dialog
            script = 'POSIX path of (choose file)'
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            # fallback to Tkinter
            root = tk.Tk()
            root.withdraw()
            result_path = filedialog.askopenfilename()
            root.destroy()
            return result_path if result_path else None

    else:
        # Unknown system → fallback
        root = tk.Tk()
        root.withdraw()
        result_path = filedialog.askopenfilename()
        root.destroy()
        return result_path if result_path else None

def open_native_pic_file_dialog():
    system = platform.system()  # 'Linux', 'Windows', 'Darwin' (macOS)

    # --- Allowed extensions ---
    allowed_extensions = "*.jpeg *.jpg *.png *.bmp *.svg *.webp *.tiff *.tif"
    file_types = [("Image files", allowed_extensions)]

    # --- Linux ---
    if system == "Linux":
        # Try GNOME
        if shutil.which("zenity"):
            result = subprocess.run(
                ['zenity', '--file-selection', '--file-filter=Images | *.jpeg *.jpg *.png *.bmp *.svg *.webp *.tiff *.tif'],
                capture_output=True, text=True
            )
        # Try KDE
        elif shutil.which("kdialog"):
            result = subprocess.run(
                ['kdialog', '--getopenfilename', '.', '*.jpeg *.jpg *.png *.bmp *.svg *.webp *.tiff *.tif'],
                capture_output=True, text=True
            )
        else:
            # fallback to Tkinter
            root = tk.Tk()
            root.withdraw()
            result_path = filedialog.askopenfilename(filetypes=file_types)
            root.destroy()
            return result_path if result_path else None

        if result.returncode == 0:
            return result.stdout.strip()
        return None

    # --- Windows ---
    elif system == "Windows":
        root = tk.Tk()
        root.withdraw()
        result_path = filedialog.askopenfilename(filetypes=file_types)
        root.destroy()
        return result_path if result_path else None

    # --- macOS ---
    elif system == "Darwin":
        try:
            # AppleScript with filter not supported natively; filter manually after selection
            script = 'POSIX path of (choose file)'
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if result.returncode == 0:
                path = result.stdout.strip()
                if path.lower().endswith(('.jpeg', '.jpg', '.png', '.bmp', '.svg', '.webp', '.tiff', '.tif')):
                    return path
                return None
        except:
            # fallback to Tkinter
            root = tk.Tk()
            root.withdraw()
            result_path = filedialog.askopenfilename(filetypes=file_types)
            root.destroy()
            return result_path if result_path else None

    else:
        # Unknown system → fallback
        root = tk.Tk()
        root.withdraw()
        result_path = filedialog.askopenfilename(filetypes=file_types)
        root.destroy()
        return result_path if result_path else None


def open_native_file_ports_dialog(multiple=False):
    """
    Opens a native file dialog for uploading files.
    
    Args:
        multiple (bool): If True, allow selecting multiple files.
        
    Returns:
        str or list[str] or None: Path(s) of selected file(s), or None if cancelled.
    """
    system = platform.system()  # 'Linux', 'Windows', 'Darwin' (macOS)

    # --- Linux ---
    if system == "Linux":
        # Try GNOME
        if shutil.which("zenity"):
            cmd = ['zenity', '--file-selection']
            if multiple:
                cmd.append('--multiple')
                cmd.append('--separator=:')  # custom separator
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                files = result.stdout.strip()
                return files.split(':') if multiple else files
            return None
        
        # Try KDE
        elif shutil.which("kdialog"):
            cmd = ['kdialog', '--getopenfilename']
            if multiple:
                cmd.append('--multiple')
                cmd.append('--separate-output')
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                files = result.stdout.strip()
                return files.split('\n') if multiple else files
            return None

    # --- Windows & macOS fallback (Tkinter) ---
    root = tk.Tk()
    root.withdraw()
    if multiple:
        result = filedialog.askopenfilenames()
        root.destroy()
        return list(result) if result else None
    else:
        result = filedialog.askopenfilename()
        root.destroy()
        return result if result else None



## === EXPOSED FUNCTIONS === ##

@eel.expose
def log(file, info, other, err=False):
    if jsonmanager('g', 'app', 'log') == "off":
        return
    elif jsonmanager('g', 'app', 'log') == "error":
        if not(err):
            return
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global i
    i = i + 1
    msg = f" ${i} ${file} ${info}  ${other} ${err}"
    log_file_path = os.path.join(FOLDER, "notes.txt")
    with open(log_file_path, 'a', encoding='utf-8') as f:
        f.write(msg + "\n")

@eel.expose
def openFolder():
    file_path = open_native_folder_dialog()
    with open('data/info.json', 'r') as f:
        data = json.load(f)
    data['LastWorkspace'] = file_path
    log('py', '', data)
    with open('data/info.json', 'w') as f:
        json.dump(data, f, indent=4)
    log("py", f"successfully gave {file_path}", "")
    return {"success": True, "path": file_path}

@eel.expose
def openFile():
    try:
        file_path = open_native_file_dialog()
        log("py", f"successfully gave {file_path}", "")
        return {"success": True, "path": file_path}
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "message": str(e)}

@eel.expose
def saveFile(content, file_path):
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return {"success": True}
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "message": str(e)}



@eel.expose
def listFiles(directory):
    try:
        objects = []
        for obj in os.listdir(directory):
            obj_path = os.path.join(directory, obj)
            if os.path.isfile(obj_path):
                objects.append({"name": obj, "type": "file", "path": obj_path})
            else:
                objects.append({"name": obj, "type": "folder", "path": obj_path})
        log('py', 'sent dicts', objects)
        return {"success": True, "files": objects} 
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "error": str(e)}

@eel.expose
def loadFile(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return {"success": True, "content": content}
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "message": str(e)}

@eel.expose
def makeFile(path, fileName):
    try:
        file_path = os.path.join(path, fileName)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Lets get to coding!")
            log('py', 'Made file at:', file_path)
        return {"success": True}
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "message": str(e)}

@eel.expose
def makeNewFolder(path):
    try:
        folder_path = os.path.join(path, "NewFolder")
        os.makedirs(folder_path, exist_ok=True)
        return {"success": True}
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "message": str(e)}

@eel.expose
def readFile(path, name):
    try:
        with open(path, 'r') as f:
            content = f.read()
            log('py', '', 'here')
            log('py', '', content)
        filename = os.path.basename(path) 
        ext = filename.split('.')[-1].lower()
        language = None
        match ext:
            case "py":
                language = "python"
            case "js":
                language = "javascript"
            case "ts":
                language = "typescript"
            case "java":
                language = "java"
            case "c":
                language = "c"
            case "cpp" | "cc" | "cxx":
                language = "cpp"
            case "html" | "htm":
                language = "html"
            case "css":
                language = "css"
            case "json":
                language = "json"
            case "rs":
                language = "rust"
            case "go":
                language = "go"
            case "bash":
                language = "shell"
            case _:
                language = "text"
        log('py', 'extension', language)
        return {"success": True, "content": content, "language": language}
    except Exception as e:
        trace = traceback.format_exc()
        log('py', e, trace, True)
        return {"success": False, "error": str(e)}

@eel.expose
def renameFile(newName, oldPath, oldName=''):
    log('py', 'rename', 'Came')
    log('py', 'rename got', f"{newName}, {oldName}, {oldPath}")
    try:
        if oldPath == 'NFOLDER':
            global NFOLDER
            oldPath = NFOLDER
            log('py', 'dict', oldPath)
            newPath = os.path.join(oldPath, newName)
            oldPath = os.path.join(oldPath, oldName)
            log('py', '', newPath)
            os.rename(oldPath, newPath)
            return {"success": True, "newPath": newPath}
   
        elif oldPath == 'DFOLDER':
            global DFOLDER
            oldPath = DFOLDER
            log('py', 'dict', oldPath)
            newPath = os.path.join(oldPath, newName)
            oldPath = os.path.join(oldPath, oldName)
            log('py', '', newPath)
            os.rename(oldPath, newPath)
            return {"success": True, "newPath": newPath}

        directory = os.path.dirname(oldPath)
        newPath = os.path.join(directory, newName)
        log('py', '', newPath)
        os.rename(oldPath, newPath)
        log('py', '', newPath)
        return {"success": True, "newPath": newPath}
    except Exception as e:
        return {"success": False, "message": str(e)}

@eel.expose
def deleteFile(path):
    try:
        os.remove(path)
        return {"success": True}
    except IsADirectoryError:
        shutil.rmtree(path)
        return {"success": True}
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "message": str(e)}

## == Notes == ##

@eel.expose
def newNote(fileName):
    if not fileName:
        return {"success": False, "error": "No file name provided"}

    try:
        file_path = os.path.join(NFOLDER, fileName)
        with open(file_path, 'w') as f:
            f.write(
                f"Write anything here then copy it to your many project (anytime, anywhere) "
                f"by writing\n notes.bring('{fileName}')"
            )
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

    finally:
        return {"success": True}




@eel.expose
def listNotes():
    notes = []
    try:
        for note in os.listdir(NFOLDER):
            path = os.path.join(NFOLDER, note)
            notes.append({"name": note, "path": path})
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "error": str(e)}
    return {"success": True, "Notes": notes}

@eel.expose
def saveNote(name, content):
    try:
        path = os.path.join(NFOLDER, name)
        with open(path, 'w') as f:
            f.write(content)
        return {"success": True}
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "w": str(e)}

## == Dict == ##

@eel.expose
def listDict():
    dictionary = []
    try:
        for dic in os.listdir(DFOLDER):
            path = os.path.join(DFOLDER, dic)
            dictionary.append({"name": dic, "path": path})
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "error": str(e)}
    return {"success": True, "Dict": dictionary}

@eel.expose
def saveDict(name, content):
    try:
        path = os.path.join(DFOLDER, name)
        with open(path, 'w') as f:
            f.write(content)
        return {"success": True}
    except Exception as e:
        trace = traceback.format_exc()
        log("py", e, trace, True)
        return {"success": False, "w": str(e)}

@eel.expose
def newDict(fileName):
    try:
        file_path = os.path.join(DFOLDER, fileName)
        with open(file_path, 'w') as f:
            f.write(
                f"Use the syntax\n"
                f"function() | description\n"
                f"to make your dictionaries then insert them for example\n"
                f"print() | to output\n"
                f"then you can use notes.info({fileName}) to get the dicts"
            )
        return {"success": True}
    except Exception as e:
        log('py', 'at newDict', e, True)
        return {"success": False, "error": str(e)}

## == Circuit Viewer == ##

@eel.expose
def displayPic():
    for fn in os.listdir(IFOLDER):
        os.remove(os.path.join(IFOLDER, fn))

    filePath = open_native_pic_file_dialog()
    if not filePath:
        return {"success": False, "error": "Canceled request"}

    filename = os.path.basename(filePath)
    Ipath = os.path.join(IFOLDER, filename)
    shutil.copy(filePath, IFOLDER)
    log('py', Ipath, '\n')
    return {"success": True, "img": f"img/{filename}"}

## == Ports == ##


serials = set()

@eel.expose
def UploadToDevice(chip, port, firmware):
    with open("data/mcu.json", 'r') as f:
        file = json.load(f)
    cmd = file[chip]["upload_command"]
    cmd = cmd.replace("{port}", port).replace("{file}", firmware)
    if chip == "RP2040":
        cmd = cmd.replace("$(whoami)", getpass.getuser())
    log("py", "COMMAND:", cmd)

@eel.expose
def readDevice(port_in, baud):
    if port_in in serials:
        return

    serials.add(port_in)

    ser = serial.Serial(
        port=port_in,
        baudrate=baud,
        timeout=1
    )

    try:
        while port_in in serials:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                eel.spawn(eel.portData(f'{port_in}: {line}'))
    finally:
        ser.close() 

@eel.expose
def stopread(port_in):
    serials.discard(port_in)



## == Terminal == ##

virtual_cwd = os.getcwd()
home_dir = os.path.expanduser("~")  # For ~ support
shell = None


@eel.expose
def run_command(cmd, sudo_password=""):
    global virtual_cwd
    try:
        # handle 'cd'
        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            path = os.path.expanduser(path)
            if not os.path.isabs(path):
                path = os.path.join(virtual_cwd, path)
            if os.path.isdir(path):
                virtual_cwd = os.path.abspath(path)
                return {"ok": True, "output": virtual_cwd}
            else:
                return {"ok": False, "output": f"No such directory: {path}"}

        # sudo commands
        if cmd.startswith("sudo"):
            process = subprocess.Popen(
                cmd,
                shell=True,
                executable=shell,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=virtual_cwd
            )
            stdout, stderr = process.communicate(sudo_password + "\n")
            if process.returncode != 0:
                return {"ok": False, "output": stderr.strip()}
            return {"ok": True, "output": stdout.strip()}

        # normal commands
        output = subprocess.check_output(
            cmd,
            shell=True,
            executable=shell,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=virtual_cwd
        )
        return {"ok": True, "output": output.strip()}

    except subprocess.CalledProcessError as e:
        return {"ok": False, "output": e.output.strip()}


@eel.expose
def get_cwd():
    return virtual_cwd



## == Ports ==##

def next_id():
    global si
    with si_lock:
        si += 1
        return si
    
@eel.expose
def getPorts():
    active_ports = []
    ports = serial.tools.list_ports.comports()

    for port in ports:
        try:
            # Try to open and immediately close the port
            s = serial.Serial(port.device)
            s.close()
            active_ports.append(port.device)
        except (OSError, serial.SerialException):
            pass
    return {"success": True, "ports": active_ports}

@eel.expose
def readPort(port, baud):
    def reader():
        try:
            ser = serial.Serial(port, baud, timeout=1)
            while True:
                if ser.in_waiting:
                    line = ser.readline().decode(errors="ignore").strip()
                    line = f"{next_id()}$ {line}"
                    log('py', 'Line:', line)
                    eel.spawn(eel.Out, line)
        except Exception as e:
            eel.spawn(eel.Out, str(e), True)
            log('py', "got error:", e, True)
    
    threading.Thread(target=reader, daemon=True).start()

@eel.expose
def upload(port, baud, firmware):
    def uploader():
        try:
            ser = serial.Serial(port, baud)
            with open(firmware, 'rb') as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    ser.write(chunk)
                    ser.flush()
                    time.sleep(0.01)
            eel.spawn(eel.Out, "Upload complete.")
        except Exception as e:
            eel.spawn(eel.Out, str(e), True)
            log('py', 'got error', e, True)

    threading.Thread(target=uploader, daemon=True).start()


@eel.expose
def test():
    for i in range(1, 300):
        line1 = f"{next_id()}$ Test output"
        line2 = f"{next_id()}$ Test fail"
        eel.spawn(eel.Out, line1)
        eel.spawn(eel.Out, line2, True)

## == Settings == ##


@eel.expose
def jsonmanager(proc, grp="", subgrp="", setto=""):
    with open("data/settings.json", 'r') as f:   
        data = json.load(f)
    if proc == 'g':
        value = data[grp][subgrp]
        return value
    
    elif proc == 's':
        data[grp][subgrp] = setto
        with open("data/settings.json", 'w') as f:
            json.dump(data, f, indent= 4)
        return {"success": True}
    elif proc == 'ga':
        return data

@eel.expose
def getLastWorkspace():
    with open('data/info.json', 'r') as f:
        data = json.load(f)
    path = data['LastWorkspace']
    return path

@eel.expose
def getKeybinds():
    with open('data/keybinds.json', 'r') as f:
        return json.load(f)
    
@eel.expose
def s(name, val, subgrp=""):
    with open('data/keybinds.json', 'r') as f:
        data = json.load(f)

    if subgrp == "":
        # If data[name] exists and is a dict, merge instead of overwrite
        if name in data and isinstance(data[name], dict) and isinstance(val, dict):
            data[name].update(val)
        else:
            data[name] = val
    else:
        if name not in data or not isinstance(data[name], dict):
            data[name] = {}
        data[name][subgrp] = val

    with open('data/keybinds.json', 'w') as f:
        json.dump(data, f, indent=4)


@eel.expose
def deleteKey(name):
    with open('data/keybinds.json', 'r') as f:
        data = json.load(f)
    
    del data[name]

    with open('data/keybinds.json', 'w') as f:
        json.dump(data, f, indent=4)

@eel.expose
def addKey(name, key, action):
    with open('data/keybinds.json', 'r') as f:
        data = json.load(f)
    data[name] = {
        "keyBind": key,
        "command": action
    }
    with open('data/keybinds.json', 'w') as f:
        json.dump(data, f, indent=4)

@eel.expose
def startshell(currentdict):
    global shell
    system = platform.system()
    shell_setting = jsonmanager('g', 'terminal', 'Shell')

    if shell_setting.lower() == "auto":
        if system in ("Linux", "Darwin"):
            shell = os.environ.get("SHELL", "/bin/bash")

        elif system == "Windows":
            shell = (
                shutil.which("pwsh")
                or shutil.which("powershell")
                or shutil.which("cmd")
                or r"C:\Windows\System32\cmd.exe"
            )

    else:
        if system == "Windows":
            if shell_setting.lower() == "cmd":
                shell = r"C:\Windows\System32\cmd.exe"
            elif shell_setting.lower() in ("powershell", "pwsh"):
                shell = (
                    shutil.which(shell_setting)
                    or r"C:\Program Files\PowerShell\7\pwsh.exe"
                )
            else:
                shell = r"C:\Windows\System32\cmd.exe"
        else:
            shell = f"/bin/{shell_setting}"

    log("py", "SHELL", shell)
    run_command(f"cd {currentdict}")


eel.init(WFOLDER)
eel.start('index.html', size=(1200, 800), port=0)


