# Noteside-underDev

This is a newer repo for NotesIDE.  
Frequent updates happen here before being merged into the main repo.

This is the source code and should work on most OS's and keep in mind, this is ONLY THE SOURCE CODE THAT SHOULD WORK ON MOST DEVICES. If you need a os specific version of the app, kindly go to [Noteside downlaod page](noteside.vercel.app).

# What i will cover in this in md file

- Overview
- What are the files for
- My purpose
- Why the delay of the README
- features of NotesIDE
- System notes


# Overview

NotesIDE is an ide that has note taking capabilites made for new learners or people who want to use IDEs without bothering about expert programming stuff. It provides a clean UI/UX made using the eel frameworks which uses Python for the backend and web Frontend; a web app. The eel frameworks also allows the app to be lightweight. It uses `Google` for MacOS, `Firefox` for Linux, `Edge` for Windows and `Google` for the open-source version by default.

# What are the files for

The root of this folder
└── NotesIDE/
    ├── data/                  --> Contains data like setting
    │   ├── darkorlight.json   --> Contains dark or light mode CSS stats
    │   ├── default.json       --> Contains default setting
    │   ├── info.json          --> Contains system information
    │   ├── keybinds.json      --> Contains all the custom keybings
    │   └── settings.json      --> Contains all the setting
    ├── Dict/                  --> Contains all dictionaries
    ├── info/                  --> Contains all the md files (besides README.md) DETAILS LATER
    ├── Notes/                 --> Contains all the Notes
    ├── web/                   --> Contains what the browser has to render and stuff/
    │   ├── img/               --> Contains the immage for Circuit viewing
    │   ├── index.html         --> Contains the main html code
    │   ├── keybinds.js        --> Contains the js code for keybinds
    │   ├── render.js          --> Contains the main js code
    │   └── style.css          --> Contains the main css styles
    ├── .gitignore             --> Contains the files i only used for development(.venv and stuff)
    ├── app.py                 --> Contains the backend
    ├── LICENSE                --> Contains the Apache license
    ├── notes.txt              --> Contains the logs
    └── README.md              --> Information point

# My purpose

I made NotesIDE because when I first stated to code, many IDEs was **messy** (way too many **tabs**) and it felt very overwhelming. Therefore this IDE solves all of this by adding an obvious **outer** tab and **inner** tab and a **panel** for information. I also noticed i needed to repeatedly write the **same** lines of code therefore my IDE allows you to copy **repeated** codes just by running **simple commands**. Copying and pasting is good for **small** scale, but **large** scale is bad. I also kept forgetting **keywords** in programming and therefore decided to allow the user to run easy commands to list **keywords** with their **definitions**. The simple **run** button is also help for people who are just starting to learn programming.

# Why the delay of the README

To be transparent, I kept on wanting to change the frameworks and had some ups and downs with the project structure therefore decided to make the readme later. Now that everything is fixed, i can make this README confidently. Additionally, personal life and other projects took over my time so i failed to make the README sooner. But now that its made there is no worries!

# Features of NotesIDE

## Core Editor & Workspace
- **Monaco Editor Integration**: Utilizes the powerful VS Code editor core for a professional coding experience.
- **Multi-tab Interface**: Open and manage multiple files simultaneously in a tabbed view.
- **Hierarchical File Tree**: Navigate project files and folders with an expandable/collapsible tree view.
- **File Drag & Drop**: Move files and folders within the project by dragging and dropping them in the file tree.
- **Workspace Management**: Open, save, and restore entire project workspaces.
- **Auto-save**: Automatically saves files, notes, and dictionaries at a configurable interval.
- **Language Detection**: Automatically applies syntax highlighting based on the file type.

## File Management
- **Create Files & Folders**: Easily create new files (`Ctrl/Cmd + N`) and folders from the UI or context menu.
- **File Operations**: Standard actions like open, rename, delete, and copy file path to clipboard.
- **Recent Workspaces**: Quick-launch functionality to reopen the last active workspace on startup.
- **Save All**: A single command to save all currently open and modified files.

## Notes System
- **Dedicated Note Editor**: A separate, full-featured editor (Monaco-based) for writing and managing notes.
- **YAML Format**: Notes are structured and saved in YAML format for organization and readability.
- **Note Management**: Create, rename, and delete individual notes from a dedicated list.
- **`idecmd.note` Commands**: A special command system (`idecmd.note.pull`, `idecmd.note.push`, etc.) for advanced note operations directly from the editor.

## Dictionary System
- **Dedicated Dictionary Editor**: A separate editor for creating and managing custom dictionaries or glossaries.
- **Searchable Dictionary Popup**: A fast, searchable pop-up interface that allows you to find and insert dictionary entries into your code.
- **Dictionary Management**: Create, rename, and delete dictionaries from a dedicated list.
- **`idecmd.dict` Commands**: A special command system (`idecmd.dict.pull`, `idecmd.dict.push`, etc.) for managing dictionary content.

## Terminal Integration
- **Built-in Terminal**: A fully functional command-line terminal integrated directly into the IDE.
- **Sudo Support**: Securely handles commands that require elevated privileges by prompting for a password.
- **Command History & Output**: Displays a scrollable history of executed commands and their outputs.
- **Terminal Context Menu**: Right-click on any command or its output to copy it to the clipboard.

## Circuit/PCB Features
- **Image Preview**: Load and display circuit diagrams or other images directly within the application.
- **Zoom Controls**: Zoom in and out on loaded images for detailed inspection.

## Settings & Customization
- **Theme Switching**: Toggle between light and dark themes for the entire application UI.
- **Editor Customization**: Fine-tune the editor experience with settings for:
    - Font family and size
    - Minimap visibility
    - Line numbers
    - Tab size and word wrapping
    - Auto-closing brackets
    - Trailing whitespace trimming on save
- **Terminal Customization**: Configure the terminal shell, font size, and theme.
- **Application Behavior**: Set preferences for auto-save intervals, session restoration, and update checks.

## User Interface (UI/UX)
- **Tabbed Workspace Navigation**: Seamlessly switch between the main editor, notes, dictionary, terminal, and settings tabs (`Alt + 1-6`).
- **Context Menus**: Context-sensitive right-click menus for files, folders, notes, dictionaries, and terminal output.
- **Modal Dialogs**: Clean, modern pop-up dialogs for user input (e.g., renaming files).
- **Notification System**: Non-intrusive notifications for success, warning, and error messages.
- **Status Bar**: Displays the current time, active file name, cursor position, and detected language.

## Keyboard Shortcuts & Commands
- **Global Shortcuts**:
    - `Alt + [1-6]`: Switch between main application tabs.
    - `Ctrl/Cmd + S`: Save the currently active file, note, or dictionary.
- **Custom `idecmd` System**: Execute powerful, predefined commands for notes and dictionaries directly by typing `idecmd.note...` or `idecmd.dict...` into any editor and pressing Enter.

# System notes
## OS-specific notes

### Linux
You guys are in luck since I use linux and this source code should be 100% runable. Use venv/system python and follow the python requirements and you shoud be good to go

### MacOS
For MacOS users, the code should be competly safe as both linux(the system i use) and MacOS have similar filesystem (/ instead of \ ) and therefore should not have any complications

### Windows
I have not tested this on Windows yet but should work perfectly, except the fact that you have to change the following libs:-
| Unix/Linux module | Windows replacement                                   |
| ----------------- | ----------------------------------------------------- |
| `pty`             | `subprocess` / `winpty`                               |
| `fcntl`           | None (skip / remove)                                  |
| `termios`         | None (skip / remove)                                  |
| `select`          | `msvcrt.kbhit()` + `msvcrt.getch()` for console input |
| `pexpect`         | `wexpect`                                             |
| `ptyprocess`      | `wexpect` (optional, if using pty features)           |


## Python-specific notes

Install python 3.10+ and the following libs and you should be good to go

eel             # pip install eel
serial          # pip install pyserial
PIL.Image       # pip install pillow
pexpect         # pip install pexpect
ptyprocess      # pip install ptyprocess
yaml            # pip install pyyaml
