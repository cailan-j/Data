import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv(r'adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    ### Use value_counts on 'race' to find # of people from each race
    race_count = df['race'].value_counts()

    # What is the average age of men?
    ### Locate all rows where 'sex' == 'Male', use values to aggregate 'age'
    ### Calculate mean on aggregated data, round float to 1 decimal
    average_age_men = round((df.loc[df['sex'] == 'Male'])['age'].mean(),1)

    # What is the percentage of people who have a Bachelor's degree?
    ### Find the normalized value_counts of each education level
    ### Locate 'Bachelors' row, *100 and round to 1 decimal
    percentage_bachelors = ((df['education'].value_counts(normalize=True)).loc['Bachelors']*100).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
   
    # with and without `Bachelors`, `Masters`, or `Doctorate`
    ### Find all rows that contain 'Bachelors', 'Masters', 'Doctorate' in 'education', use to aggregate dataframe
    higher_education = df.loc[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_education = df.loc[~df['education'].isin(['Bachelors','Masters','Doctorate'])]

    # percentage with salary >50K
    ### Calculate normalized value_counts on aggregated data where 'salary' is '>50K', *100, round to 1 decimal
    higher_education_rich = (higher_education['salary'].value_counts(normalize=True).loc['>50K']*100).round(1)
    lower_education_rich = (lower_education['salary'].value_counts(normalize=True).loc['>50K']*100).round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    ### find the min value of 'hours-per-week'
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    ### make dataframe of just people who worked the minimum number of hours per week
    num_min_workers = df[df['hours-per-week']== min_work_hours]
    ### Calculate normalized value_counts on aggregated data where 'salary' is '>50K', *100, round to 1 decimal
    rich_percentage = (num_min_workers['salary'].value_counts(normalize=True).loc['>50K']*100).round(1)

    # What country has the highest percentage of people that earn >50K?
    ### Group data by 'native-country' and 'salary', unstack salary so there are two columns 
    sort = df.groupby(['native-country','salary'])['salary'].count().unstack(level=1)
    ### Use sorted dataframe to calculate ratio of rich people/country, identify id and max percent
    highest_earning_country = (sort.iloc[:,1]/(sort.iloc[:,0]+sort.iloc[:,1])).idxmax()
    highest_earning_country_percentage = round((sort.iloc[:,1]/(sort.iloc[:,0]+sort.iloc[:,1])).max()*100,1)

    # Identify the most popular occupation for those who earn >50K in India.
    ### Find all rows where 'salary' == '>50K', find all rows where 'native-country'=='India'
    ### Take 'occupation' column from new dataframe, count all values and find max
    top_IN_occupation = ((df.loc[df['salary']=='>50K']).loc[df['native-country']=='India'])['occupation'].value_counts().idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            f"Percentage with higher education that earn >50K: {higher_education_rich}%"
        )
        print(
            f"Percentage without higher education that earn >50K: {lower_education_rich}%"
        )
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            f"Percentage of rich among those who work fewest hours: {rich_percentage}%"
        )
        print("Country with highest percentage of rich:",
              highest_earning_country)
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%"
        )
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
