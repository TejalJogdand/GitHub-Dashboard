import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile

github_data = pd.read_csv('E:/python_apps/streamlit_app/csv_files/github_dataset.csv')

with zipfile.ZipFile('E:/python_apps/streamlit_app/csv_files/repository_data.zip', 'r') as z:
    with z.open('repository_data.csv') as f:
        repository_data = pd.read_csv(f)

merged_data = pd.merge(github_data, repository_data, on='stars_count', how='inner')

st.title("GitHub Projects Dashboard")

st.write("Columns in Merged Data:")
st.write(merged_data.columns.tolist())

st.subheader("GitHub Dataset Overview")
st.write(github_data.head())
st.write(github_data.describe())

st.subheader("Repository Dataset Overview")
st.write(repository_data.head())
st.write(repository_data.describe())

st.subheader("Repository count by Language")
language_counts = merged_data['language'].value_counts()
plt.figure(figsize=(10, 5))
language_counts.plot(kind='bar')
plt.title('Count of Repositories by Language')
plt.xlabel('Language')
plt.ylabel('Count')
st.pyplot(plt)

st.write("Python, JavaScript, PHP and Java are the most common languages in the dataset, with python having the highest number of repositories.")

st.subheader("Filter Repositories by Stars")
min_stars = st.slider("Minimum Stars", 0, int(merged_data['watchers'].max()), 0)
filtered_data = merged_data[merged_data['watchers'] >= min_stars]
st.write(filtered_data.head(5))
st.write(filtered_data.describe())

st.subheader("Distribution of Stars in GitHub projects")
plt.figure(figsize=(10, 5))
sns.histplot(merged_data['stars_count'], bins=30, kde=True)
plt.title('Distribution of Stars in GitHub Projects')
plt.xlabel('Stars')
plt.ylabel('Count')
st.pyplot(plt)

st.subheader("Correlation Heatmap")
plt.figure(figsize=(10, 5))
corr = merged_data[['stars_count', 'watchers', 'forks_count_x', 'forks_count_y']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation between GitHub Project Metrics')
st.pyplot(plt)

st.subheader("Top Starred Repositories")
top_starred_repos = merged_data.sort_values(by='stars_count', ascending=False).head(10)
st.write(top_starred_repos[['repositories', 'name', 'language', 'stars_count', 'watchers']])