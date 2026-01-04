package main

import (
    "fmt"
    "os/exec"
    "encoding/json"
    "os"
    "strings"
    "strconv"
    "runtime"
    "path/filepath"
    "bufio"
)
var version_major int;
var version_minor int;

func setNestedKey(data map[string]interface{}, key string, value interface{}) {
    parts := strings.Split(key, ".")
    last := parts[len(parts)-1]
    m := data

    for _, k := range parts[:len(parts)-1] {
        // make sure the nested map exists
        if _, ok := m[k]; !ok {
            m[k] = map[string]interface{}{}
        }
        m = m[k].(map[string]interface{})
    }

    // set the final key
    m[last] = value
}
func getNestedValue(data map[string]interface{}, key string) (string, bool) {
    keys := strings.Split(key, ".")
    var current interface{} = data

    for i, k := range keys {
        m, ok := current.(map[string]interface{})
        if !ok {
            return "", false
        }

        current, ok = m[k]
        if !ok {
            return "", false
        }

        // if last key, return as string
        if i == len(keys)-1 {
            val, ok := current.(string)
            return val, ok
        }
    }

    return "", false
}



func jsonmanager(path string, method string, vals ...string) string {
    var data map[string]interface{}

    // Read JSON
    fileBytes, err := os.ReadFile(path)
    if err != nil {
        fmt.Println("Error while trying to access:", path, "error:", err)
        return ""
    }
    err = json.Unmarshal(fileBytes, &data)
    if err != nil {
        fmt.Println("Error while decoding file error:", err)
        return ""
    }

    switch method {
    case "r": // read
        val, ok := getNestedValue(data, vals[0])
        if !ok {
            return ""
        }
        return val

    case "w":
        if len(vals) >= 2 {
            key := vals[0]    // e.g., "character.name"
            value := vals[1]  // e.g., "Alice"
            setNestedKey(data, key, value)
        }

        jsonBytes, err := json.MarshalIndent(data, "", "  ")
        if err != nil {
            fmt.Println("Error marshalling JSON:", err)
            return ""
        }

        err = os.WriteFile(path, jsonBytes, 0644)
        if err != nil {
            fmt.Println("Error writing file:", err)
            return ""
        }


    default:
        fmt.Println("Error: invalid method")
        return "Error: invalid method"
    }

    return ""
}

func upgradePython() {
    pmanager := jsonmanager("data/info.json", "r", "os.packageManager")
    var cmd *exec.Cmd
    switch pmanager{
    case "pacman":
        cmd = exec.Command("sudo", "pacman", "-Syu", "python")
    case "apt":
        cmd = exec.Command("bash", "-c", "sudo apt update && sudo apt install --only-upgrade python3 -y")
    case "dnf":
        cmd = exec.Command("sudo", "dnf", "upgrade", "python3")
    case "zypper":
        cmd = exec.Command("sudo", "zypper", "upgrade", "python3")
    case "brew":
        cmd = exec.Command("brew", "update && brew upgrade python")
    case "winget":
        cmd = exec.Command("powershell", "-Command", "winget install --id Python.Python.3 --silent --upgrade")
    default:
        fmt.Println("ERROR: PACKAGE MANAGER NOT FOUND")
        os.Exit(1)
    }
    output, err := cmd.CombinedOutput()
    if err != nil {
        fmt.Println("ERROR while upgrading python command:", err)
        fmt.Println(string(output))
    } else {
        fmt.Println("SUCCESS: Python upgraded!")
    }
}

func packet_manager_exist(path string) bool {
	_, err := os.Stat(path)
	return err == nil
}

func Browser(osName string) string {
    reader := bufio.NewReader(os.Stdin)

    fmt.Println("\nEnter path to your preferred browser or type 'n' to auto-detect Chrome:")
    input, _ := reader.ReadString('\n')
    input = strings.TrimSpace(input)
    input = strings.ToLower(input)

    // User provided a path
    if input != "n" {
        cmd := exec.Command(input, "--version")
        if err := cmd.Run(); err != nil {
            fmt.Println("ERROR: Invalid path!")
            fmt.Println("Force it anyway? [y/N]")
            force, _ := reader.ReadString('\n')
            if strings.ToLower(strings.TrimSpace(force)) == "y" {
                jsonmanager("data/info.json", "w", "browser.name", "undefined")
                jsonmanager("data/info.json", "w", "browser.exec", input)
                return input
            } else {
                os.Exit(1)
            }
        } else {
            jsonmanager("data/info.json", "w", "browser.name", "undefined")
            jsonmanager("data/info.json", "w", "browser.exec", input)
            return input
        }
    }

    // Auto-detect Chrome
    var path string
    switch osName {
    case "linux":
        candidates := []string{"chrome", "google-chrome", "google-chrome-stable"}
        for _, c := range candidates {
            if exec.Command(c, "--version").Run() == nil {
                path = c
                break
            }
        }
    case "macos":
        macPath := "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if exec.Command(macPath, "--version").Run() == nil {
            path = macPath
        }
    case "windows":
        windowsPaths := []string{
            `C:\Program Files\Google\Chrome\Application\chrome.exe`,
            `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`,
        }
        for _, p := range windowsPaths {
            if exec.Command(p, "--version").Run() == nil {
                path = p
                break
            }
        }
    default:
        fmt.Println("ERROR: Unexpected OS")
        os.Exit(1)
    }

    if path == "" {
        fmt.Println("ERROR: Chrome not found, please provide browser path manually")
        os.Exit(1)
    }

    // Save detected browser info
    jsonmanager("data/info.json", "w", "browser.name", "Chrome")
    jsonmanager("data/info.json", "w", "browser.exec", path)
    return path
}

func venv() {
	osName := jsonmanager("data/info.json", "r", "os.name")

	// 1. Select system python command
	var systemPython string
	switch osName {
	case "linux", "macos":
		systemPython = "python3"
	case "windows":
		systemPython = "python"
	default:
		fmt.Println("ERROR: UNKNOWN OS, create venv manually")
		os.Exit(1)
	}

	// 2. Create venv only if it doesn't exist
	if _, err := os.Stat(".venv"); os.IsNotExist(err) {
		fmt.Println("INFO: Creating Python virtual environment...")

		cmd := exec.Command(systemPython, "-m", "venv", ".venv")
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr

		if err := cmd.Run(); err != nil {
			fmt.Println("ERROR while making virtual environment:", err)
			os.Exit(1)
		}

		fmt.Println("SUCCESS: Python virtual environment created!")
	} else {
		fmt.Println("INFO: .venv already exists, skipping creation")
	}

	// 3. Resolve venv python path
	var venvPython string
	switch osName {
	case "linux", "macos":
		venvPython = filepath.Join(".venv", "bin", "python")
	case "windows":
		venvPython = filepath.Join(".venv", "Scripts", "python.exe")
	}

	// 4. Verify venv python works
	fmt.Println("INFO: Checking venv Python...")
	cmd := exec.Command(venvPython, "--version")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		fmt.Println("ERROR while checking venv Python version:", err)
		os.Exit(1)
	}

	fmt.Println("SUCCESS: venv Python works!")
}



func info_Filler(){
    switch runtime.GOOS {
    case "linux":
        fmt.Println("DETECTED Linux os...\nDetecting distro...")
        switch {

        case packet_manager_exist("/usr/bin/pacman"):
            fmt.Println("Detected Arch (pacman)...")
            jsonmanager("data/info.json", "w", "os.name", "linux")
            jsonmanager("data/info.json", "w", "os.packageManager", "pacman")
            jsonmanager("data/info.json", "w", "os.type", "Arch")

        case packet_manager_exist("/usr/bin/apt"):
            fmt.Println("Detected Ubuntu/Debian (apt)...")
            jsonmanager("data/info.json", "w", "os.name", "linux")
            jsonmanager("data/info.json", "w", "os.packageManager", "apt")
            jsonmanager("data/info.json", "w", "os.type", "Debian")

        case packet_manager_exist("/usr/bin/dnf"):
            fmt.Println("Detected RPM based SPECIFICATION: dnf...")
            jsonmanager("data/info.json", "w", "os.name", "linux")
            jsonmanager("data/info.json", "w", "os.packageManager", "dnf")
            jsonmanager("data/info.json", "w", "os.type", "RedHat")

        case packet_manager_exist("/usr/bin/zypper"):
            fmt.Println("Detected RPM based SPECIFICATION: zypper...")
            jsonmanager("data/info.json", "w", "os.name", "linux")
            jsonmanager("data/info.json", "w", "os.packageManager", "zypper")
            jsonmanager("data/info.json", "w", "os.type", "RedHat")

        case packet_manager_exist("/usr/bin/yum"):
            fmt.Println("Detected RPM based SPECIFICATION: yum...")
            jsonmanager("data/info.json", "w", "os.name", "linux")
            jsonmanager("data/info.json", "w", "os.packageManager", "yum")
            jsonmanager("data/info.json", "w", "os.type", "RedHat")
        default:
            fmt.Println("ERROR: could not detect package manager..")
            jsonmanager("data/info.json", "w", "os.name", "linux")
        }
    case "darwin":
        fmt.Println("DETECTED MacOS...")
        jsonmanager("data/info.json", "w", "os.name", "macos")
        jsonmanager("data/info.json", "w", "os.packageManager", "brew")
        jsonmanager("data/info.json", "w", "os.type", "darwin")
    case "windows":
        fmt.Println("DETECTED Windows...")
        jsonmanager("data/info.json", "w", "os.name", "windows")
        jsonmanager("data/info.json", "w", "os.packageManager", "winget")
        jsonmanager("data/info.json", "w", "os.type", "Win")
    default:
        fmt.Println("ERROR: could not detect os")
        os.Exit(1)
    }
}

func main() {
    fmt.Println("== BUILDING SYSTEM ENVIRONMENT ==")

    fmt.Println(" #1 STORING INFORMATION ABOUT SYSTEM ==")
    info_Filler()
    fmt.Println("== ISTORAGE COMPLETE! ==")

    fmt.Println(" #2 FINDING PYTHON VERSION ==")

    fmt.Println(" CHECKING PYTHON ")

    cmd := exec.Command("python3", "--version")
    output, err := cmd.Output()
    if err != nil {
        fmt.Println("WARNING: python not installed")
        fmt.Println("Installing python...")
        // Installation process
        return
    } else{
        fmt.Println(" FOUND PYTHON ")
    }

    fmt.Println("SUCCESS: python is installed")
    fmt.Println("CHECKING PYTHON VERSION...")

    version_str := strings.TrimSpace(string(output))
    version_parts := strings.Split(version_str, " ") 
    versionNumbers_unclean := strings.Split(version_parts[1], ".")
    version_major, _ = strconv.Atoi(versionNumbers_unclean[0])
    version_minor, _ = strconv.Atoi(versionNumbers_unclean[1])
    version_patch, _ := strconv.Atoi(versionNumbers_unclean[2])
    version_clean := fmt.Sprintf("%d.%d.%d", version_major, version_minor, version_patch)

    fmt.Println("PYTHON VERSION: ", version_clean)

    if version_major < 3 || (version_major >= 3  && version_minor < 10) {
        fmt.Println("WARNING: PYTHON VERSION IS TOO OLD REQUIRED: >3.10")
        fmt.Println("UPGRADING PYTHON:")
        upgradePython()
    } else{
        fmt.Println("Python version meets requirement!")
    }
    venv()

    // 3 INSTALLING PYTHON LIBRARY //
    fmt.Println("Installing python library...")

    cmd = exec.Command(
        ".venv/bin/python",
        "-m", "pip",
        "install",
        "-r", "req.txt",
        "--disable-pip-version-check",
        "--no-input",
    )

    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr


    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr

    err = cmd.Run()
    if err != nil {
        fmt.Println("ERROR: unexpected error :", err)
    } else {
        fmt.Println("SUCCESS: installed with no errors")
    }

    fmt.Println("#4 finding browser information...")
    _ = Browser(jsonmanager("data/info.json", "r", "os.name"))

    fmt.Println("FOUND BROWSER INFORMATION SUCCESSFULLY!")
    fmt.Println("BUILD COMPLETE.. LAUNCHING APP")
    cmd = exec.Command(".venv/bin/python", "app.py")
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    cmd.Run()
}

