# Program tworzący zadane argumentami katalogi,
# oraz odczytujący dane z / wpisujący dane do plików csv.

import argparse, random

month_names   = [  "sty", "lut", "mar", "kwi", "maj",
                   "cze", "lip", "sie", "wrz",
                   "paź", "lis", "gru"  ]

weekday_names = [  "pn", "wt", "śr", "cz", "pt", "so", "nd"  ]

time_of_day   = [  "r", "w"  ]

mode          = [  "-o", "-t"  ]

# Funkcja rozdziela dni oraz sprawdza poprawność danych.
def parse_grouped_days(all_days):
    parsed_days = []
    nr_of_days = 0
    for group in all_days:
        days = group.split(",")
        nr_of_days += len(days)
        valid = {d for d in days if d in weekday_names}
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
parser.add_argument("--mode", nargs=1, default="o",
                    choices=mode, help="Podaj tryb: odczyt/tworzenie")
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

# TODO - stworzenie ścieżek

# Tworzenie pliku
if parsed.mode == ["t"]:
    # for (month, day, time) in path_tuples:
    # utworzyć plik pod odpowiednią ścieżką
    file = open("Dane.csv", "w")
    file.write("Model; Wynik; Czas;\n")
    letter = random.choice(["A", "B", "C"])
    x, y = random.randint(0, 1000), random.randint(0, 1000)
    file.write(str(letter)+"; "+str(x)+"; "+str(y)+"s;")
    file.close()

#else: TODO - odczyt z pliku

