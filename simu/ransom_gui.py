import tkinter as tk
from tkinter import messagebox
from hybrid_ransom import main as run_attack

def launch_attack():
    if messagebox.askyesno("Confirmation", "Es-tu sûr(e) de vouloir lancer l'attaque hybride ?"):
        try:
            run_attack()
            messagebox.showinfo("Succès", "L’attaque hybride a été lancée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")

# === Interface Graphique ===
app = tk.Tk()
app.title("Simulateur Ransomware - Projet majeur")
app.geometry("400x200")
app.resizable(False, False)

label = tk.Label(app, text="Bienvenue sur le simulateur éducatif de ransomware.\nCe module va chiffrer des fichiers en format zip, avec  + Fernet + RSA.", justify="center", wraplength=350)
label.pack(pady=20)

launch_button = tk.Button(app, text=" Lancer l’attaque ", command=launch_attack, bg="red", fg="white", font=("Helvetica", 12, "bold"))
launch_button.pack(pady=10)

footer = tk.Label(app, text="Projet Majeure Cyber - Donia", fg="gray")
footer.pack(side="bottom", pady=5)

app.mainloop()
