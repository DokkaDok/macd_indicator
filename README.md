---
Author:
- |
  Artur Szlędak, s197633 |
  Politechnika Gdańska |
  Kierunek: Informatyka |
  Semestr: 4 | Grupa: 1B
Title: 'Metody Numeryczne - Wskaźnik MACD'
---

Spis Treści
===========

1.  Wstęp

2.  Metodologia

3.  Analiza

4.  Symulacja portfela inwestora

5.  Podsumowanie

Wstęp
=====

-   Celem projektu jest analiza wyznacznika giełdowego MACD *(ang.
    Moving Average Convergence/Divergence)* na przykładzie indeksu S&P
    500 (SPX). Analiza zawiera symulację kapitału inwestora
    korzystającego z wyznacznika MACD oraz strategię \"Kup i Trzymaj\".

-   Dane zostały pobrane ze strony
    [nasdaq.com](https://www.nasdaq.com/market-activity/index/spx/historical).
    Rama czasowa obejmuje 1451 dni od 10.03.2021r. do 28.02.2025r. Do
    ustalenia wartości akcji została użyta cena zamknięcia z danego
    dnia. Ze względu na brakujące dane, łącznie wychodzi 999 dni.

-   Projekt został wykonany z użyciem języka Python i bibliotek tj.
    matplotlib, numpy, pandas.

-   Podstawowe założenie poniższej pracy opiera się na inwestowaniu na
    platformie umożliwiającej zakup akcji ułamkowych bez minimalnych
    kosztów transakcyjnych. Wynika ono z faktu, że obliczanie akcji
    ułamkowych do minimalnej wpłaty np. 10 PLN (standard brokerów) nie
    miało by różnicy na wyniki analizy z uwagi na niski koszt wpłaty
    przy dużym kapitale inwestora. Kwestia podatku od zysków
    kapitałowych wynoszącego 19% zostanie omówiona w podsumowaniu.

Metodologia
===========

-   Wyznacznik MACD został obliczony na podstawie wzoru:

    $$MACD = EMA_{12}-EMA_{26}$$

    gdzie:

    \- EMA12 oznacza 12-okresową wykładniczą średnią kroczącą - EMA26
    oznacza 26-okresową wykładniczą średnią kroczącą

-   Wartość EMA została obliczona rekurencyjnie ze wzoru:

    $$EMA_N(i) = \alpha\cdot x +(1-\alpha) \cdot EMA_N(i-1)$$

    gdzie:

    \- Cena zamknięcia w i-tym przedziale czasu (okresie): xi - Liczba
    okresów: N - Współczynnik wygładzający: $$\alpha = \frac{2}{N + 1}$$

Analiza
=======

Wszystkie wartości monetarne zostały przedstawione w USD. Kurs (USD/PLN)
w momencie tworzenia analizy: 1 USD = 3.85 PLN.

![Stock Over Time](https://github.com/DokkaDok/macd_indicator/blob/main/Photos/StockPriceOverTime.png?raw=true)

Na wykresie można zauważyć ogólny trend wzrostowy cen indeksu S&P 500 w
latach 2021--2025. Widać również spadek poniżej 4000 USD w okresie
06.2022 - 06.2023. Widnieje dużo punktów, gdzie potencjalny inwestor
mógłby się wzbogacić przy dynamicznym inwestowaniu, jednak samo
trzymanie środków również dałoby duży zysk. Dokładniejsze wyniki
strategii \"Kup i Trzymaj\" zostaną opisane w późniejszym etapie pracy.

![MACD and Signal Lines](https://github.com/DokkaDok/macd_indicator/blob/main/Photos/MACD_SIGNAL.png?raw=true)

Przecięcia linii MACD i Signal wyznaczają potencjalne punkty kupna i
sprzedaży. Gdy krzywa MACD przecina krzywą Signal od dołu, oznacza to
kupno, a gdy krzywa MACD przecina krzywą Signal od góry, oznacza to
sprzedaż. Dzięki takiemu rozwiązaniu można otrzymać strategie
inwestycyjną, która pozowli na sprzedanie 100% posiadanych akcji i kupno
możliwie jak najwięcej akcji, wraz z akcjami ułamkowymi w odpowiednich
punktach. 

Poniższa część pracy będzie się opierać na analizie
wyznacznika MACD przy użyciu z wykresem notowań finansowych.
Podsumowanie skuteczności wyznacznika MACD zostaną opisane na podstawie
analizy i zobrazowania dwóch różnych okresów, by znaleźć różnice, zalety
i wady. Okresy zawierają 7-8 punktów przecięć krzywych MACD i Signal.

![Stock Over Time in Date Range1](https://github.com/DokkaDok/macd_indicator/blob/main/Photos/SubplotForStockOverTime610_700.png?raw=true)

W przedstawionym okresie widzimy dynamiczny wykres z dużymi skokami,
ocena zmiany rynku byłaby ciężka, a trzymanie akcji od początku okresu
przyniosłoby stratę. Analizując akcje wykonane przez wskaźnik MACD
widzimy podjęte błędne decyzje. Często cena sprzedaży akcji jest niższa
niż cena jej zakupu. 

Przerywane linie wyznaczają największe różnice w
cenie, ważne jest aby kupować po niższej cenie i sprzedawać po wyższej,
przerywane linie ukazują, gdzie byłaby największa możliwa strata/zysk.
Można zauważyć, że przy różnicy malejącej została odniesiona duża
strata. Przy różnicy rosnącej doszło do zwiększenia kapitału. 

Warto skupić się na wyróżnionych punktach, gdyby inwestor czekał na dołek i
nie sugerował się wcześniejszym wyznacznikiem kupna mógłbym zwiększyć
swój zysk, negując przy okazji główną stratę. Wyznacznik odpowiednio
przewidział późniejszy spadek akcji, sprzedając trochę wcześniej niż po
możliwie najwyższej cenie, lecz można to uznać za obronę przed spadkiem.
Wizualizacja portfela podczas tego okresu pozwala na lepszy obraz
skuteczności wskaźnika.

![Wallet Value in Date Range](https://github.com/DokkaDok/macd_indicator/blob/main/Photos/WalletOver610_700.png?raw=true)

Wizualizacja wartości portfela potwierdza wcześniejsze obserwacje. Tylko
jedna operacja doprowadziła do zysku względem poprzedniego stanu
portfela i po dwóch operacjach inwestor miał większy kapitał od kapitału
początkowego. Ostatecznie stan portfela wzrósł o $\sim$1.83% więcej
względem kapitału początkowego. Wracając do Rysunku 3, gdyby nasz
inwestor nie kupowałby akcji po wyróżnionej sprzedaży, wyszedł by 3.77%
na plus względem stanu początkowego, co stanowi zmianę +1.94 punktu
procentowego od uzyskanego wyniku.

![Stock Over Time in Date Range2](https://github.com/DokkaDok/macd_indicator/blob/main/Photos/SubplotForStockOverTime220_400.png?raw=true)

W przeciwieństwie do Rysunku 3, następny wybrany okres pokazuję, że
gdyby inwestor trzymał swoje środki wyszedł by na plus. Można zauważyć
tylko jedną błędną propozycje kupna/sprzedaży wskaźnika MACD podczas
ósmego miesiąca. Zwracając uwagę na poprawne typy transakcji przy
najwyższych różnicach cenowych można zauważyć że wyznacznik poprawnie
przewidział spadki i wzrosty cen. 

Wyróżnione punkty pokazują największy
możliwy zysk gdyby inwestor nie postępował zgodnie z sugestiami
wskaźnika między nimi. Propozycje wskaźnika zmniejszają ilość akcji
jakie inwestor posiada, zmniejszając przyszłościowy zysk, jednak
zauważmy że częściowo zabezpieczają inwestora przed ewentualnym
\"crash-em\", a całościowo można stwierdzić że w tym przypadku
wyznacznik poradził sobie bardzo dobrze.

![Wallet Value in Date Range](https://github.com/DokkaDok/macd_indicator/blob/main/Photos/WalletOver220_400.png?raw=true)

Wartość portfela lepiej pokazuje efektywność wykonywanych transakcji,
wzrost wartości portfela o $\sim$15% w okresie dziesięciu miesięcy można
uznać jako dobry wynik z dodatkowym zabezpieczeniem przed ewentualnymi
drastycznymi spadkami.

Symulacja portfela inwestora
============================

![Wallet Capital Overtime](https://github.com/DokkaDok/macd_indicator/blob/main/Photos/WalletOverTime.png?raw=true)

Kapitał portfela symulowanego przy użyciu wskaźnika MACD podąża za
ogólnym trendem indeksu S&P 500. Nie jest to korzystne, ponieważ
oznacza, że strategia nie przynosi znaczącej przewagi inwestycyjnej.
Można zauważyć 19 pozytywnych transakcji i 18 negatywnych transakcji z
dużym zgrupowaniem negatywnych transakcji przy końcowym okresie. -
Początkowy stan portfela: 3.962.710,00 USD 
- Ostateczny stan portfela przy strategi MACD wyniósł: 5.210.384,00 USD
- Ostateczny stan portfela przy strategi \"Kup i Trzymaj\" wyniósł: 5.954.500,00 USD

Wzrost strategi MACD wyniósł: 31.48% \| Wzrost strategi \"Kup i
Trzymaj\" wyniósł: 50.26% 

Jest to różnica w wysokości 18.78 punktu
procentowego na korzyść strategi pasywnej. Indeks S&P 500 jest znany za
stabilny wzrost, minimalizując przy okazji wpływy wahań
krótkoterminowych. Strategia MACD generowała wyraźne większe zyski niż
straty, jednak nie były wystarczające by pokonać strategię \"Kup i
Trzymaj\".

Warto również rozważyć inflację. Korzystając z narzędzia
[policzmi.pl](https://policzmi.pl/inflacje) można się dowiedzieć że w
opracowywanym okresie skumulowana inflacja wyniosła o 40,28%. Oznacza to
że początkowe 3.962.710,00 USD sprowadza się do 5.558.796,00 USD. Biorąc
te informację pod uwagę, środki uzyskane ze strategi MACD mogłyby
zapewnić mniej dóbr, niż początkowy kapitał inwestora. W przeciwieństwie
to całkowitego wzrostu indeksu S&P 500, który przyniósłby zysk.

Podsumowanie
============

-   W okresach dynamicznych strategia MACD wyznaczała dużo błędnych
    sygnałów, doprowadzając do strat.

-   W okresach stabilnego wzrostu wskaźnik działał lepiej, dodatkowo
    ubezpieczając przeciwko ewentualnym spadkom.

-   Po uwzględnieniu skumulowanej inflacji przez okres 4 lat, realna
    wartość portfela zmniejszyła się, co oznacza spadek siły nabywczej.
    Dodatkowo, uwzględnienie 19% podatku od każdej transakcji sprzedaży
    jeszcze bardziej obniżyłoby efektywność strategii MACD.

-   Wskaźnik MACD nie sprawdził się samodzielnie jako dobre narzędzie
    inwestycyjne, do uzyskania lepszych wyników potrzeba wiedzy
    technicznej i znajomości rynku. W przypadku inwestowania w indeks
    S&P 500, dużą liczbę błędnych sygnałów można było ominąć trzymając
    przez dłuższy okres akcje, ze świadomością ogólnej tendencji
    wzrostowej indeksu. Niemniej jednak posiada on zaletę ubezpieczania
    przed nieplanowanymi spadkami.

-   Warto rozważyć rozszerzenie analizy strategii MACD o
    przeanalizowanie dodatkowych bardziej statyczne rynki lub dodaniem
    dodatkowej optymalizacji opartej na innych wskaźnikach, czy nawet
    sztucznej inteligencji.
