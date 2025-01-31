# PAD Final Project by Wojciech Lach
## Prerequisites
`pip install matplotlib`  
`pip install numpy`  
`pip install pandas`  
`pip install seaborn`  
`pip install streamlit`  
`pip install sklearn`  
`pip install scipy`  
`pip install selenium`  
`Python at least 3.12`  
Źródło skąd zostały pobrane dane: https://www.flashscore.com/
## Start the program
Aby wystartować program należy włączyć plik main, który domyślnie jest
ustawiony na rozpoczęcie funkcji `main2()` czyli tej odpowiedzialnej za
analizę pobranych danych. Aby rozpocząć zbieranie danych należy zmienić
w linijce 39 w pliku `main.py` `main2()` na `main1()`. Aby skorzystać ze
`streamlit` należy w głównym katalogu projektu wykonać komendę:    
`streamlit run AnalyzeData/dashboard.py` jest ona również podana w pliku
`main.py` w linijce 35. Po wykonaniu tej komendy powinna się otworzyć
przeglądarka z dashboardami.
## Files
### Folder `AnalyzeData`
#### creating_graphs.py
Ten plik umożliwia tworzenie wykresów. Za pomocą pandas wczytywany
jest plik `.csv` po czym usuwane są kolumny takie jak:
``Opponent``, ``Result`` oraz ``Season`` gdyż nie są to wartości
liczbowe. Następnie wypisywane są podstawowe statystyki, oraz generowane
są:
- Macierz korelacji,
- Trendy dla statystyki 'Oczekiwane bramki', 'Posiadania piłki' oraz
dla strzelonych bramek
- Wyświetlana jest tabela krzyżowa
- Wizualizacje tabeli jako wykresu słupkowego oraz wizualizacja liczby spotkań
- z różnumi przeciwnikami

#### dashboard.py
Plik ten odpowiada za pokazanie dashboardów za pomocą biblioteki
`streamlit`. W pliku znajduje się funkcja, która zarządza danymi
wejściowymi, obsługą tego co jest wczytywane za pomocą `pandas`.
Następnie obsługiwane są kolumny "wyjątkowe". Po czym tworzone
są wykresy dla wszystkich opisanych sekcji, które są opisane
w tym pliku, oraz w wygenerowanym dashboardzie przez `streamlit`.

#### modeling.py
Plik ten odpowiada za stworzenie modelu regresji logistycznej do
klasyfikacji. Dane są wczytywane i wstępnie czyszczone, po czym
tworzone są cechy `x` oraz etykiety `y`, gdzie `x` zawiera cechy meczu
takie jak oczekiwane bramki czy posiadanie piłki. `y` natomiast to etykieta
wyniku meczu gdzie 1 - to wygrana a 0 - to przegrana. Następnie tworzony
jest podział na zbiór treningowy i testowy w skali 80/20 (80 - do treningu,
20 - do testu). Potem tworzony jest model `regresji logistycznej` i jest on
uczony. Na sam koniec model dokonuje przewidywań i wypisywany jest
raport do oceny.

#### tests.py
Plik ten odpowiada za przeprowadzanie 2 testów statystycznych czyli
w tym przypadku `testu chi-kwadrat` oraz `testu korelacji`. Test chi-kwadrat
sprawdza, czy istnieje zależność pomiędzy posiadaniem piłki a wynikiem
meczu, oraz sprawdza czy istnieje zależność pomiędzy spodziewanymi bramkami
a wynikiem meczu, jeśli wyniki są mniejsze niż `0.05` oznacza to, że
istnieje zależność między zmiennymi. Test korelacji sprawdza czy istnieje
zależność pomiędzy spodziewanymi bramkami a bramkami strzelonymi. Również
jak w przypadku `chi-kwadrat` jeśli wyniki są mniejsze niż `0.05` to
istnieje zależność między tymi zmiennymi. Do przeprowadzenia testów
została użyta biblioteka scipy

### Folder `ClearData`
#### add_data.py
Plik ten dodaje dodatkowe kolumny do pliku csv podczas operacji 
zbierania danych. Funkcja otrzymuje wartości zebrane podczas zbierania
danych i wykonuje na nich operacje przypisania do nowych wierszy. Na
koniec zwraca wynik, który jest dalej wykorzystywany w operacji zbierania
danych.

#### convert_data.py
Plik ten wykonuje konwersje danych takich jak: `%`, `(312/346)`, oraz
usuwa zbędne spacje . Jeśli wartość nie wymaga konwersji jest po prostu 
zwracana spowrotem. Funkcja w tym pliku jest używana podczas tworzenia 
wykresów, oraz przeprowadzania testów statystycznych.

#### reading_urls.py
Plik ten odpowiada za wczytywanie adresów url z pliku `.txt`. Dzieje
się tak gdyż strona `flashscore` z której zbierałem wyniki często ma
problemy jeśli chodzi o połączenie z nią poprzez iterowanie kolejnych
bloków z archiwum wyników, więc zdecydowałem się na taki zabieg.

#### save_to_csv.py
Ostatni plik i odpowiada on za zapis do postaci `.csv` zebranych wartości
podczas operacji zbierania danych. Najpierw sprawdzane jest czy ścieżka 
istnieje, jeśli tak to dopisywane są wartości. Jeśli nie istnieje tworzony
jest plik.

### Folder `Data`
#### get_values_current_season.py
Plik ten odpowiada za zbieranie wartości z aktualnego sezonu Premier League.
Został wyodrębniony a nie jak reszta sezonów w jednym pliku, gdyż się jeszcze nie
skończył i potrzebne jest inne operowanie np. przewijaniem strony. Jeśli
chodzi o strukturę posiada funkcję:
- do klikania przycisku akceptowania ciasteczek,
- przycisk do ładowania większej ilości meczy,
- operację przewijania strony w dół i powrót na górę, która ładuje
wszystkie elementy,
- zbierającą dane ze strony poprzez przejście w statystyki danego spotkania i
pobraniu wszystkich dostępnych statystyk jakie oferuje strona, na koniec dodawane
są wartości i zapisywane do pliku,
- sprawdzającą sezon z którego zbierane są aktualnie dane
- główną, która wyzwala całą resztę iterując po ilości meczy w danym sezonie
- przewijania strony w dół o zadany parametr jako wartość wejściową.

#### get_values_past_seasons.py
Plik praktycznie identyczny do tego pierwszego z tą różnicą, że posiada inne
wartości scrollowania w dół, ponieważ są to sezony zakończone i mają kompletną
ilość rozegranych meczów.

### `Main file`
#### main.py
Plik główny, w którym są wywołane wszystkie funkcje. Zostały utworzone dwie funkcje
`main1()` oraz `main2()` aby można było włączyć np. samą analizę danych. `main1()` zbiera
dane najpierw z aktualnego sezonu potem z poprzednich w pętli za pomocą wczytanych `url`
z pliku tekstowego. Niestety strona używana przeze mnie strona `flashscore` często ma problemy
z widocznością niektórych elementów mimo, że są więc samo zbieranie danych zajęło bardzo długo,
dlatego też wpadłem na pomysł podzielenia pliku głównego na dwie funkcje. Funkcja
`main2()` przeprowadza operacje na zebranych już danych, które również są
załączone w repozytorium.


## Przykładowe wyniki i ich rozumienie dla zespołu Arsenal
`Podstawowe statystyki:`  
Mean goals expected:  1.9353521126760562  
Minimum goals expected:  0.52  
Maximum goals expected:  4.11  
Mean shots on goal:  5.141643059490085  
Minimum shots on goal:  0  
Maximum shots on goal:  16  
`Tabela krzyżowa pokazująca jak dla poszczególnych wartości 
strzelonych bramek wyglądał dla drużyny wynik meczu.`  
| xG_Category       | Defeat | Draw | Win |  
|-------------------|--------|------|-----|  
| <0.5              | 71     | 58   | 153 |  
| 0.5-1.0           | 5      | 5    | 5   |  
| 1.0-1.5           | 2      | 3    | 10  |  
| 1.5-2.0           | 3      | 5    | 4   |  
| >2.0              | 1      | 2    | 26  |  
`Tabela krzyżowa pokazująca jak dla poszczególnych wartości 
strzelonych bramek wyglądał dla drużyny wynik meczu`    
| Goals scored | Defeat | Draw | Win |  
|--------------|--------|------|-----|  
| 0            | 41     | 18   | 0   |  
| 1            | 35     | 30   | 30  |  
| 2            | 5      | 19   | 71  |  
| 3            | 1      | 6    | 51  |  
| 4            | 0      | 0    | 27  |  
| 5            | 0      | 0    | 17  |  
| 6            | 0      | 0    | 2   |   
`Wynik zwrócony przez model regresji logistycznej`:  
| Class        | Precision | Recall | F1-Score | Support |  
|-------------|-----------|--------|----------|---------|  
| 0           | 0.67      | 0.69   | 0.68     | 29      |  
| 1           | 0.78      | 0.76   | 0.77     | 42      |  
| **Accuracy**   |           |        | **0.73**  | 71      |  
| **Macro Avg**  | 0.72      | 0.73   | 0.72     | 71      |  
| **Weighted Avg** | 0.73  | 0.73   | 0.73     | 71      |  
Rozumienie tego wyniku:  
Model miał za zadanie przewidzieć wynik meczu gdzie:
- 0 to przegrana
- 1 to wygrana


`Precyzja` model przewidział że rzeczywiście 67% z meczów, które
przewidział jako przegrane były rzeczywiście przegranymi, natomiast
78% z przewidzianych zwycięstw było poprawnych. Wnioskiem jest za tem
to, że model lepiej przewiduje wygrane niż przegrane mecze.  
`Czułość` czyli ile rzeczywistych wygranych.przegranych model poprawnie
wykrył. Dla klasy 0 (czyli przegrane) model poprawnie oznaczył 69% wszystkich
rzeczywistych przegranych. Natomiast dla klasy 1 (czyli wygrane) wykrył 76% 
rzeczywistych wszystkich wygranych.  
`F1-score` jest to średnia harmoniczna precyzji i czułości. Dla klasy 0 wynosi
68% natomiast dla klasy 1 77%.  
`Support` definicja próbek w każdej klasie, czyli 29 przegranych oraz 42 wygrane
w testowym zbiorze. Dane w miarę zbalansowane jednak więcej jest wygranych.  
Jeśli chodzi o ogólną skuteczność modelu: `Accuracy` wyniosło 73%.  
Wnioski: Model osiągną 73% dokładności - jest w miarę dobry ale nie idealny.
Przewiduje lepiej wygrane niż przegrane. Można go poprawić dodając większą liczbę.
Aktualnie do modelu przekazywana jest statystyka 'Expected Goals', która według
mnie ma kluczowy wpływ na wygrane lub przegrane mecze jednak tak jak już wspominałem
wcześniej jej dostępność jest ograniczona.