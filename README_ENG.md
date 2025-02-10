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
Data from: https://www.flashscore.com/
## Start the program
To start the program, you need to enable the main file, which by default is
set to start the `main2()` function, which is the one responsible for
analyzing the collected data. To start collecting data, change the
in line 39 in the `main.py` file `main2()` to `main1()`. To use the
`streamlit` you need to run the command in the project's root directory:    
`streamlit run AnalyzeData/dashboard.py` it is also given in the file.
`main.py` on line 35.After executing this command, it should open the
dashboard browser.
## Files
### Folder `AnalyzeData`
#### creating_graphs.py
This file allows you to create charts. Using pandas, a
`.csv` file is loaded, after which columns such as:
``Opponent``, ``Result`` and ``Season`` since they are not
numeric. Then the basic statistics are printed out, and the generated
are:
- Correlation matrix,
- Trends for the statistics ``Expected goals``, ``Ball possession`` and
for goals scored
- A cross table is displayed
- Visualization of the table as a bar chart and visualization of the number of matches
- with different opponents

#### dashboard.py
This file is responsible for showing dashboards using the library
`streamlit`. In the file there is a function that manages the data
input, handling what is loaded using `pandas`.
Then the `exceptional` columns are handled. After that, the
charts are created for all the described sections that are described
in this file, and in the generated dashboard by `streamlit`.

#### modeling.py
This file is responsible for creating a logistic regression model for classification.
classification. The data is loaded and pre-cleaned, after which the
features `x` and labels `y` are created, where `x` contains match features
such as expected goals or ball possession. The `y`, on the other hand, is the label of the
of the match result where 1 is a win and 0 is a loss. Next, a
is divided into a training and test set on an 80/20 scale (80 - for training,
20 - for the test). Then a `logistic regression` model is created and it is
taught. At the very end, the model makes predictions and a
report for evaluation.

#### tests.py
This file is responsible for performing 2 statistical tests viz.
in this case the `chi-square test` and the `correlation test`. The chi-square test
tests whether there is a relationship between ball possession and the outcome of the
match, and checks whether there is a relationship between expected goals
and the outcome of the match, if the results are less than `0.05` it means that a
there is a relationship between the variables. The correlation test checks whether there is a
relationship between expected goals and goals scored. Also
as in the case of `chi-quadrat` if the results are less than `0.05` it
there is a relationship between the variables. To conduct the tests
scipy library was used.

### Folder `ClearData`
#### add_data.py
This file adds additional columns to the csv file during the operation of the 
data collection. The function receives the values collected during data collection
data and performs assignment operations on them to new rows. At
finally returns the result, which is further used in the data collection operation.
data.

#### convert_data.py
This file performs data conversions such as: `%`, `(312/346)`, and
removes unnecessary spaces . If the value does not require conversion it is simply 
returned back. The function in this file is used when creating 
graphs, and performing statistical tests.

#### reading_urls.py
This file is responsible for loading the url from the `.txt` file. It happens
This is because the `flashscore` page from which I collected results often has
problems when it comes to connecting to it by iterating successive
blocks from the results archive, so I decided to do it this way.

#### save_to_csv.py
The last file and it is responsible for saving to `.csv` form the collected values
during the data collection operation. First it is checked whether the path 
exists, if it does then the values are added. If it does not exist a
file is created.

### Folder `Data`
#### get_values_current_season.py
This file is responsible for collecting values from the current Premier League season.
It has been extracted and not like the rest of the seasons in one file, because it has not yet
finished and a different operation is needed, such as scrolling the page. If
terms of structure it has a function:
- for clicking the button to accept cookies,
- button to load more matches,
- operation to scroll down the page and back to the top, which loads
all elements,
- collecting data from the page by going to the statistics of a particular match and
downloading all the available statistics the site offers, finally adding the
values are added and saved to a file,
- checking the season from which the data is currently being collected
- the main one, which triggers all the rest by iterating over the number of matches in a given season
- scrolling the page down by a set parameter as an input value.

#### get_values_past_seasons.py
A file virtually identical to the first one except that it has different
scroll down values, since these are completed seasons and have a complete
number of matches played.

### `Main file`
#### main.py
The main file, in which all functions are called. Two functions have been created
`main1()` and `main2()` so that the data analysis itself can be included, for example. `main1()` collects
data first from the current season then from previous seasons in a loop using loaded `url`.
from a text file. Unfortunately, the site I use `flashscore` often has problems
with the visibility of some elements even though they are there so just collecting the data took a very long time,
therefore I came up with the idea of splitting the main file into two functions. Function
`main2()` performs operations on already collected data, which are also
included in the repository.

## Example results and their understanding for the Arsenal team
`Basic statistics:`.  
Mean goals expected: 1.9353521126760562  
Minimum goals expected: 0.52  
Maximum goals expected:  4.11  
Mean shots on goal: 5.141643059490085  
Minimum shots on goal: 0  
Maximum shots on goal: 16  
A `cross table showing how for each value of 
goals scored looked like for the team the result of the match.`. 
| xG_Category       | Defeat | Draw | Win |  
|-------------------|--------|------|-----|  
| <0.5              | 71     | 58   | 153 |  
| 0.5-1.0           | 5      | 5    | 5   |  
| 1.0-1.5           | 2      | 3    | 10  |  
| 1.5-2.0           | 3      | 5    | 4   |  
| >2.0              | 1      | 2    | 26  |  
A `cross table showing how for each value of 
goals scored looked like for the team the result of the match`.   
| Goals scored | Defeat | Draw | Win |  
|--------------|--------|------|-----|  
| 0            | 41     | 18   | 0   |  
| 1            | 35     | 30   | 30  |  
| 2            | 5      | 19   | 71  |  
| 3            | 1      | 6    | 51  |  
| 4            | 0      | 0    | 27  |  
| 5            | 0      | 0    | 17  |  
| 6            | 0      | 0    | 2   | 
The `result returned by the logistic regression model`:
| Class        | Precision | Recall | F1-Score | Support |  
|-------------|-----------|--------|----------|---------|  
| 0           | 0.67      | 0.69   | 0.68     | 29      |  
| 1           | 0.78      | 0.76   | 0.77     | 42      |  
| **Accuracy**   |           |        | **0.73**  | 71      |  
| **Macro Avg**  | 0.72      | 0.73   | 0.72     | 71      |  
| **Weighted Avg** | 0.73  | 0.73   | 0.73     | 71      |  

Understanding of the outcome:  
The model was tasked with predicting the outcome of a match where:
- 0 is a loss
- 1 is a win

The `precision' model predicted that indeed 67% of the matches it
it predicted as losses were actually losses, while
78% of the predicted wins were correct. The inference
that the model is better at predicting winning matches than losing matches.  
The `sensitivity' means how many actual wins.losses the model correctly
detected. For class 0 (i.e., losers), the model correctly labeled 69% of all
actual losers. In contrast, for class 1 (i.e., wins) it detected 76% of the 
of the actual total wins.  
The `F1-score` is the harmonic mean of precision and sensitivity. For class 0, it is
68% while for class 1 it is 77%.  
The `Support` definition of the samples in each class, that is, 29 losers and 42 wins
in the test set. The data reasonably balanced however there are more wins.  
As for the overall performance of the model: `Accuracy` was 73%.  
Conclusions: The model will achieve 73% accuracy - it is reasonably good but not perfect.
It predicts wins better than losses. It can be improved by adding more numbers.
Currently, the 'Expected Goals' statistic is passed to the model, which I think
in my opinion has a key impact on matches won or lost, however, as I mentioned earlier
earlier its availability is limited.