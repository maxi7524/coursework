


# TODO 
- trzeba zrobić pipeline'y z obrabianiem tych plików przez jakiegoś snakemake
- wtedy byśmy mogli zrobić ogólny plik który wybiera metoda i przekierowuje całość ustawień i zarządza plikami, znajdując które są źle podane 


plan działania
- mamy główny skrypt który wszystkim zarządza
    - robi pipeline po wszystkich strukturach i je porównuje (bo te programy chyba nie obsługują kilku plików, jak obsłgują to damy parametr ile na raz ma byc robionych) 
    
- główny skrypt 
    - sprawdzanie folderów input / output, dorabianie (jakiś snakemake?) które czynności mają być zrobione (wtedy ostatecznie będzie żądać formatu raportu) i wtedy wykonuje wszystkie wybrakowane pliki
    - argument
        - input (w jakim folderze mamy dane)
            - przyjmuje złaczaone (wszystkie pliki w jednym folderze) 
            - przyjmujemy folder z folderami (parametr -r jeśli koniczne by to było) 
        - output w zależności czy są podfoldery czy nie to zbiera nam całość odpowiednio względem nazw folderów 
        - metoda
            - każda metoda będzie musiała zostać podana ORAZ dodatkowe parametry do niej
            - będzie trzeba napisać jakie parametry są obsługiwane per metoda 
        - raport
            - podać argument czy chcemy raport lub i jaki styl (brak argumentu, none - brak raportu, w przypadku argumentu byśmy mieli zrobione wychwytywanie formatów, ALE trzeba to przemyśleć ponieważ trzeba by wtedy zrobić tak, że niezależnie od pobrania robi dobry format, wiec pobrane wszystko musiało by być w określonym formacie, i potem były by nakładki które to zbierają. 
    - imlementacja 
        - implementuje tylko kilka metod 
            - blast   
            - tmalign
            - jakaś jedna wybrana przejrzeć 


- skrypt robiący raport
    - tutaj (to będzie ciężkie) wykryć formatu output'u 

Implementacja 
- snake_make który będzie tym zarządzał 