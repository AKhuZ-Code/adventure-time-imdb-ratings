# Import requied modules
import pandas as pd

# Read the output dataset
csv_file_path = 'adventuretimedata.csv'
df = pd.read_csv(csv_file_path)

# Remove records where the series name/number starts with Unknown
episode_name_pattern = r'S\d\d?.+'
df = df[df['episode'].str.contains(episode_name_pattern, na=False)]

# Split the season number and the episode number from the title of the episode
pattern = r'S(\d\d?)\.E(\d\d?) ∙ (.+)'
df[['Season', 'Episode', 'Title']] = df['episode'].str.extract(pattern)
df['Season'] = pd.to_numeric(df['Season'], errors='coerce')
df['Episode'] = pd.to_numeric(df['Episode'], errors='coerce')

# Ensure season number is numerical and episode number is numerical (and episode name is a string)
# DONE

### Remove any quotation marks around the description and air date

# Specify columns
columns_to_clean = ['description', 'air date']
# Remove quotation marks from specified columns
for column in columns_to_clean:
    df[column] = df[column].str.strip('"')

### Export to CSV
csv_file_path = 'adventuretimedataclean.csv'
df.to_csv(csv_file_path, index=False)

print(f'DataFrame has been successfully processed and saved to {csv_file_path}')