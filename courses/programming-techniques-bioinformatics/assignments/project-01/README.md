# Project overview
Project 3 focuses on the analysis of PM2.5 air pollution data collected from measurement stations in Poland.
The project is implemented in a *function-oriented design*, where all data loading, preprocessing, analysis, and visualization logic is encapsulated in reusable Python functions located in `scripts`. The notebook `projekt_3_student.ipynb` serves as the execution and presentation layer.

Main objectives: 
- Load and clean air quality measurement data
- Calculate monthly averages of PM2.5 concentrations
- Visualize trends using heatmaps
- Identify days on which PM2.5 concentration exceeded the accepted norm



# Structure
## Files
```bash
├── PM25_combined_2014_2019_2024.csv        
├── projekt_3_student.ipynb                 solution of (1-6) project, 
├── README.md                               
├── requirements.txt                        file with used libraries
└── scripts                                 
    ├── analyse_data.py                     functions responsible for data manipulation and plots
    └── load_data.py                        functions responsible for downloading and cleaning data
```
## Data
### Station code
Measurement stations are identified using a standardized station code format:
```bash
WwPp\*Nn\*
```
Where
- Ww – voivodeship (region) code
- Pp – county (powiat) code
- Nn – station name
- x = [:lower:]
- X = [:upper:]
## Notebook Workflow (projekt_3_student.ipynb)
The notebook follows a structured execution flow:
1. Import required libraries
2. Import functions from load_data.py and analyse_data.py
3. Load and clean the dataset
4. Perform monthly average calculations
5. Generate heatmaps
6. Identify days exceeding PM2.5 norms
7. Present results using tables and plots



co zmieniłem
- dodałem file_name przy zapisie / oraz jeden chunk do ładowania ich, żeby nie musieć wszystkiego uruchamiać




