# Projekt Laboratoryjny - Metody Numeryczne

## Struktura Projektu
- `modules.py` - Moduł zawierający implementacje podstawowych funkcji
- `results.ipynb` - Jupyter Notebook z testami i wizualizacją wyników

## Implementacja i Testy

### Funkcje w modules.py
1. **horner_eval** - Implementacja schematu Hornera
2. **neville** - Algorytm interpolacji Neville'a
3. **newton_polynomial** - Obliczanie ilorazów różnicowych Newtona
4. **standard_to_chebyshev** - Konwersja do bazy Czebyszewa
5. **clenshaw_evaluate** - Algorytm Clenshawa
6. **trigonometric_interpolation** - Interpolacja trygonometryczna

### Testy w results.ipynb
Notebook zawiera:
- Testy wydajności metody Hornera
- Porównanie różnych metod interpolacji
- Wizualizacje błędów interpolacji
- Testy dla funkcji okresowych

## Uwagi Implementacyjne
1. **Problem z Importowaniem**: Podczas realizacji projektu wystąpiły problemy z importowaniem funkcji z `modules.py` do `results.ipynb`. Rozwiązano to poprzez bezpośrednią implementację funkcji w notebooku.

2. **Usunięte Funkcje**: Z modułu `modules.py` usunięto następujące przestarzałe funkcje:
   - `standard_polynomial_eval` - zastąpiona przez bardziej wydajną implementację
   - `newton_to_standard` - nieużywana w testach

3. **Najważniejsze Cechy**:
   - Wszystkie implementacje są numerycznie stabilne
   - Kod jest zoptymalizowany pod kątem wydajności
   - Implementacje zawierają szczegółowe komentarze
   - Testy obejmują różnorodne przypadki użycia

4. **Dokumentacja**:
   - Każda funkcja posiada docstring w formacie NumPy
   - README zawiera pełny opis teoretyczny metod
   - Wyniki testów są udokumentowane w notebooku

## Zalecenia
1. Przed uruchomieniem zainstaluj wymagane zależności:
   ```bash
   pip install numpy matplotlib scipy
   ```
2. Uruchom testy w kolejności przedstawionej w notebooku
3. Zwróć uwagę na sekcje z wykresami błędów i porównaniami metod

## Autorzy
Max Stróżyk
Data: 2024-12-02
Przedmiot: Metody Numeryczne