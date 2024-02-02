
import pandas as pd
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
from sympy import Interval, oo


#1.A
# načtení souboru
csv_file_path='Data/transfery.csv'
df=pd.read_csv(csv_file_path)

#vynechání prázdných nebo nečíselných hodnot z dat
#konvertuje sloupec 'vek_mother' na numerický typ a zároveň nastaví chybějící hodnoty na 'NaN'

df['clinical_gravidity'] = pd.to_numeric(df['clinical_gravidity'], errors='coerce')
df['vek_mother'] = pd.to_numeric(df['vek_mother'], errors='coerce')

# Odstraňění řádků s hodnotami NaN
df = df.dropna(subset=['clinical_gravidity'])
df = df.dropna(subset=['vek_mother'])

# rozsah hodnot pro věk
age_bins = [0, 29, 34, 39, float('inf')]
age_labels= ['<29', '30-34', '35-39', '40 a více']

# Vytvořte sloupec 'age_category' pro kategorizaci věku matky
df['age_category'] = pd.cut(df['vek_mother'], bins=age_bins, labels=age_labels, include_lowest=True)

# Kontingenční tabulka
contingency_table_age = pd.crosstab(df['age_category'],df['clinical_gravidity'], margins=True, margins_name='Celkem')

# Vytvoření sloupce 'Procentuální_Zastoupeni'
contingency_table_age['Procentuální_Zastoupeni'] = contingency_table_age[1] / contingency_table_age['Celkem'] * 100

# Vytvoření nového DataFrame s vybranými sloupci
result_df = contingency_table_age['Procentuální_Zastoupeni']


# Filtrace řádků, které nejsou 'Celkem'
filtered_contingency_table_age = contingency_table_age[contingency_table_age.index != 'Celkem']
filtered_result_df=filtered_contingency_table_age['Procentuální_Zastoupeni']

# Tisk výsledné  tabulky
print(filtered_result_df)

#vytoření grafu
age_categories=filtered_result_df.index
percentage=filtered_contingency_table_age['Procentuální_Zastoupeni']
plt.figure(figsize=(12, 6))
plt.bar(age_categories,percentage, color='skyblue')
plt.title('Tabulka úspěchu klinické gravidity dle věku matky')
plt.xlabel('věk matky')
plt.ylabel('úspěšnost v %')
plt.savefig('tabulka_A.png')
plt.close()


# 1B Určete zda-li je věk matky statisticky významný na úspěch transferu.
#Chi-kvadrát test
chi2, p, _, _ = chi2_contingency(contingency_table_age)

# Tisk výsledků testu
print(f"Chi-kvadrát hodnota: {chi2}")
print(f"P-hodnota: {p}")

# Vyhodnocení výsledků testu
alpha = 0.05
if p < alpha:
    print("Věk matky je statisticky významně spojen s clinical_gravidity.")
else:
    print("Věk matky není statisticky významně spojen s clinical_gravidity.")


#C)	Taktéž A-B proveďte i pro věk embrya “vek_embryo”. Pokud bylo embryo darované ”f_donor” = 1, takový transfer do statistiky nepočítejte.

#konvertuje sloupec 'vek_embryo' na numerický typ
df['vek_embryo'] = pd.to_numeric(df['vek_embryo'], errors='coerce')

# Odstraňte řádky s chybějícími hodnotami (NaN)
df = df.dropna(subset=['vek_embryo'])

# neuvažujeme hodnoty kde f_donor=1
df=df[df['f_donor']!=1]

# Vytvořte sloupec 'age_category' pro kategorizaci věku embrya
df['age_category'] = pd.cut(df['vek_embryo'], bins=age_bins, labels=age_labels, include_lowest=True)

# Kontingenční tabulka pro počet 'vek_embryo'
contingency_table_embryo = pd.crosstab(df['age_category'],df['clinical_gravidity'], margins=True, margins_name='Celkem')

# Vytvoření sloupce 'Procentuální_Zastoupeni'
contingency_table_embryo['Procentuální_Zastoupeni'] = contingency_table_embryo[1] / contingency_table_embryo['Celkem'] * 100

# Vytvoření nového DataFrame s vybranými sloupci
result_df = contingency_table_embryo['Procentuální_Zastoupeni']

# Filtrace řádků, které nejsou 'Celkem'
filtered_contingency_table_embryo = contingency_table_embryo[contingency_table_embryo.index != 'Celkem']
filtered_result_df=filtered_contingency_table_embryo['Procentuální_Zastoupeni']

# Tisk výsledné  tabulky
print(filtered_result_df)

# Určete zda-li je věk matky statisticky významný na úspěch transferu.
#Chi-kvadrát test
chi2, p, _, _ = chi2_contingency(contingency_table_embryo)

# Tisk výsledků testu
print(f"Chi-kvadrát hodnota: {chi2}")
print(f"P-hodnota: {p}")

# Vyhodnocení výsledků testu
alpha = 0.05
if p < alpha:
    print("Věk embrya je statisticky významně spojen s clinical_gravidity.")
else:
    print("Věk embrya není statisticky významně spojen s clinical_gravidity.")

#D D)	Vytvořte tabulku s počty transferů dle použité genetické metody "genetic_method” viz tabulka.


# Zahrnutí pouze 4  metod a přiřazení 'Other' pro všechny ostatní a pro NaN bez genetické metody
select_method=['PGT-A', 'PGT-SR', 'Karyomapping','OneGene']
df['genetic_method'] = df['genetic_method'].apply(lambda x: x if (x in select_method) else ('bez genetické metody(prázdná hodnota)' if x is None else 'ostatní'))

# Kontingenční tabulka pro metody
contingency_table_method = pd.crosstab(df['genetic_method'], df['clinical_gravidity'])

print(contingency_table_method[1])

# Vytvoření sloupcového grafu pomocí matplotlib
method_labels_plot=contingency_table_method.index
success_counts=contingency_table_method[1]
plt.figure(figsize=(10, 6))
plt.bar(method_labels_plot, success_counts, color='lightcoral')
plt.title('Počet úspěšných transferů dle genetické metody')
plt.xlabel('Genetická Metoda')
plt.ylabel('počty transferů')
plt.savefig('tabulka_D.png')
plt.close()
plt.show()


#E	Určete statistickou významnost pohlaví embrya “sex” – XX/XY na úspěch klinické gravidity dle sloupce “clinical_gravidity”, kde 1 = transfer byl úspěšný a 0 = neúspěšný. Prázdné hodnoty do statistik nepočítejte.
#odstranění hodnot NaN
df = df.dropna(subset=['sex'])
#vytvoření kontingeční tabulky
contingency_table = pd.crosstab(df['sex'], df['clinical_gravidity'])

# Chi-kvadrát test
chi2, p, _, _ = chi2_contingency(contingency_table)

# Tisk výsledků testu
print(f"Chi-kvadrát hodnota: {chi2}")
print(f"P-hodnota: {p}")

# Vyhodnocení výsledků testu
alpha = 0.05
if p < alpha:
    print("Existuje statisticky významný vztah mezi pohlavím embrya a úspěchem klinické gravidity.")
else:
    print("Není dostatek důkazů pro existenci statisticky významného vztahu mezi pohlavím embrya a úspěchem klinické gravidity.")


