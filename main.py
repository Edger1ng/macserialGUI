import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import plistlib
import uuid
import os
from pathlib import Path
import urllib.request
import stat
import platform
import zipfile
import io
import json
import requests


APP_NAME = "SMBIOS Generator GUI"
MACSERIAL_BASENAME = "macserial"
MACSERIAL_EXEC = MACSERIAL_BASENAME + (".exe" if platform.system() == "Windows" else "")
GITHUB_API_RELEASES = "https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest"
DORTANIA_MODELS_URL = "https://raw.githubusercontent.com/dortania/OpenCore-Install-Guide/master/data/platforms.json"
DEBUG = True
GENERATE_COUNT = 5

MODEL_DESCRIPTIONS = {
    # iMac
    "iMac4,1": "Early Intel iMac 20-inch Core Duo",
    "iMac5,1": "Early Intel iMac 24-inch Core 2 Duo",
    "iMac5,2": "Mid 2007 iMac 20-inch Core 2 Duo",
    "iMac6,1": "Mid 2007 iMac 24-inch Core 2 Duo",
    "iMac7,1": "Early 2008 iMac 20-inch Core 2 Duo",
    "iMac8,1": "Early 2008 iMac 24-inch Core 2 Duo",
    "iMac9,1": "Early 2009 iMac 20-inch Core 2 Duo / Nehalem i5",
    "iMac10,1": "Mid 2009 iMac 21.5-inch Core i3/i5/i7",
    "iMac11,1": "Mid 2010 iMac 21.5-inch Core i3/i5/i7",
    "iMac11,2": "Mid 2010 iMac 27-inch Core i3/i5/i7",
    "iMac12,1": "Mid 2011 iMac 21.5-inch Sandy Bridge",
    "iMac12,2": "Mid 2011 iMac 27-inch Sandy Bridge",
    "iMac13,1": "Late 2012 iMac 21.5-inch Ivy Bridge",
    "iMac13,2": "Late 2012 iMac 27-inch Ivy Bridge",
    "iMac14,1": "Late 2013 iMac 21.5-inch Haswell",
    "iMac14,2": "Late 2013 iMac 27-inch Haswell",
    "iMac14,3": "Mid 2014 iMac 21.5-inch Haswell",
    "iMac15,1": "Mid 2014 and Mid 2015 iMac 27-inch Haswell Retina",
    "iMac16,1": "Late 2015 iMac 21.5-inch Skylake",
    "iMac16,2": "Late 2015 iMac 27-inch Skylake",
    "iMac17,1": "Late 2015 iMac 27-inch Skylake",
    "iMac18,1": "Mid 2017 iMac 21.5-inch Kaby Lake",
    "iMac18,2": "Mid 2017 iMac 21.5-inch Kaby Lake with discrete GPU",
    "iMac18,3": "Mid 2017 iMac 27-inch Kaby Lake",
    "iMac19,1": "Mid 2019 iMac 27-inch Coffee Lake",
    "iMac19,2": "Mid 2019 iMac 21.5-inch Coffee Lake",
    "iMac20,1": "Mid 2020 iMac 27-inch Comet Lake",
    "iMac20,2": "Mid 2020 iMac 27-inch Comet Lake (high-end)",

    # iMac Pro
    "iMacPro1,1": "2017 iMac Pro Xeon",

    # MacBook
    "MacBook1,1": "Early 2006 MacBook Core Duo",
    "MacBook2,1": "Late 2006 MacBook Core 2 Duo",
    "MacBook3,1": "Late 2007 MacBook Core 2 Duo",
    "MacBook4,1": "Early 2008 MacBook Core 2 Duo",
    "MacBook5,1": "Late 2008 MacBook Core 2 Duo",
    "MacBook5,2": "Late 2008 MacBook Aluminum Unibody",
    "MacBook6,1": "Early 2009 MacBook Core 2 Duo",
    "MacBook7,1": "Mid 2010 MacBook Core 2 Duo",
    "MacBook8,1": "Early 2015 Retina MacBook Broadwell",

    # MacBook Air
    "MacBookAir1,1": "Early 2008 MacBook Air Core 2 Duo",
    "MacBookAir2,1": "Late 2008 MacBook Air Core 2 Duo",
    "MacBookAir3,1": "Late 2010 MacBook Air 11-inch Sandy Bridge",
    "MacBookAir3,2": "Late 2010 MacBook Air 13-inch Sandy Bridge",
    "MacBookAir4,1": "Mid 2011 MacBook Air 11-inch Sandy Bridge",
    "MacBookAir4,2": "Mid 2011 MacBook Air 13-inch Sandy Bridge",
    "MacBookAir5,1": "Mid 2012 MacBook Air 11-inch Ivy Bridge",
    "MacBookAir5,2": "Mid 2012 MacBook Air 13-inch Ivy Bridge",
    "MacBookAir6,1": "Mid 2013 MacBook Air 11-inch Haswell",
    "MacBookAir6,2": "Mid 2013 MacBook Air 13-inch Haswell",
    "MacBookAir7,1": "Early 2015 MacBook Air 11-inch Broadwell",
    "MacBookAir7,2": "Early 2015 MacBook Air 13-inch Broadwell",
    "MacBookAir8,1": "2018 MacBook Air Retina 13-inch Kaby Lake",
    "MacBookAir8,2": "2019 MacBook Air Retina 13-inch True Tone",
    "MacBookAir9,1": "2020 MacBook Air Retina 13-inch Ice Lake",

    # MacBook Pro
    "MacBookPro1,1": "Early 2006 MacBook Pro 15-inch Core Duo",
    "MacBookPro1,2": "Late 2006 MacBook Pro 15-inch Core 2 Duo",
    "MacBookPro2,1": "Mid 2007 MacBook Pro 17-inch Core 2 Duo",
    "MacBookPro3,1": "Early 2008 MacBook Pro 15-inch Core 2 Duo",
    "MacBookPro4,1": "Early 2008 MacBook Pro 15-inch Unibody",
    "MacBookPro5,1": "Late 2008 MacBook Pro 15-inch Unibody Nvidia",
    "MacBookPro5,2": "Early 2009 MacBook Pro 17-inch Unibody",
    "MacBookPro5,3": "Mid 2009 MacBook Pro 15-inch Unibody Nvidia",
    "MacBookPro5,4": "Mid 2009 MacBook Pro 13-inch Unibody",
    "MacBookPro5,5": "Mid 2010 MacBook Pro 13-inch Unibody",
    "MacBookPro6,1": "Mid 2010 MacBook Pro 15-inch Core i5/i7",
    "MacBookPro6,2": "Mid 2010 MacBook Pro 17-inch Unibody",
    "MacBookPro7,1": "Early 2011 MacBook Pro 13-inch Sandy Bridge",
    "MacBookPro8,1": "Late 2011 MacBook Pro 13-inch Sandy Bridge",
    "MacBookPro8,2": "Late 2011 MacBook Pro 15-inch Sandy Bridge",
    "MacBookPro8,3": "Late 2011 MacBook Pro 17-inch Sandy Bridge",
    "MacBookPro9,1": "Mid 2012 MacBook Pro 15-inch Retina Ivy Bridge",
    "MacBookPro9,2": "Mid 2012 MacBook Pro 13-inch Retina Ivy Bridge",
    "MacBookPro10,1": "Early 2013 MacBook Pro 15-inch Retina Haswell",
    "MacBookPro10,2": "Early 2013 MacBook Pro 13-inch Retina Haswell",
    "MacBookPro11,1": "Late 2013 MacBook Pro 13-inch Retina Haswell",
    "MacBookPro11,2": "Late 2013 MacBook Pro 15-inch Retina Haswell",
    "MacBookPro11,3": "Mid 2014 MacBook Pro 15-inch Retina Haswell",
    "MacBookPro11,4": "Mid 2015 MacBook Pro 15-inch Retina Broadwell",
    "MacBookPro11,5": "Mid 2015 MacBook Pro 15-inch Retina Broadwell",
    "MacBookPro12,1": "Early 2015 MacBook Pro 13-inch Retina Broadwell",
    "MacBookPro13,1": "Late 2016 MacBook Pro 13-inch Kaby Lake no Touch Bar",
    "MacBookPro13,2": "Late 2016 MacBook Pro 13-inch Kaby Lake with Touch Bar",
    "MacBookPro13,3": "Late 2016 MacBook Pro 15-inch Skylake with Touch Bar",
    "MacBookPro14,1": "2017 MacBook Pro 13-inch Kaby Lake no Touch Bar",
    "MacBookPro14,2": "2017 MacBook Pro 13-inch Kaby Lake with Touch Bar",
    "MacBookPro14,3": "2017 MacBook Pro 15-inch Kaby Lake with Touch Bar",
    "MacBookPro15,1": "2018 MacBook Pro 15-inch Coffee Lake with Touch Bar",
    "MacBookPro15,2": "2018 MacBook Pro 13-inch Coffee Lake with Touch Bar",
    "MacBookPro15,3": "2019 MacBook Pro 15-inch Coffee Lake with Touch Bar",
    "MacBookPro15,4": "2019 MacBook Pro 13-inch Coffee Lake with Touch Bar",
    "MacBookPro16,1": "2019 MacBook Pro 16-inch Coffee Lake with Touch Bar",
    "MacBookPro16,2": "2019 MacBook Pro 13-inch Coffee Lake with Touch Bar",
    "MacBookPro16,3": "2019 MacBook Pro 16-inch lower-end configuration",

    # Mac mini
    "Macmini1,1": "Early 2006 Mac mini Core Duo",
    "Macmini2,1": "Late 2006 Mac mini Core 2 Duo",
    "Macmini3,1": "Early 2009 Mac mini Core 2 Duo",
    "Macmini4,1": "Mid 2010 Mac mini Core i5/i7",
    "Macmini5,1": "Mid 2011 Mac mini Sandy Bridge",
    "Macmini5,2": "Mid 2011 Mac mini Server Sandy Bridge",
    "Macmini5,3": "Mid 2011 Mac mini Discrete GPU",
    "Macmini6,1": "Late 2012 Mac mini Ivy Bridge",
    "Macmini6,2": "Late 2012 Mac mini Server Ivy Bridge",
    "Macmini7,1": "Late 2014 Mac mini Haswell",
    "Macmini8,1": "2018 Mac mini Coffee Lake",

    # Mac Pro
    "MacPro1,1": "Early 2006 Mac Pro Xeon 32-bit",
    "MacPro2,1": "2007 Mac Pro Xeon 64-bit",
    "MacPro3,1": "Early 2008 Mac Pro Nehalem Xeon",
    "MacPro4,1": "Early 2009 Mac Pro Nehalem Xeon updated",
    "MacPro5,1": "Mid 2010 and Mid 2012 Mac Pro Westmere Xeon",
    "MacPro6,1": "Late 2013 Mac Pro 'trashcan' Xeon E5",
    "MacPro7,1": "2019 Mac Pro Xeon-W high-end workstation",

    # Xserve
    "Xserve1,1": "Early 2006 Xserve Xeon Core Duo",
    "Xserve2,1": "2007 Xserve Xeon Core 2 Duo",
    "Xserve3,1": "Early 2009 Xserve Nehalem Xeon",
    "Xserve4,1": "Early 2010 Xserve Westmere Xeon",
    "Xserve5,1": "Mid 2012 Xserve Ivy Bridge Xeon",
}

def _print_debug(msg):
    if DEBUG:
        print(msg)

def download_macserial_from_ocpkg():
    try:
        req = urllib.request.Request(GITHUB_API_RELEASES, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-J530FM Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Mobile Safari/537.36 YaApp_Android/10.91 YaSearchBrowser/10.91"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            release_info = json.loads(resp.read().decode())

        assets = release_info.get("assets", [])
        zip_asset = next((a for a in assets if a["name"].endswith(".zip")), None)
        if not zip_asset:
            _print_debug("No .zip asset found in OpenCorePkg release")
            return None

        url = zip_asset["browser_download_url"]
        _print_debug(f"Downloading OpenCorePkg zip from {url}...")
        req_zip = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-J530FM Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Mobile Safari/537.36 YaApp_Android/10.91 YaSearchBrowser/10.91"})
        with urllib.request.urlopen(req_zip, timeout=60) as zipresp:
            with zipfile.ZipFile(io.BytesIO(zipresp.read())) as archive:
                candidate = None
                names = archive.namelist()
                prefer = []
                if platform.system() == "Windows":
                    prefer = [n for n in names if n.endswith("/macserial.exe") or n.endswith("macserial.exe")]
                elif platform.system() == "Darwin":
                    prefer = [n for n in names if n.endswith("/macserial") and "macserial." not in n] or \
                             [n for n in names if n.endswith("Utilities/macserial/macserial")]
                else:
                    prefer = [n for n in names if n.endswith("macserial.Linux")]
                if prefer:
                    candidate = prefer[0]
                else:
                    for n in names:
                        base = n.split("/")[-1]
                        if base.startswith("macserial"):
                            candidate = n
                            break

                if not candidate:
                    _print_debug("macserial binary not found in archive")
                    return None

                outname = MACSERIAL_EXEC
                _print_debug(f"Extracting {candidate} -> {outname}")
                with open(outname, "wb") as f:
                    f.write(archive.read(candidate))
                os.chmod(outname, os.stat(outname).st_mode | stat.S_IEXEC)
                return outname
    except Exception as e:
        _print_debug(f"Failed to download/extract macserial: {e}")
        return None

def get_models_from_dortania():
    try:
        r = requests.get(DORTANIA_MODELS_URL, timeout=20, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-J530FM Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Mobile Safari/537.36 YaApp_Android/10.91 YaSearchBrowser/10.91"})
        r.raise_for_status()
        data = r.json()
        models = list(data.keys())
        _print_debug(f"Loaded {len(models)} models from Dortania")
        return sorted(models)
    except Exception as e:
        _print_debug(f"Failed to fetch models from Dortania: {e}")
        return sorted(MODEL_DESCRIPTIONS.keys())

def check_serial_occupied(serial):
    prefix = serial[:3]
    url = f"https://support-sp.apple.com/sp/product?cc={prefix}"
    try:
        r = requests.get(url, timeout=5, headers={"User-Agent": "SMBIOSGen/1.0"})
        if r.status_code == 200:
            text = r.text.lower()
            return "no info" not in text
        return None
    except Exception:
        return None

def run_macserial_multiple(model, count=5):
    exec_path = Path("./" + MACSERIAL_EXEC)
    if not exec_path.exists():
        raise RuntimeError(f"{MACSERIAL_EXEC} is missing. Download step failed.")

    results = []
    for _ in range(count):
        try:
            result = subprocess.run([str(exec_path), "-m", model], capture_output=True, text=True)
            output = result.stdout.strip().splitlines()
            if result.returncode != 0 or not output:
                raise RuntimeError(result.stderr.strip() or "macserial returned no output")

            _print_debug("macserial output:\n" + "\n".join(output))

            serial = None
            board = None
            for line in output:
                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 2:
                        serial, board = parts[0], parts[1]
                        break

            if not serial or not board:
                raise RuntimeError("No valid SMBIOS data found in macserial output.")

            smuuid = str(uuid.uuid4()).upper()
            rom = uuid.uuid4().hex[:12].upper()

            occupied = check_serial_occupied(serial)
            if occupied is None:
                occupied_str = "Unknown (check failed)"
            elif occupied:
                occupied_str = "Probably OCCUPIED"
            else:
                occupied_str = "Probably FREE"

            results.append({
                "Model": model,
                "SerialNumber": serial,
                "BoardSerialNumber": board,
                "SmUUID": smuuid,
                "ROM": rom,
                "Occupied": occupied_str
            })
        except Exception as e:
            raise RuntimeError(f"macserial execution failed: {e}")
    return results

def insert_into_config(config_path, smbios_data):
    try:
        with open(config_path, "rb") as f:
            plist = plistlib.load(f)

        plist.setdefault("PlatformInfo", {})
        plist["PlatformInfo"].setdefault("Generic", {})
        g = plist["PlatformInfo"]["Generic"]
        g["SystemProductName"] = smbios_data["Model"]
        g["SystemSerialNumber"] = smbios_data["SerialNumber"]
        g["MLB"] = smbios_data["BoardSerialNumber"]
        g["SystemUUID"] = smbios_data["SmUUID"]
        g["ROM"] = bytes.fromhex(smbios_data["ROM"])

        with open(config_path, "wb") as f:
            plistlib.dump(plist, f)
        return True, None
    except Exception as e:
        return False, str(e)

class SMBIOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)

        self.model_var = tk.StringVar()
        self.variants = [] 
        self.count_var = tk.StringVar(value=str(GENERATE_COUNT))
        self.description_var = tk.StringVar()

        self._build_gui()
        self._populate_models()

    def _build_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Mac Model:").grid(row=0, column=0, sticky="w")
        self.model_combo = ttk.Combobox(frame, textvariable=self.model_var, state="readonly", width=25)
        self.model_combo.grid(row=0, column=1, sticky="w")
        self.model_combo.bind("<<ComboboxSelected>>", self._update_description)

        tk.Label(frame, textvariable=self.description_var, fg="gray", width=50, anchor="w", justify="left").grid(row=0, column=2, padx=10, sticky="w")

        tk.Label(frame, text="Variants count:").grid(row=1, column=0, sticky="w")
        self.count_entry = tk.Entry(frame, textvariable=self.count_var, width=5)
        self.count_entry.grid(row=1, column=1, sticky="w")

        tk.Button(frame, text="Generate SMBIOS Variants", command=self.generate).grid(row=2, column=0, columnspan=3, pady=5)

        self.variants_listbox = tk.Listbox(frame, height=10, width=90)
        self.variants_listbox.grid(row=3, column=0, columnspan=3, pady=5)
        self.variants_listbox.bind("<<ListboxSelect>>", self._on_variant_select)

        self.output_text = tk.Text(self.root, height=10, width=90)
        self.output_text.pack(padx=10, pady=10)

        self.insert_button = tk.Button(self.root, text="Insert into config.plist", command=self.insert, state="disabled")
        self.insert_button.pack(pady=(0, 10))

    def generate(self):
        try:
            count = int(self.count_var.get())
            if count < 1:
                messagebox.showwarning(APP_NAME, "Please enter a positive number.")
                return
        except ValueError:
            messagebox.showwarning(APP_NAME, "Please enter a valid number.")
            return

        model = self.model_var.get()
        if not model:
            messagebox.showwarning(APP_NAME, "Please select a Mac model.")
            return

        try:
            self.variants = run_macserial_multiple(model, count)
        except Exception as e:
            messagebox.showerror(APP_NAME, f"Generation failed:\n{e}")
            return

        self.variants_listbox.delete(0, tk.END)
        for i, v in enumerate(self.variants, 1):
            display_str = f"{i}: SN={v['SerialNumber']} MLB={v['BoardSerialNumber']} Status={v.get('Occupied', 'Unknown')}"
            self.variants_listbox.insert(tk.END, display_str)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Select a variant to see details.\n")

    def _populate_models(self):
        models = get_models_from_dortania()
        self.model_combo["values"] = models
        if models:
            self.model_var.set(models[0])
            self._update_description()

    def _update_description(self, *args):
        model = self.model_var.get()
        desc = MODEL_DESCRIPTIONS.get(model, "No description available.")
        self.description_var.set(desc)

    def _on_variant_select(self, event):
        if not self.variants:
            return
        sel = self.variants_listbox.curselection()
        if not sel:
            return
        index = sel[0]
        variant = self.variants[index]

        self.output_text.delete(1.0, tk.END)
        for k, v in variant.items():
            self.output_text.insert(tk.END, f"{k}: {v}\n")
        self.insert_button.config(state="normal")

    def insert(self):
        sel = self.variants_listbox.curselection()
        if not sel:
            messagebox.showwarning(APP_NAME, "Please select a variant to insert.")
            return
        idx = sel[0]
        variant = self.variants[idx]
        path = filedialog.askopenfilename(title="Select config.plist", filetypes=[("Plist files", "*.plist")])
        if not path:
            return
        ok, err = insert_into_config(path, variant)
        if ok:
            messagebox.showinfo(APP_NAME, "config.plist updated successfully!")
        else:
            messagebox.showerror(APP_NAME, f"Failed to update config.plist:\n{err}")


if __name__ == "__main__":
    exec_path = Path("./" + MACSERIAL_EXEC)
    if not exec_path.exists():
        fetched = download_macserial_from_ocpkg()
        if not fetched or not Path("./" + MACSERIAL_EXEC).exists():
            print("Failed to download macserial. Check your internet and try again.")
            exit(1)


    root = tk.Tk()
    app = SMBIOSApp(root)
    root.mainloop()
