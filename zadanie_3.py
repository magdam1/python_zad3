# Autorzy: Magdalena Molenda, Iwona Raczkowska
# Program tworzący zadane argumentami katalogi,
# oraz odczytujący dane z / wpisujący dane do plików csv.

import argparse, random, os

month_names   = [  "sty", "lut", "mar", "kwi", "maj",
                   "cze", "lip", "sie", "wrz",
                   "paź", "lis", "gru"  ]

weekday_names = [  "pn", "wt", "śr", "cz", "pt", "so", "nd"  ]

time_of_day   = [  "r", "w"  ]

mode          = [  "o", "t"  ]

# Funkcja rozdziela dni oraz sprawdza poprawność danych.
def parse_grouped_days(all_days):
    parsed_days = []
    nr_of_days = 0
    for group in all_days:
        days = group.split(",")
        nr_of_days += len(days)
        valid = [d for d in days if d in weekday_names]
        invalid = [d for d in days if d not in weekday_names]
        if invalid:
            raise argparse.ArgumentTypeError("Nieprawidłowe nazwy dni tygodnia")
        parsed_days.append(valid)
    return parsed_days, nr_of_days

path_tuples = []

parser = argparse.ArgumentParser()
day_parser = argparse.ArgumentParser()

# Parsowanie miesięcy, pór dnia i trybu
parser.add_argument("--months", nargs="+", required=True,
                    choices=month_names, help="Podaj miesiące")
parser.add_argument("--times", nargs="*", default=["r"],
                    choices=time_of_day, help="Podaj pory dnia")
parser.add_argument("--mode", choices=mode, default="o", help="Podaj tryb: odczyt (o) lub tworzenie (t)")
parsed, remaining = parser.parse_known_args()

months_chosen = { month: '' for month in parsed.months }

# Parsowanie dni tygodnia
day_parser.add_argument("--days", nargs=len(months_chosen), type=str,  required=True,
                    help="Podaj dni tygodnia")
day_parser.parse_args(remaining, namespace=parsed)

days_by_month, nr_of_days = parse_grouped_days(parsed.days)

# Dopełnienie listy pór dnia domyślnymi wartościami
remainder = ["r"] * (nr_of_days-len(parsed.times))
times_chosen = parsed.times+remainder

# Tworzenie listy wszystkich ścieżek
for (month, days) in zip(months_chosen, days_by_month):
    for day in days:
        path_tuples.append((month, day))

path_tuples = [(month, day, time) for ((month, day), time) in zip(path_tuples, times_chosen)]

print(path_tuples)

# Tworzenie katalogów i zapis plików
if parsed.mode == "t":
    for (month, day, time) in path_tuples:
        # Ścieżka katalogu np. "sty/pn/r"
        dir_path = os.path.join(month, day, time)
        os.makedirs(dir_path, exist_ok=True)

        # Pełna ścieżka do pliku CSV
        file_path = os.path.join(dir_path, "Dane.csv")

        # Zapis danych do pliku
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            f.write("Model; Wynik; Czas\n")
            letter = random.choice(["A", "B", "C"])
            x, y = random.randint(0, 1000), random.randint(0, 1000)
            f.write(f"{letter}; {x}; {y}s\n")

        print(f"Utworzono plik: {file_path}")


# Odczyt i sumowanie danych
if parsed.mode == "o":
    total_time = 0
    found_files = 0

    for (month, day, time) in path_tuples:
        file_path = os.path.join(month, day, time, "Dane.csv")

        if os.path.exists(file_path):
            found_files += 1
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()[1:]
                for line in lines:
                    parts = [p.strip() for p in line.split(";")]
                    if len(parts) >= 3:
                        model, _, czas = parts
                        if model == "A":
                            try:
                                total_time += int(czas.replace("s", "").strip())
                            except ValueError:
                                pass

    if found_files == 0:
        print("Nie znaleziono żadnych plików Dane.csv.")
    else:
        print(f"Suma czasów (Model == A) ze wszystkich plików: {total_time}s")





