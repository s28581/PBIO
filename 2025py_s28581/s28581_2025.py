# Cel programu:
# Program generuje losową sekwencję DNA w formacie FASTA, umożliwiając użytkownikowi określenie długości sekwencji,
# ID oraz opisu. W losowe miejsce sekwencji wstawiane jest imię użytkownika (nie wpływa na statystyki).
# Program wylicza statystyki procentowe zawartości nukleotydów i zapisuje dane do pliku w formacie FASTA.

import random

def generate_random_dna(length):
    """Generuje losową sekwencję DNA z nukleotydów A, C, G, T"""
    return ''.join(random.choices('ACGT', k=length))

def insert_name(sequence, name):
    """Wstawia imię użytkownika w losowe miejsce sekwencji DNA (nie wpływa na długość)"""
    index = random.randint(0, len(sequence))
    return sequence[:index] + name + sequence[index:]

def calculate_statistics(sequence):
    """Oblicza statystyki sekwencji DNA"""
    # Filtrujemy tylko prawdziwe nukleotydy
    clean_sequence = ''.join([base for base in sequence if base in 'ACGT'])

    total = len(clean_sequence)
    stats = {nucleotide: clean_sequence.count(nucleotide) / total * 100 for nucleotide in 'ACGT'}
    cg = stats['C'] + stats['G']
    return stats, cg

def save_fasta(id_, description, sequence):
    """Zapisuje dane do pliku w formacie FASTA"""
    filename = f"{id_}.fasta"
    with open(filename, 'w') as file:
        file.write(f">{id_} {description}\n")
        # ORIGINAL:
        # file.write(sequence + "\n")
        # MODIFIED (dzielenie sekwencji na linie po 60 znaków):
        for i in range(0, len(sequence), 60):
            file.write(sequence[i:i + 60] + "\n")

    print(f"Sekwencja została zapisana do pliku {filename}")

# Główna część programu
# ORIGINAL:
# length = int(input("Podaj długość sekwencji: "))
# MODIFIED (dodano walidację długości sekwencji - tylko dodatnie liczby całkowite):
while True:
    try:
        length = int(input("Podaj długość sekwencji: "))
        if length > 0:
            break
        else:
            print("Długość musi być większa od zera.")
    except ValueError:
        print("Proszę podać poprawną liczbę całkowitą.")

id_ = input("Podaj ID sekwencji: ")
description = input("Podaj opis sekwencji: ")
# ORIGINAL:
#name = input("Podaj imię: ")

# MODIFIED (dodano implementacje imienia malymi literami, aby litery imienia nie wliczały sie w statystyki sekwencji):
name = input("Podaj imię: ").lower()

dna_sequence = generate_random_dna(length)
final_sequence = insert_name(dna_sequence, name)
stats, cg_ratio = calculate_statistics(final_sequence)

save_fasta(id_, description, final_sequence)

# Wyświetlenie statystyk
print("Statystyki sekwencji:")
for nucleotide, percentage in stats.items():
    print(f"{nucleotide}: {percentage:.1f}%")
print(f"%CG: {cg_ratio:.1f}")
