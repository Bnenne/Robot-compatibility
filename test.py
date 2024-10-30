import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('finalized_combined.csv', nrows=20)

red1 = data[['red1', 'red1_epa_pre_champs']]
red1.rename(columns={'red1': 'teams', 'red1_epa_pre_champs': 'epa'}, inplace=True)

red2 = data[['red2', 'red2_epa_pre_champs']]
red2.rename(columns={'red2': 'teams', 'red2_epa_pre_champs': 'epa'}, inplace=True)

red3 = data[['red3', 'red3_epa_pre_champs']]
red3.rename(columns={'red3': 'teams', 'red3_epa_pre_champs': 'epa'}, inplace=True)

blue1 = data[['blue1', 'blue1_epa_pre_champs']]
blue1.rename(columns={'blue1': 'teams', 'blue1_epa_pre_champs': 'epa'}, inplace=True)

blue2 = data[['blue2', 'blue2_epa_pre_champs']]
blue2.rename(columns={'blue2': 'teams', 'blue2_epa_pre_champs': 'epa'}, inplace=True)

blue3 = data[['blue3', 'blue3_epa_pre_champs']]
blue3.rename(columns={'blue3': 'teams', 'blue3_epa_pre_champs': 'epa'}, inplace=True)

teams = pd.concat([red1, red2, red3, blue1, blue2, blue3]).drop_duplicates()

sns.set_theme(style='whitegrid')

sns.barplot(x="epa", y="teams", data=teams, order=teams.sort_values('epa', ascending=False).teams,
            label="EPA before Champs", color="b", orient='h')

plt.show()