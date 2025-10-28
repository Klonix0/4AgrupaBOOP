from __future__ import annotations
from typing import List

class Zaposlenik:
    """Osnovna klasa za sve zaposlenike."""
    def __init__(self, ime: str, prezime: str, placa: float) -> None:
        # Spremamo osnovne podatke kao atribute objekta
        self.ime = ime
        self.prezime = prezime
        self.placa = placa

    def prikazi_info(self) -> None:
        """Ispis osnovnih podataka o zaposleniku."""
        print(f"Ime i prezime: {self.ime} {self.prezime}, Plaća: {self.placa} EUR")


class Programer(Zaposlenik):
    """Programer je također zaposlenik, ali ima listu programskih jezika."""
    def __init__(self, ime: str, prezime: str, placa: float, programski_jezici: List[str]) -> None:
        # Pozivamo konstruktor roditeljske klase da postavi ime, prezime i plaću
        super().__init__(ime, prezime, placa)
        # Dodatni atribut specifičan za Programera
        self.programski_jezici = programski_jezici

    def prikazi_info(self) -> None:
        """Ispis podataka za Programera: osnovni podaci + jezici."""
        # Prvo ispiši osnovne podatke iz roditeljske klase
        super().prikazi_info()
        # Zatim i listu programskih jezika
        if self.programski_jezici:
            jezici = ", ".join(self.programski_jezici)
        else:
            jezici = "—"
        print(f"Programski jezici: {jezici}")


class Menadzer(Zaposlenik):
    """Menadžer je zaposlenik koji upravlja timom (listom imena)."""
    def __init__(self, ime: str, prezime: str, placa: float, tim: List[str]) -> None:
        # Poziv roditeljske klase
        super().__init__(ime, prezime, placa)
        # Dodatni atribut: tim (lista stringova s imenima članova)
        self.tim = list(tim)  # kopija radi sigurnosti

    def prikazi_info(self) -> None:
        """Ispis podataka za Menadžera: osnovni podaci + članovi tima."""
        super().prikazi_info()
        if self.tim:
            clanovi = ", ".join(self.tim)
        else:
            clanovi = "—"
        print(f"Tim: {clanovi}")

    # BONUS: dodavanje novog člana tima
    def dodaj_clana_tima(self, novi_clan: str) -> None:
        """Dodaje novog člana u tim (ako već nije unutra)."""
        if novi_clan not in self.tim:
            self.tim.append(novi_clan)


if __name__ == "__main__":
    # --- Testiranje po uputama iz radnog listića ---
    z1 = Zaposlenik("Atilio", "Marečić", 600)
    p1 = Programer("Lara", "Perković", 200, ["Python", "JavaScript"])
    m1 = Menadzer("Borna", "Lakoseljac", 250000, ["Atilio Marečić", "Lara Perković"])

    print("--- Podaci o zaposleniku ---")
    z1.prikazi_info()

    print("\n--- Podaci o programeru ---")
    p1.prikazi_info()

    print("\n--- Podaci o menadžeru ---")
    m1.prikazi_info()

    # BONUS: demonstracija dodavanja člana tima
    m1.dodaj_clana_tima("Aljoša")
    print("\n Nakon dodavanja novog člana")
    m1.prikazi_info()
