import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from library.intake_locations import create_files

create_files()

intake_data = pd.read_csv('team_intake_prev.csv')
intake_data_filtered = pd.read_csv('team_intake.csv')

sample_size = 20

intake_data = intake_data.sample(sample_size)
intake_data_filtered = intake_data_filtered.sample(sample_size)

sns.set_theme(style='whitegrid')

sns.barplot(x="source", y="team", data=intake_data_filtered,
            label="source", color="r", orient='h')

sns.barplot(x="speaker", y="team", data=intake_data_filtered,
            label="speaker", color="b", orient='h')

sns.barplot(x="center", y="team", data=intake_data_filtered,
            label="center", color="g", orient='h')

sns.barplot(x="amp", y="team", data=intake_data_filtered,
            label="amp", color="m", orient='h')

sns.barplot(x="trap", y="team", data=intake_data_filtered,
            label="trap", color="y", orient='h')

plt.show()