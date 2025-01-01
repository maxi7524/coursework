# numerical-methods_IS

## Wprowadzenie

Dokument ten opisuje metody numeryczne stosowane w badaniach. Celem jest zrozumienie, jak różne metody wpływają na efektywność próbkowania w symulacjach Monte Carlo.

## Metody badawcze

### Metoda

W badaniach analizujemy różne wartości \( p_t \) i obserwujemy, jak zmienia się zysk symulacji. To pozwala nam określić, ile dodatkowych próbek należy dodać w metodzie Monte Carlo, aby osiągnąć tę samą precyzję, co w metodzie IS.

Wybieramy coraz mniej prawdopodobne zdarzenia i sprawdzamy, jak dla optymalnych wartości zwiększa się liczba próbek potrzebnych w metodzie Monte Carlo, aby uzyskać podobne wyniki.

### Uwagi

- **Funkcja `quad`**: Należy zachować ostrożność przy całkowaniu dystrybucji. Wartości poza przedzialem 15-30 od środka dystrybucji są tak małe, że całka może nie być zbieżna z powodu błędów numerycznych. Błąd przy całkowaniu wynosi około \( e^{-8} \), co oznacza, że są to dokładne pomiary.

- **Porównanie metod (translacja vs. scaling)**:
  - Należy zastanowić się, dlaczego translacja osiąga lepszy wzrost efektywności, mimo że scaling na rzeczywistych danych osiąga mniejsze błędy.
  - Przy błędach estymacji błąd Monte Carlo staje się liniowy po pewnym czasie, jest to spowodowane tym że nie jest on w stanie wychwycić żadnej wartości tak daleko od środka rozkładu więc przypisuje prawdopodobieństwo 0.

## Metody

### Scaling

#### Weibull

- \( b = 1 \)
- \( \mu = 2 \)
- \( \text{max\_error} = 3.486882562314591e-08 \)

Funkcje i minimum były znajdowane explicite.

#### Normalny

- \( \mu = 0 \)
- \( \sigma = 1 \)
- \( \text{max\_error} = 1.328265402247495e-08 \)

Minimum było znajdowane numerycznie. Należało ograniczyć przedział szukania, ponieważ spełnia warunek, że w nieskończoności maleje do zera. Na dużym przedziale (0, e5) znajdujemy sensowne wartości.

### Translation

#### Weibull

Parametry są takie same jak wcześniej.

**Ważne**: Nie ma sensu sprawdzać efektywności dla \( c > t \), ponieważ Weibull jest jednostronny. W takim przypadku mamy po prostu 0 wszędzie, a dla \( c > t \) zawsze będzie to największe dostępne \( c \), co sprawia, że całka nie istnieje. Dlatego szukając minimum ograniczamy się do wartości \( t\).

#### Normalny

Jest efektywniejszy.

## TODO

- Należy stworzyć metodę łączącą scaling z translation.
- Sprawdzić, dlaczego porównania wychodzą dziwne.

## Schemat obliecznia.ipynb

Obliczenia to notatnik, w którym przechowujemy różne eksperymenty i obliczenia związane z metodami numerycznymi. Zawiera on:

- **Importy**: Biblioteki używane w obliczeniach, takie jak NumPy, Pandas, SciPy i Matplotlib.
- **Funkcje**: Definicje funkcji do estymacji i obliczeń, takich jak `monte_carlo_estimate` i `simulation_gain_known`.
- **Wizualizacje**: Wykresy ilustrujące wyniki symulacji i efektywność różnych metod.

Dokumentacja brudnopisu jest kluczowa dla zrozumienia przeprowadzonych eksperymentów i uzyskanych wyników. Zawiera również uwagi dotyczące potencjalnych problemów i błędów, które mogą wystąpić podczas analizy danych. 