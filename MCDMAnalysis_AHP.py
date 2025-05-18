import pandas as pd
import os
import numpy as np

class TreeNode:
    def __init__(self, code, name, weight, score):
        self.code = code
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

criteria_structure = {
    "code": None,
    "name": None,
    "weight": None,
    "children": [
        {
            "code": "2.1", "name": "Skill Appropriateness", "weight": 21.82, "children": [
                {"code": "2.1.1", "name": "Available positions", "weight": 25.64},
                {"code": "2.1.2", "name": "SKPvsESCO", "weight": 51.28},
                {"code": "2.1.3", "name": "Other skills", "weight": 23.08, "children": [
                    {"code": "2.1.3.1", "name": "Languages", "weight": 50.00},
                    {"code": "2.1.3.2", "name": "Driving license", "weight": 50.00},
                ]},
            ]
        },
        {
            "code": "2.2", "name": "Personal characteristics", "weight": 27.27, "children": [
                {"code": "2.2.1", "name": "Age appropriateness", "weight": 42.86},
                {"code": "2.2.2", "name": "Disability appropriateness", "weight": 42.86},
                {"code": "2.2.3", "name": "SKP Wish", "weight": 14.29},
            ]
        },
        {
            "code": "2.3", "name": "Job appropriateness", "weight": 50.91, "children": [
                {"code": "2.3.1", "name": "Contract type", "weight": 57.14, "children": [
                    {"code": "2.3.1.1", "name": "JS Wishes for contract type", "weight": 42.86},
                    {"code": "2.3.1.2", "name": "Job contract type", "weight": 57.14},
                ]},
                {"code": "2.3.2", "name": "Work type", "weight": 21.43, "children": [
                    {"code": "2.3.2.1", "name": "Career advance", "weight": 33.33, "children": [
                        {"code": "2.3.2.1.1", "name": "JS career wishes", "weight": 0.00001},
                        {"code": "2.3.2.1.2", "name": "Job career advancement", "weight": 99.9999},
                    ]},
                    {"code": "2.3.2.2", "name": "Working hours", "weight": 66.67, "children": [
                        {"code": "2.3.2.2.1", "name": "Job working hours", "weight": 50.00},
                        {"code": "2.3.2.2.2", "name": "JS working hours wishes", "weight": 50.00},
                    ]},
                ]},
                {"code": "2.3.3", "name": "Location", "weight": 21.43, "children": [
                    {"code": "2.3.3.1", "name": "Distance to job position", "weight": 69.23},
                    {"code": "2.3.3.2", "name": "JS wish location", "weight": 30.77},
                ]},
            ]
        }
    ]
}

def build_tree(node_dict, parent_score=None):
    weight = node_dict.get("weight")
    score = (weight / 100 * parent_score) if weight is not None and parent_score is not None else None

    node = TreeNode(
        code=node_dict.get("code"),
        name=node_dict.get("name"),
        weight=weight,
        score=score
    )

    for child_dict in node_dict.get("children", []):
        if score is not None:
            child_parent_score = score
        elif weight is not None:
            child_parent_score = weight / 100
        else:
            child_parent_score = None

        child_node = build_tree(child_dict, child_parent_score)
        node.addChild(child_node)

    return node

def get_leaf_scores(node):
    if not node.children:
        return [node.score]
    scores = []
    for child in node.children:
        scores.extend(get_leaf_scores(child))
    return scores

def calculate_criteria_relative_values():
    root = build_tree(criteria_structure, parent_score=1.0)
    CritRV = get_leaf_scores(root)
    return CritRV

def AHPReplaceValues(Alternatives: pd.DataFrame):
    # Replace qualitative values with quantitative
    # In the Excel file (AHPQuantVal.xlsx) it is explained how are quantitative values calculated

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

    # Criteria local values are taken from the (dexi weights.txt) file and all are divided by 100.
    # Values which belong to each hierarchical node are multiplied with the criteria value of that node.
    CritRV = calculate_criteria_relative_values()

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

    return AlterRankingsAHP_df

#Load TotalSKPData.csv
filename = 'AHP_test.csv'  #load sample of first 100
#filename = 'TotalSKPData.csv'  #load complete TotalSKPData

directory = './Results'
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

AHPRanking_df.to_csv(directory + '/AHP_Results.csv', sep=';', index=True, header=True)