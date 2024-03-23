import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
import pyarabic.araby as araby

line_sep = "☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪☪"

def load_surah_names(file_name):
    surah_names = {}
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('. ', 1)
                if len(parts) == 2:
                    surah_number, surah_name = parts
                    surah_names[int(surah_number)] = surah_name
                else:
                    print(f"Ignoré: {line} (Format incorrect)")
    return surah_names

def find_word_in_file(file_name, search_word, surah_names):
    normalized_search_word = araby.strip_diacritics(search_word)
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        results = []
        count = 0
        for i, line in enumerate(lines):
            normalized_line = araby.strip_diacritics(line)
            if normalized_search_word in normalized_line:
                surah_number, ayah_number, ayah_text = line.split('|', 2)
                surah_number = int(surah_number)
                surah_name = surah_names.get(surah_number, f'Surah {surah_number}')
                result = {'word': search_word, 'surah_name': surah_name, 'ayah_number': int(ayah_number), 'ayah_text': ayah_text.strip()}
                count += 1

                # Ajouter le verset précédent s'il existe
                if i > 0:
                    prev_line = lines[i - 1]
                    prev_surah_number, prev_ayah_number, prev_ayah_text = prev_line.split('|', 2)
                    prev_surah_number = int(prev_surah_number)
                    prev_surah_name = surah_names.get(prev_surah_number, f'Surah {prev_surah_number}')
                    result['prev_ayah'] = {'surah_name': prev_surah_name, 'ayah_number': int(prev_ayah_number), 'ayah_text': prev_ayah_text.strip()}

                # Ajouter le verset suivant s'il existe
                if i < len(lines) - 1:
                    next_line = lines[i + 1]
                    next_surah_number, next_ayah_number, next_ayah_text = next_line.split('|', 2)
                    next_surah_number = int(next_surah_number)
                    next_surah_name = surah_names.get(next_surah_number, f'Surah {next_surah_number}')
                    result['next_ayah'] = {'surah_name': next_surah_name, 'ayah_number': int(next_ayah_number), 'ayah_text': next_ayah_text.strip()}

                results.append(result)
    return count, results

def generate_html_with_results(search_word, count, results):
    html_content = f"<html><head><title>Résultats de la recherche</title>"
    html_content += "<style>body { font-size: 24px; }</style></head><body>"
    html_content += f"<p><strong>تم العثور على الكلمة '{search_word}' {count} مرة في القرآن الكريم.</strong><br></p><br><br>"

    for result in results:
        html_content += f"<center><span style='color: blue; font-weight: bold;'>{result['surah_name']}</span></center>"

        normalized_word = araby.strip_diacritics(search_word)
        ayah_number = result['ayah_number']
        ayah_text = result['ayah_text']
        ayah_text_red = ayah_text.replace(
            normalized_word, f"<span style='color: red;'>{search_word}</span>")

        # Ajouter le numéro de verset à chaque verset
        #ayah_text_with_number = f"{result['surah_name']} ({ayah_number}): <span style='color: red;'>{ayah_text}</span>"
        ayah_text_with_number = f"({ayah_number}): <span style='color: red;'>{ayah_text}</span>"




        # Ajouter le verset précédent s'il existe
        if 'prev_ayah' in result:
            prev_ayah = result['prev_ayah']
            prev_ayah_number = prev_ayah['ayah_number']
            prev_ayah_text = prev_ayah['ayah_text']
            prev_ayah_text_with_number = f"({prev_ayah_number}): {prev_ayah_text}"
            html_content += f"<p>{prev_ayah_text_with_number}</p>"

        # Ajouter le verset actuel
        html_content += f"<p>{ayah_text_with_number}</p>"

        # Ajouter le verset suivant s'il existe et si la sourate est la même
        if 'next_ayah' in result and result['surah_name'] == result['next_ayah']['surah_name']:
            next_ayah = result['next_ayah']
            next_ayah_number = next_ayah['ayah_number']
            next_ayah_text = next_ayah['ayah_text']
            next_ayah_text_with_number = f" ({next_ayah_number}): {next_ayah_text}"
            html_content += f"<p>{next_ayah_text_with_number}</p>"
            html_content += f"<p><br>{line_sep}</p><br>"

    html_content += "</body></html>"

    with open('search_results.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    import webbrowser
    webbrowser.open('search_results.html', new=2)




class QuranSearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Quran Search App")
        self.button_font = ("Arial", 18)  
        
        
        self.label = tk.Label(master, text="Entrez le mot à rechercher :")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.search_button = tk.Button(master, text="Rechercher", command=self.search)

        # Appeler create_keyboard après la création du bouton de recherche
        self.create_keyboard()

    def create_keyboard(self):
        arabic_letters = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"

        # Créer un frame pour contenir les boutons du clavier
        keyboard_frame = tk.Frame(self.master)
        keyboard_frame.pack()

        # Ajouter le bouton de recherche
        self.search_button.pack()

        
        # Ajouter les boutons du clavier avec la police spécifiée
        for i, letter in enumerate(arabic_letters):
            button = tk.Button(keyboard_frame, text=letter, command=lambda l=letter: self.insert_letter(l), font=self.button_font)
            row_num, col_num = divmod(i, 7)  # Changer 7 selon le nombre de boutons par ligne souhaité
            button.grid(row=row_num, column=col_num, padx=5, pady=5)

    def insert_letter(self, letter):
        # Insérer la lettre dans l'entrée et stocker la lettre insérée
        self.entry.insert(tk.END, letter)
        self.inserted_letter = letter
        
  
    def search(self):
        search_word = self.entry.get()
        count, results = find_word_in_file("quran-simple-plain.txt", search_word, load_surah_names("surah_names.txt"))
        generate_html_with_results(search_word, count, results)
        messagebox.showinfo("Recherche terminée", f"Le mot '{search_word}' a été trouvé {count} fois. Les résultats sont affichés dans le navigateur.")

def main():
    root = tk.Tk()
    root.geometry("500x400") 
    app = QuranSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
