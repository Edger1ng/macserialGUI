# SMBIOS Generator GUI

**SMBIOS Generator GUI** is a Python + Tkinter-based graphical utility for generating valid Apple SMBIOS information using [macserial](https://github.com/acidanthera/OpenCorePkg). This tool is useful for Hackintosh users and developers who need realistic, unique Apple serial numbers for OpenCore.

## 🚀 Features

* GUI-based interface using Tkinter
* Auto-download and extraction of `macserial` from official OpenCorePkg releases
* Support for a wide range of Apple models (iMac, MacBook, Mac mini, Mac Pro, Xserve, etc.)
* Batch generation of SMBIOS variants
* Apple Support serial number occupation check (via web query)
* One-click injection of SMBIOS data into `config.plist`




## 📦 Installation

1. Make sure Python 3.7+ is installed.
2. Install required packages:

   ```bash
   pip install requests
   ```
3. Clone this repository or download the script:

   ```bash
   git clone https://github.com/your-username/macserial-gui.git
   cd macserial-gui
   ```
4. Run the application:

   ```bash
   python main.py
   ```

   The script will automatically download `macserial` on first run.

## 📦 Where to Download Pre-built Binaries

You don’t need to build the app yourself if you don’t want to. Ready-made executables are available for all major platforms (Windows, macOS, Linux) as **artifacts** on GitHub Actions.

### How to download pre-built binaries

1. Go to the [Actions tab](https://github.com/Edger1ng/macserialGUI/actions) in this repository.
2. Find the latest successful workflow run called **Build SMBIOS Generator GUI**.
3. Open the run and scroll down to the **Artifacts** section.
4. Download the artifact matching your platform:
   - `SMBIOS-GUI-Windows.zip` (contains `main.exe`)
   - `SMBIOS-GUI-macOS.zip` (contains `main` executable)
   - `SMBIOS-GUI-Linux.zip` (contains `main` executable)
5. Unzip and run the executable directly. No additional setup required except Python dependencies are bundled.

## ⚙️ Usage

1. Choose your desired **Mac model** from the dropdown.
2. Enter how many **SMBIOS variants** to generate.
3. Click **Generate SMBIOS Variants**.
4. Select one of the generated variants from the list.
5. Click the **Insert into config.plist** button to update your OpenCore `config.plist`.

### Sample Output

```
Model: iMac14,2
SerialNumber: C02LXYZ12345
BoardSerialNumber: C02123456789ABCDE
SmUUID: 5D9DAF0F-2E21-4A36-B999-3D6D01B2A107
ROM: 112233445566
Occupied: Probably FREE
```

## 🧐 How It Works

* The GUI uses the `macserial` utility downloaded from the latest [OpenCorePkg GitHub release](https://github.com/acidanthera/OpenCorePkg).
* A selected Mac model (e.g., iMac14,2) is passed to `macserial` with the `-m` flag.
* `macserial` generates matching serial numbers and board serials.
* A unique SmUUID and ROM are generated using `uuid`.
* A lightweight serial occupation check is performed using Apple Support’s lookup service.
* If selected, this data can be inserted into `config.plist` using Python’s `plistlib`.

## 📁 Project Structure

```
macserial-gui/
├── main.py           # Main GUI application
├── README.md         # This file
└── macserial(.exe)   # Automatically downloaded on first run
```

## 🧪 Compatibility

* ✅ Windows 10/11
* ✅ macOS (with Python and permissions)
* ✅ Linux (with Python and Tkinter)

## 📌 Dependencies

* Python 3.7+
* `requests` module
* Tkinter (built-in)

## ⚠️ Notes

* Serial number occupation check uses a public Apple endpoint and is best-effort.
* Do not use generated SMBIOS data for illegal purposes. You are responsible for your usage.

## 📄 License

This project is under the [MIT License](LICENSE).

## 🙏 Credits

* [Acidanthera](https://github.com/acidanthera) for `macserial` and OpenCorePkg

