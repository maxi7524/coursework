# numerical-methods_IS


### scaling 

#### Weibull

b = 1
mu = 2 
max_error = 3.486882562314591e-08

funkcje i minimum było znajdowane explicite 

#### Normalny

mu = 0
sigma = 1
max_error = 1.328265402247495e-08

minimum było znajdowane numeryczne, trzeba było ograniczyć przedział szukania (ponieważ spełnia warunek że w nieskończoności maleje do zera, na dużym przedziale znajduje sensowne wartości (0, e5), znajduje [1, 6])

### translation 

#### Weibull 
    parametry te co poprzednio 

    ważne: nie ma sensu sprawdzać efektywności dla c > t poniewaz weibull jest jednostronny z tego wynika że mam po prostu 0 wszędzie i dla c > t zawsze będzie to największe dostępne c, ale wtedy całka nie istnieje 

#### Normalny 
    jest efektywniejszy 
