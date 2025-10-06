def carica_da_file(file_path):
    """Carica i libri dal file"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Errore: File non trovato al percorso: {file_path}")

    biblioteca = {}

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        try:
            num_sezioni = int(next(reader)[0])
            for i in range(1, num_sezioni + 1):
                biblioteca[i] = []
        except (StopIteration, ValueError, IndexError):
            print("Errore: Formato errato nella prima riga del file CSV.")
            return None

        for riga in reader:
            if len(riga) == 5:
                try:
                    titolo, autore, anno, pagine, sezione = riga
                    sezione_int = int(sezione)
                    if sezione_int in biblioteca:
                        libro = Libro(titolo, autore, anno, pagine, sezione_int)
                        biblioteca[sezione_int].append(libro)
                except ValueError:
                    pass

    print(f"Biblioteca caricata con successo.")
    return biblioteca


def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""

    if sezione not in biblioteca:
            print(f"Errore: La sezione {sezione} non esiste.")
            return None

    for sezione_libri in biblioteca.values():
            for libro in sezione_libri:
                if libro.titolo.lower() == titolo.strip().lower():
                    print(f"Errore: Il libro '{titolo}' è già presente.")
                    return None

    nuovo_libro = Libro(titolo, autore, anno, pagine, sezione)
    biblioteca[sezione].append(nuovo_libro)

    try:
        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            file.write('\n' + nuovo_libro.to_csv_row())
        return nuovo_libro
    except Exception as e:
        print(f"Errore durante l'aggiornamento del file CSV: {e}")
        biblioteca[sezione].pop()
        return None


def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""
    titolo_cercato = titolo.strip().lower()

    for sezione_libri in biblioteca.values():
        for libro in sezione_libri:
            if libro.titolo.lower() == titolo_cercato:
                return str(libro)

    return None


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    if sezione not in biblioteca:
        return None

    titoli = [libro.titolo for libro in biblioteca[sezione]]
    return sorted(titoli)


def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

