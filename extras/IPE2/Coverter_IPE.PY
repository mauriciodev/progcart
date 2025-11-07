import geopandas as gpd
import pandas as pd

# Load the polygon layer (GeoJSON of Brazilian states)
gdf_states = gpd.read_file("br_states.json")

# Load the CSV data
df_alunos = pd.read_csv("origem_alunos.csv")

# Preview the column names to confirm the key column
print(gdf_states.columns)
print(df_alunos.columns)

# OPTIONAL: Clean state names to ensure consistency (strip whitespace, etc.)
gdf_states["Estado"] = gdf_states["Estado"].str.strip()
df_alunos["Estado"] = df_alunos["Estado"].str.strip()


# Step 1: Count occurrences of each state in df_alunos
state_counts = df_alunos["Estado"].value_counts().reset_index()
state_counts.columns = ["Estado", "aluno_count"]

# Step 2: Merge the counts into gdf_states
gdf_states = gdf_states.merge(state_counts, on="Estado", how="left")

# Step 3: Fill NaN with 0 for states with no matches
gdf_states["aluno_count"] = gdf_states["aluno_count"].fillna(0).astype(int)

# Done: gdf_states now includes a new column 'aluno_count'
print(gdf_states[["Estado", "aluno_count"]])

# Save or plot the result (optional)
#gdf_states.to_file("br_states_with_alunos.geojson", driver="GeoJSON")

gdf_states[['Alunos','População']] = gdf_states[["aluno_count",'Total']]

# 3. Group by 'estados' and 'year' and count rows
df_counts = (
    df_alunos
    .groupby(["Estado", "Ano"])
    .size()
    .reset_index(name="count")
)

df_pivot = df_counts.pivot(index="Estado", columns="Ano", values="count").fillna(0).reset_index()

# Optional: rename columns to make them clearer
df_pivot.columns.name = None  # remove the multi-index name
df_pivot = df_pivot.rename(columns=lambda x: f"Ano_{x}" if isinstance(x, int) else x)

# 5. Merge with the GeoDataFrame
gdf_joined = gdf_states.merge(df_pivot, on="Estado", how="left").fillna(0)


gdf_joined[["Estado", 'SIGLA', 'População', "Alunos", 'geometry', "Ano_2017", "Ano_2018", "Ano_2019", "Ano_2020", "Ano_2021", "Ano_2022", "Ano_2023"]].to_file("br_states_with_alunos.geojson", driver="GeoJSON")
