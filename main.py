from AnalyzeData.tests import Tests
from ClearData.reading_urls import ReadingURLs
from Data.get_values_current_season import GetValuesCurrentSeason
from Data.get_values_past_seasons import GetValuesPastSeasons
from AnalyzeData.creating_graphs import CreatingGraphs
from AnalyzeData.modeling import Modeling


# main1() func is for gathering data, in order to see what are the
# outcome of the collected data change if __name__ == "__main__": main1()
# for if __name__ == "__main__": main2()
# data is collected and stored in the 'Output' folder
def main1():
    # Values updated up to 23 round
    get_values_current_season = GetValuesCurrentSeason()
    get_values_current_season.fetch_all_results()
    # Unlikely past season only has values till season 2013/2014, older seasons doesn't have statistics available
    read_urls = ReadingURLs()
    urls = read_urls.read_urls('urls.txt')
    for url in urls:
        get_values_past_seasons = GetValuesPastSeasons(url)
        get_values_past_seasons.fetch_all_results()


def main2():
    # In order to see other teams statistics just change the name of the .csv
    # file which can be seen in the Output folder
    create_graphs = CreatingGraphs("Output/Arsenal.csv")
    create_graphs.create_graphs()
    modeling = Modeling("Output/Arsenal.csv")
    modeling.modeling()
    tests = Tests("Output/Arsenal.csv")
    tests.test_chi_square()
    tests.correlation_test()
    # To start streamlit dashboard enter: 'streamlit run AnalyzeData/dashboard.py'


if __name__ == "__main__":
    main2()
