class GiosDataManager:
    """
    Downloads and manage GIOS data for different years and information types
    \n**years**: which years from GIOS should be considered
    \n**informations**: which measurements should be taken, available are: #TODO list them. 
    """
    def __init__(self, years: list, informations :list):
        self.years = years
        self.informations = informations

        self._metadata = None
        self._data = None

        self._load_and_clean()

    def _load_and_clean(self):
        "Loads, cleans data, and save them in metadata and database"
        self._load_data()
        self._clean_data()

    def _load_data(self) -> None:
        """
        Downloads data from server given the years and format
        """
        #TODO - przerobić tą funkcje co oni podali, oraz pobrać metadane, 
        # TODO - ostatecznie ładujemy wszystko do _data
        # wazne żeby tutaj sprawdzić, ilość wierszy po pobraniu, (zaraz po) i po zakończeniu i sprawdzić czy się to różni) 
        self._data = ...
        self._metadata = ...
    
    def _clean_data(self) -> None:
        """
        Cleans data, merge names with newest tags 
        """
        #TODO - ta metoda będzie wywoływana
        self._data = ... 

    def save_local(self, path) -> None:
        """
        Saves loaded data locally
        """
        #TODO - zrobić funkcje która zapisuje metadane oraz dataset, w podanej ścieżce w nastepujący sposób: path/metadata + path/database
 
    def df(self) -> pd.DataFrame:
        return self._data.copy()
    

    #TODO - przepisać funkcje od zarządzania formatami 
    #TODO - wszystkie te funkcje które odpowiadają, za niektóre analizy, (jak heatmapy itd.)

