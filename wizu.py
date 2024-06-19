import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Helper function to convert string values to float
def convert_to_float(column):
    return column.str.replace(',', '.').astype(float)

# Wczytywanie danych z pliku CSV
filename = 'RYNED.csv'
df = pd.read_csv(filename, sep=';', header=0)

df.columns = df.columns.str.strip()

# Zmiana etykiet kolumn
new_column_names = {
    'ogółem;2004;[%]': 'Rok 2004',
    'ogółem;2005;[%]': 'Rok 2005',
    'ogółem;2006;[%]': 'Rok 2006',
    'ogółem;2007;[%]': 'Rok 2007',
    'ogółem;2008;[%]': 'Rok 2008',
    'ogółem;2009;[%]': 'Rok 2009',
    'ogółem;2010;[%]': 'Rok 2010',
    'ogółem;2011;[%]': 'Rok 2011',
    'ogółem;2012;[%]': 'Rok 2012',
    'ogółem;2013;[%]': 'Rok 2013',
    'ogółem;2014;[%]': 'Rok 2014',
    'ogółem;2015;[%]': 'Rok 2015',
    'ogółem;2016;[%]': 'Rok 2016',
    'ogółem;2017;[%]': 'Rok 2017',
    'ogółem;2018;[%]': 'Rok 2018',
    'ogółem;2019;[%]': 'Rok 2019',
    'ogółem;2020;[%]': 'Rok 2020',
    'ogółem;2021;[%]': 'Rok 2021',
    'ogółem;2022;[%]': 'Rok 2022',
    'ogółem;2023;[%]': 'Rok 2023',
    'Nazwa': 'Województwo'
}

# Zastosowanie zmiany etykiet kolumn
df.rename(columns=new_column_names, inplace=True)

# 1. Wizualizacja obejmująca wszystkie województwa w wybranym okresie lat
def plot_all_provinces(df, start_year, end_year):
    years = list(range(start_year, end_year + 1))
    df_period = df[['Województwo'] + [f'Rok {year}' for year in years]].copy()

    # Konwersja wartości na liczby zmiennoprzecinkowe
    for year in years:
        column = f'Rok {year}'
        df_period[column] = convert_to_float(df_period[column])
    
    plt.figure(figsize=(14, 7))
    
    # Wyodrębnienie danych dla Polski
    df_polska = df_period[df_period['Województwo'].str.upper() == 'POLSKA']
    df_wojewodztwa = df_period[df_period['Województwo'].str.upper() != 'POLSKA']
    
    # Rysowanie linii dla województw
    for index, row in df_wojewodztwa.iterrows():
        plt.plot(years, row[1:], label=row['Województwo'])
    
    # Rysowanie wyróżnionej linii dla Polski
    if not df_polska.empty:
        row_polska = df_polska.iloc[0]
        plt.plot(years, row_polska[1:], label='POLSKA', linewidth=3, linestyle='--', color='black')
    
    plt.xlabel('Rok')
    plt.ylabel('Stopa bezrobocia (%)')
    plt.title(f'Stopa bezrobocia w Polsce w latach {start_year}-{end_year}')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))
    plt.xticks(years)  # Wyświetlanie wszystkich lat na osi X

    plt.tight_layout()
    plt.show()

# 2. Wizualizacja dla wybranych trzech województw
def plot_selected_provinces(df, provinces, start_year, end_year):
    years = [f'Rok {year}' for year in range(start_year, end_year + 1)]
    df_filtered = df[df['Województwo'].str.strip().str.upper().isin([prov.upper() for prov in provinces])].copy()

    # Konwersja wartości na liczby zmiennoprzecinkowe
    for year in years:
        df_filtered[year] = convert_to_float(df_filtered[year])
    
    if not df_filtered.empty:
        plt.figure(figsize=(14, 7))
        for index, row in df_filtered.iterrows():
            plt.plot(range(start_year, end_year + 1), row[years], label=row['Województwo'])
        plt.xlabel('Rok')
        plt.ylabel('Stopa bezrobocia (%)')
        plt.title(f'Stopa bezrobocia w wybranych województwach w latach {start_year}-{end_year}')
        plt.legend()

        ax = plt.gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))
        plt.xticks(range(start_year, end_year + 1))  # Ustawianie pełnych lat na osi X

        plt.tight_layout()
        plt.show()
    else:
        print(f"Brak danych dla województw: {provinces}")

# Funkcja do rysowania wykresu kołowego dla wybranych trzech województw w roku 2020
def plot_pie_chart(df, provinces, year):
    # Create the column name for the specified year
    year_column = f'Rok {year}'
    
    # Filter data for the selected year and provinces, excluding "POLSKA"
    df_filtered = df[(df['Województwo'] != 'POLSKA') & df['Województwo'].str.upper().isin([prov.upper() for prov in provinces])].copy()
    df_filtered = df_filtered[['Województwo', year_column]]
    
    # Drop rows with missing data
    df_filtered.dropna(subset=[year_column], inplace=True)
    
    # Konwersja wartości na liczby zmiennoprzecinkowe
    df_filtered[year_column] = convert_to_float(df_filtered[year_column])
    
    # Sort values in descending order by unemployment rate in the selected year
    df_filtered.sort_values(by=year_column, ascending=False, inplace=True)
    
    # Get the top three provinces and sum the rest
    top_provinces = df_filtered.head(3)
    other_sum = df_filtered.iloc[3:][year_column].sum() if len(df_filtered) > 3 else 0.0
    
    # Prepare data for the pie chart
    pie_data = list(top_provinces[year_column]) + [other_sum]
    labels = list(top_provinces['Województwo']) + ['Inne']
    colors = plt.cm.Set3.colors[:len(pie_data)]
    
    # Plot the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(pie_data, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title(f'Udział bezrobocia w wybranych województwach (bez POLSKI) w roku {year}')
    plt.axis('equal')
    plt.show()

start_year = 2004
end_year = 2023
year = 2020
provinces = ['ŚLĄSKIE', 'MAZOWIECKIE', 'MAŁOPOLSKIE']

plot_all_provinces(df, start_year, end_year)
plot_selected_provinces(df, provinces, start_year, end_year)
plot_pie_chart(df, provinces, year)

