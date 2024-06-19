import pandas as pd
import matplotlib.pyplot as plt

# Wczytywanie danych z pliku CSV
filename = 'RYNED.csv'
df = pd.read_csv(filename, sep=';', header=0)

df.columns = df.columns.str.strip()

print(df.columns)

# Upewnijmy się, że dane są poprawnie wczytane
print(df.head())

# Zmiana etykiet kolumn (przykład zmiany kolumny '2004' na 'Rok 2004')
# W dictionary podajesz, które kolumny chcesz zmienić
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
    # Dodaj inne kolumny, które chcesz zmienić
}

# Zastosowanie zmiany etykiet kolumn
df.rename(columns=new_column_names, inplace=True)

# Sprawdzenie, czy zmiany zostały zastosowane
print(df.head())

# 1. Wizualizacja obejmująca wszystkie województwa w wybranym okresie lat
def plot_all_provinces(df, start_year, end_year):
    years = list(range(start_year, end_year + 1))
    df_period = df[['Województwo'] + [f'Rok {year}' for year in years]]
    plt.figure(figsize=(14, 7))
    for index, row in df_period.iterrows():
        plt.plot(years, row[1:], label=row['Województwo'])
    plt.xlabel('Rok')
    plt.ylabel('Stopa bezrobocia (%)')
    plt.title(f'Stopa bezrobocia w Polsce w latach {start_year}-{end_year}')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# 2. Wizualizacja dla wybranych trzech województw
def plot_selected_provinces(df, provinces, start_year, end_year):
    years = [f'Rok {year}' for year in range(start_year, end_year + 1)]
    df_filtered = df[df['Województwo'].str.strip().str.upper().isin([prov.upper() for prov in provinces])]
    print(df_filtered.head())  # Debugowanie - sprawdzenie, co jest filtrowane
    if not df_filtered.empty:
        plt.figure(figsize=(14, 7))
        for index, row in df_filtered.iterrows():
            plt.plot(years, row[years], label=row['Województwo'])
        plt.xlabel('Rok')
        plt.ylabel('Stopa bezrobocia (%)')
        plt.title(f'Stopa bezrobocia w wybranych województwach w latach {start_year}-{end_year}')
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print(f"Brak danych dla województw: {provinces}")

# 3. Kolejna wizualizacja dla tych samych trzech województw, np. histogram
def plot_histogram_selected_provinces(df, provinces, start_year, end_year):
    years = [f'Rok {year}' for year in range(start_year, end_year + 1)]
    plt.figure(figsize=(14, 7))
    for province in provinces:
        df_province = df[df['Województwo'].str.strip().str.upper() == province.upper()]
        print(df_province.head())  # Debugowanie - sprawdzenie, co jest filtrowane
        if not df_province.empty:
            data = df_province[years].iloc[0].str.replace(',', '.').astype(float)
            plt.hist(data, bins=10, alpha=0.5, label=province)
    plt.xlabel('Stopa bezrobocia (%)')
    plt.ylabel('Liczba wystąpień')
    plt.title(f'Histogram stopy bezrobocia w wybranych województwach w latach {start_year}-{end_year}')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Przykładowe wywołanie funkcji
start_year = 2010
end_year = 2023
provinces = ['Mazowieckie', 'Śląskie', 'Wielkopolskie']

plot_all_provinces(df, start_year, end_year)
plot_selected_provinces(df, provinces, start_year, end_year)
plot_histogram_selected_provinces(df, provinces, start_year, end_year)
