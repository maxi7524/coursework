# 
openpyxl

# Struktura
## Pliki
#TODO 
- data 
    - wykresy
    - csv
- projekt_1_student.ipynb
## Dane
### Kod stacji
Przyjmujemy:
- x = [:lower:]
- X = [:upper:]
Kody są postaci:

    WwPp\*Nn\*

Gdzie:
Ww - oznacza województwo
Pp - oznacza powiat 
Nn - oznacza nazwe stacji

# Opis 
## 1. Wczytanie i czyszczenie danych
## 2. Średnie miesięczne 
## 3. Heatmapa miesięcznych średnich
## 4. Dni z przekroczeniem normy 

# Wykonane rzeczy 
Tutaj nie wiem jak to opisywać, jak bym to jakoś wypisywał po kolei i problemy jakie się pojawiły dla danej osoby, bezwstydu to należy pytać bo wtedy możemy się zastanowić nad problemem który wystąpił, forma wynika oczywiście z tego, że się nie widzimy na zajęciach, wolałbym bym sobie to po prostu omówić. 

## Co nowego:
### Wtorek
- Zamienienie lini zmieniającej NA values 
- zaimplementowanie nowych funkcji do zadań 2, 3
    - są tutaj funkcje które pozwalają na sortowanie wartości `time_to_month` i `get_tations` które można użyć w zadaniu 4


# UWAGI 
## Max -> Aleksandra
### Opis funkcji
#### definiowanie typu obiektów
Możesz predefiniować typy które występują w danej funkcji:
```Python
def function(arg: float) -> float:
    pass
```
To trochę pomaga w czytelności, ale to jest głównie dla mnie pomocne jak programuje ponieważ jak nadasz typ parametrowi, to masz dostęp do wszystkich metod danej klasy. 
#### Dokumentacja funkcji
Ja bym proponował, żeby zrobić opis operacji które są wykonywane w tej funkcji, można input opisać jaki jest przyjmowany obiekt (jako przykład moje funkcje)
#### Format 
zastanawiałem się czy zamiast pisania tych funkcji i kodu po kolei, nie zrobiliśmy klasy która tym w której były by metody odpowiedzialne za ładowanie danych itd. bo wtedy kod jest czytelniejszy i niektóre działania były by znacznie szybsze - byśmy zrobili odpowiednie zbiory które trzymały by wartości odpowiednich zbiorów itd. Możemy też zostawić tak jak jest 
### Raport 
Myślałem nad tym, żeby przy / nad ładowaniem danych opisać dokładnie format danych, o tym jak są przechowywane i jak nimi zarządzać. Nie zauważyłem że w metadata jest tak na dobrą sprawę słownik który pozwala na wygodne szukanie określonych indeksów, dlatego mi to tyle zajeło - tworzyłem funkcje która to robi. 


### Konstrukcja with open 
- wiem że to oni robili ale:
    - Sprawdzanie wartości `filename` jest nie potrzebne - filename jest parametrem pozycyjnym, jak się go nie poda otrzymamy `TypeError`
### 


## Aleksandra -> Max