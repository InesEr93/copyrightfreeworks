import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Funktion, um die CSV-Dateien zu laden
def load_data(bibl_file, author_file):
    bibliographic_data = []
    author_data = {}

    # Lade die bibliografischen Daten
    with open(bibl_file, mode='r', encoding='utf-8') as bibl_csv:
        reader = csv.DictReader(bibl_csv)
        for row in reader:
            bibliographic_data.append(row)

    # Lade die Autorendaten
    with open(author_file, mode='r', encoding='utf-8') as author_csv:
        reader = csv.DictReader(author_csv)
        for row in reader:
            author_data[row['Name']] = {
                'birthdate': row['Geburtsdatum'],
                'deathdate': row['Todesdatum']
            }

    return bibliographic_data, author_data

# Funktion zur Berechnung der Urheberrechtsfreiheit
def check_public_domain(bibl_data, author_data):
    current_year = datetime.now().year
    public_domain_works = []
    protected_works = []

    for work in bibl_data:
        author = work['Autor']
        if author in author_data and author_data[author]['deathdate']:
            death_year = int(author_data[author]['deathdate'].split('-')[2])
            if current_year - death_year > 70:
                public_domain_works.append(work)
            else:
                protected_works.append(work)
        else:
            protected_works.append(work)

    return public_domain_works, protected_works

# Funktion zur Darstellung eines Kreisdiagramms
def plot_results(public_count, protected_count):
    labels = ['Urheberrechtsfrei', 'Geschützt']
    sizes = [public_count, protected_count]
    colors = ['#bfdde0', '#ffc1bc']  # Grün für frei, Orange für geschützt
    explode = (0.1, 0)  # Hervorhebung des ersten Segments

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Urheberrechtsstatus der Titel')
    plt.show()

# Hauptprogramm
def main():
    # Dateinamen im gleichen Ordner wie das Skript
    bibl_file = "BiblData.txt"
    author_file = "Authorbirthdates.txt"

    # Lade Daten
    bibl_data, author_data = load_data(bibl_file, author_file)

    # Überprüfe, welche Werke urheberrechtsfrei sind
    public_domain_works, protected_works = check_public_domain(bibl_data, author_data)

    # Ausgabe der Ergebnisse
    print(f"Urheberrechtsfreie Werke: {len(public_domain_works)}")
    print(f"Geschützte Werke: {len(protected_works)}")

    if public_domain_works:
        print("\nUrheberrechtsfreie Werke:")
        for work in public_domain_works:
            print(f"'{work['Titel']}' von {work['Autor']} ({work['Jahr']})")
    
    # Visualisierung der Ergebnisse
    plot_results(len(public_domain_works), len(protected_works))

# Ausführung des Programms
if __name__ == '__main__':
    main()
