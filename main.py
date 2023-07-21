# Annual Stackoverflow Devloper Survey 2022
# Guiding question:
# 1. What is the demographic distribution of the survey respondents?
# 2. What are the most used programming languages among developers?
# 3. What are the most common job titles and roles among the respondents?
# 4. What are the most desired languages by developer? 
# 5. What is the salary trends among the developers based on their experience? 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(r"C:\Users\simcy\OneDrive\Desktop\new_stackoverflow_2022\stack-overflow-developer-survey-2022\survey_results_public.csv")

country_name = {
    "Iran, Islamic Republic of..." : "Iran",
    "Congo, Republic of the..." : "Congo",
    "CÃ´te d'Ivoire" : "Ivory Coast", 
    "Venezuela, Bolivarian Republic of..." : "Venezuela",
    "Lao People's Democratic Republic" : "Laos",
    "United Kingdom of Great Britain and Northern Ireland" : "United Kingdom",
    "The former Yugoslav Republic of Macedonia" : "North Macedonia",
    "United States of America" : "America",
    "Republic of Moldova" : "Moldova",
    "Republic of Korea" : "South Korea"
}

new_branch = {
    "I am a developer by profession": "Profession Developer",
    "I am learning to code": "Learn to code",
    "I am not primarily a developer, but I write code sometimes as part of my work": "Citizen Developer",
    "I code primarily as a hobby": "Code for Hobby",
    "I used to be a developer by profession, but no longer am": "Ex-developer"
}

#--------------------------- Q1 -------------------------------------#
q1_columns = ["MainBranch", "Employment", "Gender", "Age", "EdLevel", "YearsCode", "Country"]
data_q1 = (df[q1_columns])
data_q1["Country"].replace(country_name, inplace=True)
data_q1["MainBranch"].replace(new_branch, inplace=True)
data_q1["EdLevel"].replace("Something else", "Other")
data_q1["Employment"] = data_q1["Employment"].str.split(";", expand=True)[0]
data_q1["Gender"] = data_q1["Gender"].str.replace(":", "").str.split(";", expand=True)[0]
cleaned_q1 = data_q1.dropna().drop_duplicates()

# Top 10 country with high respondents 
top_countries = cleaned_q1["Country"].value_counts().head(10).sort_values(ascending=False)
plt.bar(top_countries.index, top_countries.values)
plt.xlabel("Country")
plt.ylabel("Totol Respondents")
plt.title("Top 10 Countries with Highest Respondents")
plt.show()

# Respondent Gender Distribution
gender_counts = cleaned_q1["Gender"].value_counts()
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%')
plt.title("Respondent Gender Distribution")
plt.show()

# Profession grouped by Age
profession_by_age = cleaned_q1.groupby(["Age", "MainBranch"]).size().unstack()
profession_by_age.plot(kind="barh", stacked=True, figsize=(12, 8))
plt.ylabel("Age")
plt.title("Professions Grouped by Age")
plt.legend(title="Profession", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.gca().invert_yaxis() 
plt.show()

#--------------------------- Q2 -------------------------------------#
q2_columns = ["LanguageHaveWorkedWith", "LanguageWantToWorkWith"]
data_q2 = (df[q2_columns])
data_q2.rename(columns={"LanguageHaveWorkedWith": "MostUsedLangauges", "LanguageWantToWorkWith": "PreferredLanguage"}, inplace=True)
clean_q2 = data_q2.drop_duplicates().dropna()

# Most Used Langauges
clean_q2["MostUsedLangauges"] = clean_q2["MostUsedLangauges"].str.split(";")
most_used_langauges = clean_q2.explode("MostUsedLangauges")["MostUsedLangauges"].value_counts()

# Preferred Languages 
clean_q2["PreferredLanguage"] = clean_q2["PreferredLanguage"].str.split(";")
preferred_languages = clean_q2.explode("PreferredLanguage")["PreferredLanguage"].value_counts()

# Most Used Langauges Vs Preferred Languages
plt.figure(figsize=(10, 6))
plt.barh(most_used_langauges.index, most_used_langauges.values, label="Most Used Languages")
plt.barh(preferred_languages.index, preferred_languages.values, label="Preferred Languages")
plt.title("Most Used Languages Vs Preferred Languages")
plt.legend()
plt.gca().invert_yaxis()
plt.show()

#--------------------------- Q3 -------------------------------------#
q3_columns = ["DevType"]
data_q3 = (df[q3_columns])
data_q3 = data_q3["DevType"].str.get_dummies(sep=";")
cleaned_q3 = data_q3.drop_duplicates().dropna()

# Top 10 Developer Distribution
role_counts = cleaned_q3.sum().sort_values(ascending=False).head(10)
plt.barh(role_counts.index, role_counts.values)
plt.ylabel("Roles")
plt.gca().invert_yaxis() 
plt.show()

#--------------------------- Q4 -------------------------------------#
q4_columns = ["LanguageWantToWorkWith", "DatabaseWantToWorkWith", "WebframeWantToWorkWith", "MiscTechWantToWorkWith"]
data_q4 = (df[q4_columns])
for column in q4_columns:
    data_q4[column] = data_q4[column].str.split(";")

tech_counts = pd.Series(dtype=int)
for column in q4_columns:
    tech_counts = tech_counts.add(data_q4[column].explode().value_counts(), fill_value=0)

# Top 10 Popular Languages 
top_n = 10
top_tech = tech_counts.sort_values(ascending=False).astype(int).head(10)
plt.figure(figsize=(10,6))
plt.bar(top_tech.index, top_tech.values)
plt.xlabel("Programming Languages")
plt.title("Top 10 Popular Languages")
plt.xticks(rotation=45)
plt.show()

#--------------------------- Q5 -------------------------------------#
q5_columns = ["YearsCode", "Currency", "DevType", "CompTotal", "CompFreq", "ConvertedCompYearly"]
data_q5 = df[q5_columns]
data_q5["Currency"] = data_q5["Currency"].str.split("\t").str[0]
data_q5["DevType"] = data_q5["DevType"].str.split(";").str[0]

def converted_comp(row):
    if row["Currency"] != "USD" and row["CompFreq"] != "Yearly":
        return row["ConvertedCompYearly"]
    return row["CompTotal"]    
data_q5["CompYearlyUSD"] = data_q5.apply(converted_comp, axis=1)
cleaned_q5  = data_q5[["YearsCode", "DevType", "CompYearlyUSD"]].drop_duplicates().dropna()

# Salary and experience by developer type
def convert_int(exp):
    if exp == "More than 50 years":
        return 51
    elif exp == "Less than 1 year":
        return 0
    else:
        return(int(exp))
cleaned_q5["YearsCode"] = cleaned_q5["YearsCode"].apply(convert_int)  
cleaned_q5 = cleaned_q5[cleaned_q5["DevType"] != "Student"] 
average_exp = cleaned_q5.groupby("DevType")["YearsCode"].mean().round(1).reset_index()
median_comp = cleaned_q5.groupby("DevType")["CompYearlyUSD"].median().reset_index()
avg_exp_med_comp = pd.merge(average_exp, median_comp, on="DevType")

y = avg_exp_med_comp["YearsCode"]
x = avg_exp_med_comp["CompYearlyUSD"]
develepor_role = avg_exp_med_comp["DevType"]
plt.figure(figsize=(10,6))
plt.scatter(x, y, alpha=0.5)
for i, develepor_role in enumerate(develepor_role):
    plt.text(x[i], y[i], develepor_role, fontsize=7, ha="center", va="bottom", alpha=0.7)

plt.ylabel("Average Experience")
plt.xlabel("Annual Median Salary USD")
plt.title("Average Experience Vs Salary with Developer Roles")
plt.grid(True)
plt.show()