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
MACSERIAL_EXEC = "macserial"
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

def download_macserial_from_ocpkg():
    try:
        response = urllib.request.urlopen(GITHUB_API_RELEASES)
        release_info = json.loads(response.read().decode())
        assets = release_info.get("assets", [])

        zip_asset = next((a for a in assets if a["name"].endswith(".zip")), None)
        if not zip_asset:
            raise RuntimeError("No .zip asset found in OpenCorePkg release")

        url = zip_asset["browser_download_url"]
        print(f"Downloading OpenCorePkg zip from {url}...")
        with urllib.request.urlopen(url) as zipresp:
            with zipfile.ZipFile(io.BytesIO(zipresp.read())) as archive:
                for name in archive.namelist():
                    if platform.system() == "Windows" and name.endswith("macserial.exe"):
                        outname = "macserial.exe"
                    elif platform.system() == "Darwin" and name.endswith("macserial") and "macserial." not in name:
                        outname = "macserial"
                    elif platform.system() != "Windows" and platform.system() != "Darwin" and name.endswith("macserial.Linux"):
                        outname = "macserial.Linux"
                    else:
                        continue

                    print(f"Extracting {name} -> {outname}")
                    with open(outname, "wb") as f:
                        f.write(archive.read(name))
                    os.chmod(outname, os.stat(outname).st_mode | stat.S_IEXEC)
                    return outname
        raise RuntimeError("macserial binary not found in archive")
    except Exception as e:
        messagebox.showerror(APP_NAME, f"Failed to download macserial from OpenCorePkg:\n{e}")
        return None

def get_models_from_dortania():
    try:
        response = requests.get(DORTANIA_MODELS_URL)
        response.raise_for_status()
        data = response.json()
        models = list(data.keys())
        if DEBUG:
            print(f"Loaded {len(models)} models from Dortania")
        return sorted(models)
    except Exception as e:
        if DEBUG:
            print(f"Failed to fetch models from Dortania: {e}")
        return list(MODEL_DESCRIPTIONS.keys())

def check_serial_occupied(serial):
    """Попытка проверить, не занят ли серийник (через запрос на Apple Support)."""
    prefix = serial[:3]
    url = f"https://support-sp.apple.com/sp/product?cc={prefix}"
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200 and "no info" not in r.text.lower():
            return False 
        else:
            return True 
    except Exception:
        return None 

def run_macserial_multiple(model, count=5):
    exec_name = MACSERIAL_EXEC + (".exe" if platform.system() == "Windows" else "")
    results = []
    for _ in range(count):
        try:
            result = subprocess.run([f"./{exec_name}", "-m", model], capture_output=True, text=True)
            output = result.stdout.strip().splitlines()

            if DEBUG:
                print("macserial output:")
                print("\n".join(output))

            serial = None
            board = None
            for line in output:
                if "|" in line:
                    parts = line.strip().split("|")
                    if len(parts) >= 2:
                        serial = parts[0].strip()
                        board = parts[1].strip()
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
            messagebox.showerror("Error", f"macserial execution failed:\n{e}")
            break
    return results

def insert_into_config(config_path, smbios_data):
    try:
        with open(config_path, "rb") as f:
            plist = plistlib.load(f)

        if "PlatformInfo" not in plist:
            plist["PlatformInfo"] = {}
        if "Generic" not in plist["PlatformInfo"]:
            plist["PlatformInfo"]["Generic"] = {}

        generic = plist["PlatformInfo"]["Generic"]
        generic["SystemProductName"] = smbios_data["Model"]
        generic["SystemSerialNumber"] = smbios_data["SerialNumber"]
        generic["MLB"] = smbios_data["BoardSerialNumber"]
        generic["SystemUUID"] = smbios_data["SmUUID"]
        generic["ROM"] = bytes.fromhex(smbios_data["ROM"])

        with open(config_path, "wb") as f:
            plistlib.dump(plist, f)

        messagebox.showinfo(APP_NAME, "config.plist updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update config.plist:\n{e}")

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

        # Модель
        tk.Label(frame, text="Mac Model:").grid(row=0, column=0, sticky="w")
        self.model_combo = ttk.Combobox(frame, textvariable=self.model_var, state="readonly", width=25)
        self.model_combo.grid(row=0, column=1, sticky="w")
        self.model_combo.bind("<<ComboboxSelected>>", self._update_description)

        # Описание модели справа
        tk.Label(frame, textvariable=self.description_var, fg="gray", width=40, anchor="w", justify="left").grid(row=0, column=2, padx=10, sticky="w")

        # Кол-во вариантов
        tk.Label(frame, text="Variants count:").grid(row=1, column=0, sticky="w")
        self.count_entry = tk.Entry(frame, textvariable=self.count_var, width=5)
        self.count_entry.grid(row=1, column=1, sticky="w")

        # Кнопка генерации
        tk.Button(frame, text="Generate SMBIOS Variants", command=self.generate).grid(row=2, column=0, columnspan=3, pady=5)

        # Список вариантов
        self.variants_listbox = tk.Listbox(frame, height=10, width=80)
        self.variants_listbox.grid(row=3, column=0, columnspan=3, pady=5)
        self.variants_listbox.bind("<<ListboxSelect>>", self._on_variant_select)

        # Окно вывода деталей
        self.output_text = tk.Text(self.root, height=10, width=80)
        self.output_text.pack(padx=10, pady=10)
        
        # Кнопка вставки в config.plist (изначально выключена)
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

        self.variants = run_macserial_multiple(model, count)

        self.variants_listbox.delete(0, tk.END)
        for i, v in enumerate(self.variants, 1):
            display_str = f"{i}: SN={v['SerialNumber']} MLB={v['BoardSerialNumber']} Status={v.get('Occupied', 'Unknown')}"
            self.variants_listbox.insert(tk.END, display_str)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Select a variant to see details.\n")

    def _populate_models(self):
        models = sorted(MODEL_DESCRIPTIONS.keys())
        self.model_combo["values"] = models
        if models:
            self.model_var.set(models[0])
            self._update_description()

    def _update_description(self, *args):
        model = self.model_var.get()
        desc = MODEL_DESCRIPTIONS.get(model, "No description available.")
        self.description_var.set(desc)

    def _on_model_change(self, event):
        self.clear_output_and_variants()






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
            self.insert_button.config(state="normal")  # Активируем кнопку после выбора


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
        insert_into_config(path, variant)

    def clear_output_and_variants(self):
        self.variants = []
        self.variants_listbox.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.insert_button.config(state="disabled")



if __name__ == "__main__":
    exec_path = MACSERIAL_EXEC + (".exe" if platform.system() == "Windows" else "")
    if not Path(exec_path).exists():
        if not download_macserial_from_ocpkg():
            exit(1)

    root = tk.Tk()
    app = SMBIOSApp(root)
    root.mainloop()
