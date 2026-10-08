
### MAIN objective
Dimension reduction




VAE - redukcja wymiaru - przykłady

Reduckja wymiaru nazw
- możemy str zamienić na współrzędne i później to zdekodować 
- 

Nadmiar wymiaru
- możemy znaleźć dodatkowe cechy które spełniają pewen wartości 
    - trzeba zastosować regularyzacje 

Autoencodery
- chcemy stworzyć przestrzeń zawierającą dodatkowe informacje 

Loss
- just determine difference between encoding and decoded 


autoencodey
- chcemy odtworzyć rozkład normlalny
    - potrzebujem średnią oraz waraiancję wyestymować 
- loss
    - prawpdopodobieńśtwo żę ten rozkład został wylosowany z tego rozkłądu 
    - parametr $\beta$, pozwala nam zwiększac wpływ kulback'a liebliera żeby miał większy wplyw w stosunki do reconstruction error 