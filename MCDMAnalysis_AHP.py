import pandas as pd
import os
import numpy as np

class TreeNode:
    def __init__(self, ID, name, weight, score):
        self.ID = ID
        self.name = name
        self.weight = weight
        self.score = score
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def serialize(self):
        s = {}
        for child in self.children:
            s[child.name] = child.serialize()
        return s

def AHPReplaceValues(Alternatives: pd.DataFrame):
    # The procedure of how the values are calculated is shown in the SKP AHP relative measures weights.xlsx file, on the Categoris sheet.
    # For each of the 15 criteria at the bottom level, their categories are pairwise compared according to the DEX model.
    # For example, the Available positions criteria, large is the best value, then medium and small is the worst,
    # Categories are compared in way that large has the best score, small the worst and medium is somwhere in the middle.
    # All other categories for all other criteria are compared in the same way.

    pd.set_option('future.no_silent_downcasting', True)

    Alternatives['Available positions'] = Alternatives['Available positions'].replace(['small', 'medium', 'large'],
                                                                                      [0.06096, 0.21577,0.72327])
    Alternatives['SKPvsESCO'] = Alternatives['SKPvsESCO'].replace(['>10', '5 - 10', '< 5 new competences'],
                                                                  [0.06096, 0.21577, 0.72327])
    Alternatives['Languages'] = Alternatives['Languages'].replace(['no', 'yes'],
                                                                  [0.09955, 0.90045])
    Alternatives['Driving license'] = Alternatives['Driving license'].replace(['no', 'yes'],
                                                                              [0.09955, 0.90045])
    Alternatives['Age appropriateness'] = Alternatives['Age appropriateness'].replace(['no', 'yes'],
                                                                                      [0.09955, 0.90045])
    Alternatives['Disability appropriateness'] = Alternatives['Disability appropriateness'].replace(['no', 'yes'],
                                                                                                    [0.09955, 0.90045])
    Alternatives['SKP Wish'] = Alternatives['SKP Wish'].replace(['no', 'yes'],
                                                                [0.09955, 0.90045])
    Alternatives['JS wishes for contract type'] = Alternatives['JS wishes for contract type'].replace(['part time', 'full time', 'not important'],
                                                                                                      [0.06096, 0.21577, 0.72327])
    Alternatives['Job contract type'] = Alternatives['Job contract type'].replace(['part time', 'full time'],
                                                                                  [0.09955, 0.90045])
    Alternatives['JS career wishes'] = Alternatives['JS career wishes'].replace(['downgrade', 'same', 'not important', 'upgrade career'],
                                                                                [0.04767, 0.10841, 0.25835, 0.58558])
    Alternatives['Job career advancement'] = Alternatives['Job career advancement'].replace(['down', 'same', 'up'],
                                                                                            [0.06096, 0.21577, 0.72327])
    Alternatives['Job working hours'] = Alternatives['Job working hours'].replace(['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift'],
                                                                                  [0.04767, 0.10841, 0.25835, 0.58558])
    Alternatives['JS working hours wishes'] = Alternatives['JS working hours wishes'].replace(['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift'],
                                                                                              [0.04767, 0.10841, 0.25835, 0.58558])
    Alternatives['Distance to job position'] = Alternatives['Distance to job position'].replace(['> 20 km', '10 - 20 km', '< 10 km'],
                                                                                                [0.06096, 0.21577, 0.72327])
    Alternatives['JS wish location'] = Alternatives['JS wish location'].replace(['no', 'yes'],
                                                                                [0.09955, 0.90045])

    return Alternatives

def GetAHPRankingResults(AlterAHP: pd.DataFrame):
    np.set_printoptions(precision=8)

    # Calculate the criteria values from dexi weights.txt using local values.
    # Procedure of how the weight values for the 15 bottom criteria are calculated is in the SKP AHP relative measures weights.xlsx file, on the Criteria sheet.
    # AHP TREE STRUCTURE
    SKP_Evaluation = TreeNode(None, None, None, None)

    Skill_Appropriateness = TreeNode("2.1", "Skill Appropriateness", 21.82, None)
    SKP_Evaluation.addChild(Skill_Appropriateness)

    Personal_characteristics = TreeNode("2.2", "Personal characteristics", 27.27, None)
    SKP_Evaluation.addChild(Personal_characteristics)

    Job_appropriateness = TreeNode("2.3", "Job appropriateness", 50.91, None)
    SKP_Evaluation.addChild(Job_appropriateness)

    Available_positions = TreeNode("2.1.1", "Available positions", 25.64, None)
    Available_positions.score = Available_positions.weight / 100 * Skill_Appropriateness.weight / 100
    Skill_Appropriateness.addChild(Available_positions)

    SKPvsESCO = TreeNode("2.1.2", "SKPvsESCO", 51.28, None)
    SKPvsESCO.score = SKPvsESCO.weight / 100 * Skill_Appropriateness.weight / 100
    Skill_Appropriateness.addChild(SKPvsESCO)

    Other_skills = TreeNode("2.1.3", "Other skills", 23.08, None)
    Other_skills.score = Other_skills.weight / 100 * Skill_Appropriateness.weight / 100
    Skill_Appropriateness.addChild(Other_skills)

    Languages = TreeNode("2.1.3.1", "Languages", 50.00, None)
    Languages.score = Languages.weight / 100 * Other_skills.score
    Other_skills.addChild(Languages)

    Driving_license = TreeNode("2.1.3.2", "Driving license", 50.00, None)
    Driving_license.score = Driving_license.weight / 100 * Other_skills.score
    Other_skills.addChild(Driving_license)

    Age_appropriateness = TreeNode("2.2.1", "Age appropriateness", 42.86, None)
    Age_appropriateness.score = Age_appropriateness.weight / 100 * Personal_characteristics.weight / 100
    Personal_characteristics.addChild(Age_appropriateness)

    Disability_appropriateness = TreeNode("2.2.2", "Disability appropriateness", 42.86, None)
    Disability_appropriateness.score = Disability_appropriateness.weight / 100 * Personal_characteristics.weight / 100
    Personal_characteristics.addChild(Disability_appropriateness)

    SKP_Wish = TreeNode("2.2.3", "SKP Wish", 14.29, None)
    SKP_Wish.score = SKP_Wish.weight / 100 * Personal_characteristics.weight / 100
    Personal_characteristics.addChild(SKP_Wish)

    Contract_Type = TreeNode("2.3.1", "Contract type", 57.14, None)
    Contract_Type.score = Contract_Type.weight / 100 * Job_appropriateness.weight / 100
    Job_appropriateness.addChild(Contract_Type)

    Work_Type = TreeNode("2.3.2", "Work type", 21.43, None)
    Work_Type.score = Work_Type.weight / 100 * Job_appropriateness.weight / 100
    Job_appropriateness.addChild(Work_Type)

    Location = TreeNode("2.3.3", "Location", 21.43, None)
    Location.score = Location.weight / 100 * Job_appropriateness.weight / 100
    Job_appropriateness.addChild(Location)

    JS_Wish_ContrType = TreeNode("2.3.1.1", "JS Wishes for contract type", 42.86, None)
    JS_Wish_ContrType.score = JS_Wish_ContrType.weight / 100 * Contract_Type.score
    Contract_Type.addChild(JS_Wish_ContrType)

    Job_ContrType = TreeNode("2.3.1.2", "Job contract type", 57.14, None)
    Job_ContrType.score = Job_ContrType.weight / 100 * Contract_Type.score
    Contract_Type.addChild(Job_ContrType)

    Career_Advance = TreeNode("2.3.2.1", "Career advance", 33.33, None)
    Career_Advance.score = Career_Advance.weight / 100 * Work_Type.score
    Work_Type.addChild(Career_Advance)

    Working_Hours = TreeNode("2.3.2.2", "Working hours", 66.67, None)
    Working_Hours.score = Working_Hours.weight / 100 * Work_Type.score
    Work_Type.addChild(Working_Hours)

    JS_Career_Wishes = TreeNode("2.3.2.1.1", "JS career wishes", 0.00001, None)
    JS_Career_Wishes.score = JS_Career_Wishes.weight / 100 * Career_Advance.score
    Career_Advance.addChild(JS_Career_Wishes)

    Job_Career_Advancement = TreeNode("2.3.2.1.2", "Job career advancement", 99.9999, None)
    Job_Career_Advancement.score = Job_Career_Advancement.weight / 100 * Career_Advance.score
    Career_Advance.addChild(Job_Career_Advancement)

    Job_Working_Hours = TreeNode("2.3.2.2.1", "Job working hours", 50.00, None)
    Job_Working_Hours.score = Job_Working_Hours.weight / 100 * Working_Hours.score
    Working_Hours.addChild(Job_Working_Hours)

    JS_WorkingH_Wishes = TreeNode("2.3.2.2.2", "JS working hours wishes", 50.00, None)
    JS_WorkingH_Wishes.score = JS_WorkingH_Wishes.weight / 100 * Working_Hours.score
    Working_Hours.addChild(JS_WorkingH_Wishes)

    Distance_JobPosition = TreeNode("2.3.3.1", "Distance to job position", 69.23, None)
    Distance_JobPosition.score = Distance_JobPosition.weight / 100 * Location.score
    Location.addChild(Distance_JobPosition)

    JS_Wish_Location = TreeNode("2.3.3.2", "JS wish location", 30.77, None)
    JS_Wish_Location.score = JS_Wish_Location.weight / 100 * Location.score
    Location.addChild(JS_Wish_Location)

    # Criteria relative values
    CritRV = []
    CritRV.append(Available_positions.score)
    CritRV.append(SKPvsESCO.score)
    CritRV.append(Languages.score)
    CritRV.append(Driving_license.score)
    CritRV.append(Age_appropriateness.score)
    CritRV.append(Disability_appropriateness.score)
    CritRV.append(SKP_Wish.score)
    CritRV.append(JS_Wish_ContrType.score)
    CritRV.append(Job_ContrType.score)
    CritRV.append(JS_Career_Wishes.score)
    CritRV.append(Job_Career_Advancement.score)
    CritRV.append(Job_Working_Hours.score)
    CritRV.append(JS_WorkingH_Wishes.score)
    CritRV.append(Distance_JobPosition.score)
    CritRV.append(JS_Wish_Location.score)

    print('Criteria relative values')
    print(CritRV)
    print('----------------------------------------------------------')

    #Calculate weighted matrix
    AlterAHP['Available positions'] = AlterAHP['Available positions'].multiply(CritRV[0])
    AlterAHP['SKPvsESCO'] = AlterAHP['SKPvsESCO'].multiply(CritRV[1])
    AlterAHP['Languages'] = AlterAHP['Languages'].multiply(CritRV[2])
    AlterAHP['Driving license'] = AlterAHP['Driving license'].multiply(CritRV[3])
    AlterAHP['Age appropriateness'] = AlterAHP['Age appropriateness'].multiply(CritRV[4])
    AlterAHP['Disability appropriateness'] = AlterAHP['Disability appropriateness'].multiply(CritRV[5])
    AlterAHP['SKP Wish'] = AlterAHP['SKP Wish'].multiply(CritRV[6])
    AlterAHP['JS wishes for contract type'] = AlterAHP['JS wishes for contract type'].multiply(CritRV[7])
    AlterAHP['Job contract type'] = AlterAHP['Job contract type'].multiply(CritRV[8])
    AlterAHP['JS career wishes'] = AlterAHP['JS career wishes'].multiply(CritRV[9])
    AlterAHP['Job career advancement'] = AlterAHP['Job career advancement'].multiply(CritRV[10])
    AlterAHP['Job working hours'] = AlterAHP['Job working hours'].multiply(CritRV[11])
    AlterAHP['JS working hours wishes'] = AlterAHP['JS working hours wishes'].multiply(CritRV[12])
    AlterAHP['Distance to job position'] = AlterAHP['Distance to job position'].multiply(CritRV[13])
    AlterAHP['JS wish location'] = AlterAHP['JS wish location'].multiply(CritRV[14])

    # Print the weighted matrix
    print('Weighted matrix:')
    print(AlterAHP)
    print('----------------------------------------------------------')

    #Determine the max value for each criterion
    AlterMaxValues = AlterAHP.max()

    print('Maximum value of the alternatives for each criterion.')
    print(AlterMaxValues)
    print('----------------------------------------------------------')

    #Divide values by the max value of each crtierion and multiply by criterion value
    AlterAHP['Available positions'] = AlterAHP['Available positions'].divide(AlterMaxValues['Available positions'])
    AlterAHP['SKPvsESCO'] = AlterAHP['SKPvsESCO'].divide(AlterMaxValues['SKPvsESCO'])
    AlterAHP['Languages'] = AlterAHP['Languages'].divide(AlterMaxValues['Languages'])
    AlterAHP['Driving license'] = AlterAHP['Driving license'].divide(AlterMaxValues['Driving license'])
    AlterAHP['Age appropriateness'] = AlterAHP['Age appropriateness'].divide(AlterMaxValues['Age appropriateness'])
    AlterAHP['Disability appropriateness'] = AlterAHP['Disability appropriateness'].divide(AlterMaxValues['Disability appropriateness'])
    AlterAHP['SKP Wish'] = AlterAHP['SKP Wish'].divide(AlterMaxValues['SKP Wish'])
    AlterAHP['JS wishes for contract type'] = AlterAHP['JS wishes for contract type'].divide(AlterMaxValues['JS wishes for contract type'])
    AlterAHP['Job contract type'] = AlterAHP['Job contract type'].divide(AlterMaxValues['Job contract type'])
    AlterAHP['JS career wishes'] = AlterAHP['JS career wishes'].divide(AlterMaxValues['JS career wishes'])
    AlterAHP['Job career advancement'] = AlterAHP['Job career advancement'].divide(AlterMaxValues['Job career advancement'])
    AlterAHP['Job working hours'] = AlterAHP['Job working hours'].divide(AlterMaxValues['Job working hours'])
    AlterAHP['JS working hours wishes'] = AlterAHP['JS working hours wishes'].divide(AlterMaxValues['JS working hours wishes'])
    AlterAHP['Distance to job position'] = AlterAHP['Distance to job position'].divide(AlterMaxValues['Distance to job position'])
    AlterAHP['JS wish location'] = AlterAHP['JS wish location'].divide(AlterMaxValues['JS wish location'])

    AlterAHP['Available positions'] = AlterAHP['Available positions'].multiply(CritRV[0])
    AlterAHP['SKPvsESCO'] = AlterAHP['SKPvsESCO'].multiply(CritRV[1])
    AlterAHP['Languages'] = AlterAHP['Languages'].multiply(CritRV[2])
    AlterAHP['Driving license'] = AlterAHP['Driving license'].multiply(CritRV[3])
    AlterAHP['Age appropriateness'] = AlterAHP['Age appropriateness'].multiply(CritRV[4])
    AlterAHP['Disability appropriateness'] = AlterAHP['Disability appropriateness'].multiply(CritRV[5])
    AlterAHP['SKP Wish'] = AlterAHP['SKP Wish'].multiply(CritRV[6])
    AlterAHP['JS wishes for contract type'] = AlterAHP['JS wishes for contract type'].multiply(CritRV[7])
    AlterAHP['Job contract type'] = AlterAHP['Job contract type'].multiply(CritRV[8])
    AlterAHP['JS career wishes'] = AlterAHP['JS career wishes'].multiply(CritRV[9])
    AlterAHP['Job career advancement'] = AlterAHP['Job career advancement'].multiply(CritRV[10])
    AlterAHP['Job working hours'] = AlterAHP['Job working hours'].multiply(CritRV[11])
    AlterAHP['JS working hours wishes'] = AlterAHP['JS working hours wishes'].multiply(CritRV[12])
    AlterAHP['Distance to job position'] = AlterAHP['Distance to job position'].multiply(CritRV[13])
    AlterAHP['JS wish location'] = AlterAHP['JS wish location'].multiply(CritRV[14])

    row_sums = AlterAHP.sum(axis=1)

    AlterRankingsAHP_df = row_sums.to_frame('AHP')

    # Print final ranking
    print('AHP final ranking results:')
    print(AlterRankingsAHP_df)
    print('----------------------------------------------------------')

    return AlterRankingsAHP_df

#Load TotalSKPData.csv
#filename = 'SKPData_sample100.csv'  #load sample of first 100
filename = 'TotalSKPData.csv'  #load complete TotalSKPData

directory = './Results/' + filename.replace('.csv', '')
if not os.path.exists(directory):
    os.makedirs(directory)

TotalSKPData_df = pd.read_csv('./'+filename, index_col=0, delimiter=';')

print("TotalSKPData dataframe:")
print(TotalSKPData_df)
print("----------------------------------------------------------")

# AHP Ranking
print("AHP RANKING:")
print("----------------------------------------------------------")

TotalSKPData_RepVal = AHPReplaceValues(TotalSKPData_df)
print("TotalSKPData Criteria categories values dataframe:")
print(TotalSKPData_RepVal)
print("---------------------------")

AHPRanking_df = GetAHPRankingResults(TotalSKPData_RepVal)

# Print final ranking
print('AHP final ranking results:')
print(AHPRanking_df)
print('----------------------------------------------------------')

AHPRanking_df.to_csv(directory + '/AHPRanking_' + filename, sep=';', index=True, header=True)