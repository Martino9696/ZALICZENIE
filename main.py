import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt


class Klient:
    def __init__(self, imie, waga, wzrost, jednostka='m'):
        self.imie = imie
        self.waga = waga
        self.wzrost = wzrost / 100 if jednostka == 'c' else wzrost
        self.bmi = self.oblicz_bmi()
        self.kategoria = self.interpretuj_bmi()

    def oblicz_bmi(self):
        return self.waga / (self.wzrost ** 2)

    def interpretuj_bmi(self):
        bmi = self.bmi
        if bmi < 16:
            return "Wygłodzenie"
        elif 16 <= bmi < 17:
            return "Wychudzenie"
        elif 17 <= bmi < 18.5:
            return "Niedowaga"
        elif 18.5 <= bmi < 25:
            return "Waga prawidłowa"
        elif 25 <= bmi < 30:
            return "Nadwaga"
        elif 30 <= bmi < 35:
            return "Otyłość I stopnia"
        elif 35 <= bmi < 40:
            return "Otyłość II stopnia"
        else:
            return "Otyłość III stopnia (skrajna)"


class BazaDanychBMI:
    def __init__(self, plik='historia_bmi.csv'):
        self.plik = plik
        self.naglowki = ['Data', 'Klient', 'Waga', 'Wzrost_m', 'BMI', 'Kategoria']

    def zapisz(self, klient: Klient):
        plik_istnieje = os.path.exists(self.plik)
        with open(self.plik, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.naglowki)
            if not plik_istnieje:
                writer.writeheader()
            writer.writerow({
                'Data': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Klient': klient.imie,
                'Waga': klient.waga,
                'Wzrost_m': round(klient.wzrost, 2),
                'BMI': round(klient.bmi, 2),
                'Kategoria': klient.kategoria
            })


class WykresBMI:
    def __init__(self, plik='historia_bmi.csv'):
        self.plik = plik

    def pokaz(self, imie_klienta):
        daty = []
        wagi = []
        with open(self.plik, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Klient'].lower() == imie_klienta.lower():
                    daty.append(datetime.strptime(row['Data'], "%Y-%m-%d %H:%M:%S"))
                    wagi.append(float(row['Waga']))
        if daty:
            plt.plot(daty, wagi, marker='o')
            plt.title(f"Waga w czasie - {imie_klienta}")
            plt.xlabel("Data")
            plt.ylabel("Waga (kg)")
            plt.grid(True)
            plt.show()
        else:
            print("Brak danych do wyświetlenia wykresu.")


class AplikacjaBMI:
    def __init__(self):
        self.baza = BazaDanychBMI()
        self.wykres = WykresBMI()

    def pobierz_float(self, prompt):
        while True:
            try:
                wartosc = float(input(prompt))
                if wartosc <= 0:
                    print("Wartość musi być większa niż 0.")
                else:
                    return wartosc
            except ValueError:
                print("Niepoprawna liczba.")

    def uruchom(self):
        print("=== Kalkulator BMI ===")

        while True:
            imie = input("Podaj imię klienta: ")
            waga = self.pobierz_float("Podaj wagę (w kg): ")
            wzrost = self.pobierz_float("Podaj wzrost (np. 175 dla cm lub 1.75 dla m): ")
            jednostka = input("Czy wzrost jest w [c]entymetrach czy [m]etrach? (c/m): ").lower()

            klient = Klient(imie, waga, wzrost, jednostka)

            print(f"\nBMI: {klient.bmi:.2f} — {klient.kategoria}")

            self.baza.zapisz(klient)

            if input("Czy chcesz zobaczyć wykres zmian wagi? (tak/nie): ").lower() == 'tak':
                self.wykres.pokaz(imie)

            if input("\nCzy chcesz dodać kolejne dane? (tak/nie): ").lower() != 'tak':
                break

        print("Dziękuję za skorzystanie z aplikacji!")


if __name__ == "__main__":
    app = AplikacjaBMI()
    app.uruchom()