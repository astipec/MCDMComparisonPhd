import pandas as pd
import os
import numpy as np

#Names of the criteria
col_available_positions = 'Available positions'
col_skp_vs_esco = 'SKPvsESCO'
col_languages = 'Languages'
col_driving_license = 'Driving license'
col_age = 'Age appropriateness'
col_disability = 'Disability appropriateness'
col_skp_wish = 'SKP Wish'
col_js_contract_wish = 'JS wishes for contract type'
col_job_contract = 'Job contract type'
col_js_career = 'JS career wishes'
col_job_advancement = 'Job career advancement'
col_job_hours = 'Job working hours'
col_js_hours = 'JS working hours wishes'
col_distance = 'Distance to job position'
col_location = 'JS wish location'

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
                {"code": "2.1.1", "name": col_available_positions, "weight": 25.64},
                {"code": "2.1.2", "name": col_skp_vs_esco, "weight": 51.28},
                {"code": "2.1.3", "name": "Other skills", "weight": 23.08, "children": [
                    {"code": "2.1.3.1", "name": col_languages, "weight": 50.00},
                    {"code": "2.1.3.2", "name": col_driving_license, "weight": 50.00},
                ]},
            ]
        },
        {
            "code": "2.2", "name": "Personal characteristics", "weight": 27.27, "children": [
                {"code": "2.2.1", "name": col_age, "weight": 42.86},
                {"code": "2.2.2", "name": col_disability, "weight": 42.86},
                {"code": "2.2.3", "name": col_skp_wish, "weight": 14.29},
            ]
        },
        {
            "code": "2.3", "name": "Job appropriateness", "weight": 50.91, "children": [
                {"code": "2.3.1", "name": "Contract type", "weight": 57.14, "children": [
                    {"code": "2.3.1.1", "name": col_js_contract_wish, "weight": 42.86},
                    {"code": "2.3.1.2", "name": col_job_contract, "weight": 57.14},
                ]},
                {"code": "2.3.2", "name": "Work type", "weight": 21.43, "children": [
                    {"code": "2.3.2.1", "name": "Career advance", "weight": 33.33, "children": [
                        {"code": "2.3.2.1.1", "name": col_js_career, "weight": 0.00001},
                        {"code": "2.3.2.1.2", "name": col_job_advancement, "weight": 99.9999},
                    ]},
                    {"code": "2.3.2.2", "name": "Working hours", "weight": 66.67, "children": [
                        {"code": "2.3.2.2.1", "name": col_job_hours, "weight": 50.00},
                        {"code": "2.3.2.2.2", "name": col_js_hours, "weight": 50.00},
                    ]},
                ]},
                {"code": "2.3.3", "name": "Location", "weight": 21.43, "children": [
                    {"code": "2.3.3.1", "name": col_distance, "weight": 69.23},
                    {"code": "2.3.3.2", "name": col_location, "weight": 30.77},
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

    map_three = {'small': 0.06096, 'medium': 0.21577, 'large': 0.72327}
    map_competences = {'>10': 0.06096, '5 - 10': 0.21577, '< 5 new competences': 0.72327}
    map_yes_no = {'no': 0.09955, 'yes': 0.90045}
    map_part_full = {'part time': 0.06096, 'full time': 0.21577, 'not important': 0.72327}
    map_contract = {'part time': 0.09955, 'full time': 0.90045}
    map_career = {'downgrade': 0.04767, 'same': 0.10841, 'not important': 0.25835, 'upgrade career': 0.58558}
    map_advancement = {'down': 0.06096, 'same': 0.21577, 'up': 0.72327}
    map_hours = {'daily/night shift': 0.04767, 'two-shift': 0.10841, 'afternoon shift': 0.25835,
                 'morning shift': 0.58558}
    map_distance = {'> 20 km': 0.06096, '10 - 20 km': 0.21577, '< 10 km': 0.72327}

    replacement_maps = {
        col_available_positions: map_three,
        col_skp_vs_esco: map_competences,
        col_languages: map_yes_no,
        col_driving_license: map_yes_no,
        col_age: map_yes_no,
        col_disability: map_yes_no,
        col_skp_wish: map_yes_no,
        col_js_contract_wish: map_part_full,
        col_job_contract: map_contract,
        col_js_career: map_career,
        col_job_advancement: map_advancement,
        col_job_hours: map_hours,
        col_js_hours: map_hours,
        col_distance: map_distance,
        col_location: map_yes_no
    }

    pd.set_option('future.no_silent_downcasting', True)

    for column, value_map in replacement_maps.items():
        Alternatives[column] = Alternatives[column].replace(value_map)

    return Alternatives

def GetAHPRankingResults(AlterAHP: pd.DataFrame):
    np.set_printoptions(precision=8)

    # Criteria local values are taken from the (dexi weights.txt) file and all are divided by 100.
    # Values which belong to each hierarchical node are multiplied with the criteria value of that node.
    CritRV = calculate_criteria_relative_values()

    print('Criteria relative values')
    print(CritRV)
    print('-' * 58)

    #Calculate weighted matrix
    columns = [
        col_available_positions,
        col_skp_vs_esco,
        col_languages,
        col_driving_license,
        col_age,
        col_disability,
        col_skp_wish,
        col_js_contract_wish,
        col_job_contract,
        col_js_career,
        col_job_advancement,
        col_job_hours,
        col_js_hours,
        col_distance,
        col_location
    ]

    for col, weight in zip(columns, CritRV):
        AlterAHP[col] = AlterAHP[col].multiply(weight)

    # Print the weighted matrix
    print('Weighted matrix:')
    print(AlterAHP)
    print('-' * 58)

    #Determine the max value for each criterion
    AlterMaxValues = AlterAHP.max()

    print('Maximum value of the alternatives for each criterion.')
    print(AlterMaxValues)
    print('-' * 58)

    #Divide values by the max value of each criterion and multiply by criterion value
    columns = [
        col_available_positions,
        col_skp_vs_esco,
        col_languages,
        col_driving_license,
        col_age,
        col_disability,
        col_skp_wish,
        col_js_contract_wish,
        col_job_contract,
        col_js_career,
        col_job_advancement,
        col_job_hours,
        col_js_hours,
        col_distance,
        col_location
    ]

    for col, weight in zip(columns, CritRV):
        max_val = AlterMaxValues[col]
        if max_val != 0 and pd.notnull(max_val):
            AlterAHP[col] = AlterAHP[col].divide(max_val).multiply(weight)
        else:
            AlterAHP[col] = 0

    row_sums = AlterAHP.sum(axis=1)

    AlterRankingsAHP_df = row_sums.to_frame('AHP')

    return AlterRankingsAHP_df

filename = 'AHP_test.csv'  #load test sample (this is small sample of data for testing purposes)
#filename = 'TotalSKPData.csv'  #load complete TotalSKPData (first run MCDMAnalysis_SKPdata.py to generate the dataset)

directory = './Results'
if not os.path.exists(directory):
    os.makedirs(directory)

TotalSKPData_df = pd.read_csv('./'+filename, index_col=0, delimiter=';')

print("TotalSKPData dataframe:")
print(TotalSKPData_df)
print('-' * 58)

# AHP Ranking
print("AHP RANKING:")
print('-' * 58)

TotalSKPData_RepVal = AHPReplaceValues(TotalSKPData_df)
print("TotalSKPData Criteria categories values dataframe:")
print(TotalSKPData_RepVal)
print('-' * 58)

AHPRanking_df = GetAHPRankingResults(TotalSKPData_RepVal)

# Print final ranking
print('AHP final ranking results:')
print(AHPRanking_df)
print('-' * 58)

AHPRanking_df.to_csv(directory + '/AHP_Results.csv', sep=';', index=True, header=True)