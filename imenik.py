# imenik_simple.py
import tkinter as tk
from tkinter import messagebox
import csv

CSV_PATH = "kontakti.csv"

# ------------------ MODEL PODATAKA ------------------
class Kontakt:
    def __init__(self, ime, email, telefon):
        self.ime = ime
        self.email = email
        self.telefon = telefon

    def __str__(self):
        return f"{self.ime}, {self.email}, {self.telefon}"

# ------------------ GUI + FUNKCIONALNOST ------------------
class ImenikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jednostavni imenik")
        self.root.geometry("520x420")

        self.kontakti = []

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        unos_frame = tk.Frame(self.root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")

        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")
        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)

        gumbi_frame = tk.Frame(self.root, padx=10, pady=10)
        gumbi_frame.grid(row=2, column=0, sticky="EW")

        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.email_entry = tk.Entry(unos_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Telefon:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.tel_entry = tk.Entry(unos_frame)
        self.tel_entry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")

        unos_frame.columnconfigure(1, weight=1)

        tk.Button(gumbi_frame, text="Dodaj kontakt", command=self.dodaj_kontakt).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(gumbi_frame, text="Spremi kontakte", command=self.spremi_kontakte).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(gumbi_frame, text="Učitaj kontakte", command=self.ucitaj_kontakte).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(gumbi_frame, text="Obriši kontakt", command=self.obrisi_odabrani).grid(row=0, column=3, padx=5, pady=5)

        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")
        scrollbar = tk.Scrollbar(prikaz_frame, command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.ucitaj_kontakte(prvi_put=True)

    def dodaj_kontakt(self):
        ime = self.ime_entry.get().strip()
        email = self.email_entry.get().strip()
        telefon = self.tel_entry.get().strip()

        if not (ime and email and telefon):
            messagebox.showwarning("Upozorenje", "Popuni sva tri polja (ime, email, telefon).")
            return
        if len(ime) < 3:
            messagebox.showwarning("Upozorenje", "Ime mora imati 3 ili više znakova")
            return

        if len(telefon) != 9 and len(telefon) != 10:
            messagebox.showwarning("Upozorenje", "Telefonski broj mora imati 9 ili 10 znakova")
            return

        if '@' not in email or not email.endswith('.com'):
            messagebox.showwarning("Upozorenje", "Email mora sadržavati znak @ i završavati se sa .com")
            return


        k = Kontakt(ime, email, telefon)
        self.kontakti.append(k)
        self.osvjezi_prikaz()
        self.ocisti_polja()

    def osvjezi_prikaz(self):
        self.listbox.delete(0, tk.END)
        for k in self.kontakti:
            self.listbox.insert(tk.END, str(k))

    def spremi_kontakte(self):
        try:
            with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["ime", "email", "telefon"])
                for k in self.kontakti:
                    w.writerow([k.ime, k.email, k.telefon])
            messagebox.showinfo("Spremanje", "Kontakti su spremljeni.")
        except Exception as e:
            messagebox.showerror("Greška", f"Nije moguće spremiti datoteku.\n{e}")

    def ucitaj_kontakte(self, prvi_put=False):
        try:
            with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
                r = csv.reader(f)
                rows = list(r)
            self.kontakti.clear()
            start = 1 if rows and rows[0][:3] == ["ime", "email", "telefon"] else 0
            for row in rows[start:]:
                if len(row) >= 3:
                    self.kontakti.append(Kontakt(row[0], row[1], row[2]))
            self.osvjezi_prikaz()
            if not prvi_put:
                messagebox.showinfo("Učitavanje", "Kontakti su učitani.")
        except FileNotFoundError:
            if not prvi_put:
                messagebox.showinfo("Info", "Datoteka ne postoji.")
        except Exception as e:
            messagebox.showerror("Greška", f"Nije moguće učitati datoteku.\n{e}")

    def obrisi_odabrani(self):
        odabrani = self.listbox.curselection()
        if not odabrani:
            messagebox.showinfo("Info", "Najprije odaberi kontakt iz liste.")
            return
        idx = odabrani[0]
        del self.kontakti[idx]
        self.osvjezi_prikaz()

    def ocisti_polja(self):
        self.ime_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.tel_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImenikApp(root)
    root.mainloop()
