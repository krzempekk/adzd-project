## Cel projektu
Celem projektu jest zaprezentowanie rożnych wykresów przedstawiajacych ciekawe zależności z milionów partii szachowych. Wśród nich znajdą się:
- wykresy obrazujące procent zwycięstw danego koloru w zależności od czasu,
- hot-mapa wizualizująca gdzie najczęściej zostaje wykonany ruch,
- rozkład przedstawiający liczbę ruchów w partiach,
- porównania powyższych zależności między najlepszymi graczami, a średnim poziomem,
- porównanie powyższych statystyk w zależności od ilości czasu na każdego gracza.




## Lista problemów koncepcyjnych do rozwiązania
1) Niestandardowy format wejścia (notacja PGN). Format ten pozwala odtworzyć partię poprzez zapis kolejnych ruchów. Całościowe odtwarzanie parti ma jednak duży nakład czasowy i aby odpowiednie statystyki były obliczalne w sensownym czasie, będzie to wymagało innego sposobu przetwarzania danych. 
2) Uruchomienie aplikacji na klastrze AWS na koncie AWS Academy. Z powodu braku uprawnień na wiele dostępnych funkcji, uruchomienie nie będzie tak proste jak zakładają autorzy Raya. 

## Schemat architektury

![](/docs/images/architecture.png)

## Planowane testy
1) Infrastruktura - klaster na AWS
2) Zbiór danych:
    - partie najlepszych graczy https://www.pgnmentor.com/files.html#interzonal
    - partie z popularnej strony szachowej https://database.lichess.org/
3) Metryki:
    - Przyspieszenie
    - Efektywność
    - Karp-Flatt

## Szkic rozwiązania
 - Do przetworzenia danych zostanie wykorzystana biblioteka Ray (https://github.com/ray-project/ray). Infrastruktura zostanie postawiona na AWS.