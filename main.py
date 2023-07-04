# This data is from stackoverflow annual developer survery from 2022. This is a survey that the user in stackoverflow submit by their own knowledge of coding, 
# years of exprience, and their pay roll.

# Guiding questions:
# 1. Which companies pay the most salaries
# 2. How much does remote work means for employees
# 3. How does coding experience affect the level of pay 
# 4. What is the most popular method learning to code
# 5. Is getting a master's degree to get a job as a developer easily?

import pandas as pd

df = pd.read_csv(r"C:\Users\simcy\OneDrive\Desktop\stackoverflow_analysis\survey_results_public.csv")

# Look for the header 
# df.header = (df.info())

# Filter & clean the data
selected_df = df[["ResponseId", "MainBranch", "Employment", "RemoteWork", "Age", "YearsCode", "YearsCodePro", "EdLevel", "LearnCode", "LearnCodeOnline", "LearnCodeCoursesCert", "LanguageHaveWorkedWith", "LanguageWantToWorkWith", "OrgSize", "Country", "Currency", "CompFreq", "CompTotal"]]
selected_df = selected_df.dropna()
selected_df = selected_df.drop_duplicates(subset="ResponseId")

# 1. Highest yearly compensation in USD sorted by company and country
paid_df = selected_df[["OrgSize", "Currency" , "Country", "CompFreq", "CompTotal"]]
#  Convert the Orgsize cell value to company size 
business_size = {
    "Just me - I am a freelancer, sole proprietor, etc." : "Freelancer",
    "2 to 9 employees" : "Micro Business" ,
    "10 to 19 employees" : "Small Business" ,
    "20 to 99 employees" : "Small-Medium Business" ,
    "100 to 499 employees" : "Medium-Sized Business" ,
    "500 to 999 employees" :  "Large Business",
    "1,000 to 4,999 employees" : "Large Enterprise" ,
    "5,000 to 9,999 employees" : "Major Corporation" ,
    "10,000 or more employees" : "Mega Corporation" 
}

paid_df["OrgSize"] = paid_df["OrgSize"].replace(business_size)
# Format some country name (Optional)
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

paid_df["Country"] = paid_df["Country"].replace(country_name)
#  Extract the currency abbreviation from the "Currency" column
paid_df ["Currency"] = paid_df["Currency"].str.split().str[0]
#  Remove row contains the cell value of "I don't know"
paid_df = paid_df[paid_df["OrgSize"] != "I don’t know"]
#  Find the most paid company by each country in USD
usd_df = paid_df[paid_df["Currency"] == "USD"]
#Convert all usd comp frequency into yearly freq
# frequency = {
#     "Weekly": 52,
#     "Monthly": 12,
#     "Yearly": 1
# }
# usd_df["AnnualComp"] = usd_df.apply(lambda row: row["CompTotal"] * frequency[row["CompFreq"]], axis=1)
#  Take only yearly CompFreq
annual_usd_df = usd_df[usd_df["CompFreq"] == "Yearly"]
highest_paid_companies_by_usd = annual_usd_df.sort_values(by="CompTotal", ascending=False)
# highest_paid_companies_by_usd.to_csv("max_annual_comp_in_usd.csv", index=False)
## We have found out a Mega Corporation in America with 10,000 or more than 10,000 employees offered the highest annual compensation in USD.

# 2. Remote work preferences sorted out by age group and main branch 
# Select the data from selected dataframe
remote_work_df = selected_df[["MainBranch", "RemoteWork", "Age"]]
# Take out the "None of these" cell value from the dataframe
remote_work_df = remote_work_df[remote_work_df["MainBranch"] != "None of these"]
# remote_work_df.to_csv("remote_work_df.csv", index=False)
#  Remote work preferences and age group 
count_remote_work_by_age = remote_work_df.groupby(["Age", "RemoteWork"]).size().reset_index(name='Count')
remote_work_by_age = count_remote_work_by_age.sort_values(by="Count", ascending=False)
# remote_work_by_age.to_csv("remote_work_by_age.csv", index=False) 
#  Remote work preferences and main branch
count_remote_work_by_professions = remote_work_df.groupby(["RemoteWork", "MainBranch"]).size().reset_index(name='Count')
remote_work_by_professions = count_remote_work_by_professions.sort_values(by="Count", ascending=False)
# remote_work_by_professions.to_csv("remote_work_by_professions.csv", index=False) 
#  Find out the count of professions by their age group
count_age_by_prefession = remote_work_df.groupby(["Age", "MainBranch"]).size().reset_index(name='Count')
age_by_prefession = count_age_by_prefession.sort_values(by="Count", ascending=False)
age_by_prefession.to_csv("age_by_prefession.csv", index=False)
## By these info, we have know that most of the developer by profession are with the age group of 25-34 years old and 
# they prefered fully remote work.

# 3. Did coding experience affect the level of pay (in USD)
# MainBranch, YearsCodePro, comptotal, currency
experience_df = selected_df[["MainBranch", "YearsCodePro", "CompFreq", "CompTotal", "Currency"]]
# Select the developer profession
filtered_experience_df = experience_df[selected_df["MainBranch"].isin([
    "I am a developer by profession",
    "I am not primarily a developer, but I write code sometimes as part of my work"
])]
#  Select the yearly paid
year_experience_df = filtered_experience_df[filtered_experience_df["CompFreq"] == "Yearly"]
#  Select only the USD currency
year_experience_df ["Currency"] = year_experience_df["Currency"].str.split().str[0]
year_experience_df = year_experience_df[year_experience_df ["Currency"] == "USD"]
# Gouped by their experience of coding
year_experience_df = year_experience_df.sort_values(by = "CompTotal", ascending=False)
# year_experience_df.to_csv("experience_df.csv", index=False) 
# Based on the info, we find out there is a developer by profession is having a 5 years coding experience have the most annual paid (USD 2520000),
# this developer have more annual paid compare with other developer or non-developer those who have more experience than him.

# 4.1 Most popular method learning to code
#"LearnCode", "LearnCodeOnline"
learning_code = selected_df[["LearnCode"]]
# Split all the learn code options
learning_code["LearnCode"] = learning_code["LearnCode"].str.replace(r'\([^)]*\)', '').str.split(";")
# Count each of the learning to code method
method_count = learning_code["LearnCode"].explode().value_counts().reset_index()
# Rename the column
method_count.columns = ["LearnCode", "CountLearnCode"]
method_count.to_csv("method_count.csv", index=False)
# We have found out most of the user are using other online resources and go for online courses/ certification to learn code.

# 4.2 Find out how many person learn code from online sources and what type of online source they are using
online_learning_code = selected_df[["LearnCodeOnline"]]
# Split the LearnCodeOnline
online_learning_code["LearnCodeOnline"] = online_learning_code["LearnCodeOnline"].str.replace(r'\([^)]*\)', '').str.split(";")
# Count method to find out how the contestant use online resources
online_sources_count = online_learning_code["LearnCodeOnline"].explode().value_counts().reset_index()
# Rename the column 
online_sources_count.columns = ["LearnCodeOnline", "CountLearnCodeOnline"]
online_sources_count.to_csv("online_sources_count.csv", index=False)
# Most of the user are using Techinical Documentaion and Stack Overflow 

# 5. Master Degree Vs Other study or degree sorted by developer position
# "MainBranch" "EdLevel" "Employment"
degree_job_df = selected_df[["MainBranch", "EdLevel"]]
# Select developer profession
degree_job_df = degree_job_df[degree_job_df["MainBranch"] == "I am a developer by profession"]
# Use count to calculate the total amount of developer by thier education level
count_degree_df = degree_job_df["EdLevel"].explode().value_counts().reset_index()
# Rename the column 
count_degree_df.columns = ["EduLevel", "CountDeveloper"]
count_degree_df.to_csv("degree_vs_dev.csv", index=False)
# As the result, we can see that developer which hold a Bachelor’s degree are more than those who were holding a Master’s degree (5276 Vs 2584).
# We can assume that holding a Master's degree doesn't mean easier to get a job.