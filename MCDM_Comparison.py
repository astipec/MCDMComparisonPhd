import os
import pandas as pd

from GenAllAlternatives import GenerateDataFrame

from DEX_RANKING import GetDEXRankingResults
from AHP import AHPReplaceValues
from AHP import GetAHPRankingResults
from TOPSIS import TOPSISReplaceValues
from TOPSIS import GetTOPSISRankingResults
from PROMETHEE import PROMETHEEReplaceValues
from PROMETHEE import GetPROMETHEERankingResults
from PAPRIKA import PAPRIKAReplaceValues
from PAPRIKA import GetPAPRIKARankingResults

from Statistics import CalcCorrelations

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    print("\nMAIN MENU")
    print("Select option:")
    print("1. Generate dataset with all possible combinations")
    print("2. DEX Ranking (baseline)")
    print("3. AHP Ranking")
    print("4. TOPSIS Ranking")
    print("5. PROMETHEE II Ranking")
    print("6. PAPRIKA Ranking")
    print("7. Calculate comparison statistics")
    print("--------------------------------------------------")
    print("0. Exit program\n")

def ImportCSVtoDataFrame(filePath):
    if os.path.exists(filePath):
        try:
            df = pd.read_csv(filePath, delimiter=';', index_col=0)
            print("\nCSV file successfully loaded!")
            print(df.head())
            return df
        except Exception as e:
            print(f"\nError while reading CSV file: {e}")
            return None
    else:
        print(f"\nCSV file not found at: {filePath}")
        print(f"Dataframe must be generated first.")
        return None

def option_1(): #Create dataset with all combinations
    while True:
        clear_screen()
        print("\nGenerate dataset with all possible combinations\n")
        print("Select option:")
        print("1. This will generate dataset with all possible options for the following criteria:")
        print("   Available positions, SKPvsESCO, Languages, Driving license, Age appropriateness,")
        print("   Disability appropriateness, SKP Wish, JS wishes for contract type, Job contract type,")
        print("   JS career wishes, Job career advancement, Job working hours, JS working hours wishes,")
        print("   Distance to job position, JS wish location")
        print("--------------------------------------------------")
        print("0. Return to main menu\n")

        choice = input("Insert option number: ")

        if choice == "1":
            GenerateDataFrame()

            input("\nPress enter")
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

def option_2():  #DEX Ranking
    while True:
        clear_screen()
        print("\nDEX Ranking (baseline)\n")
        print("Select option:")
        print("1. Rank dataset using DEX method")
        print("--------------------------------------------------")
        print("0. Return to main menu\n")

        choice = input("Insert option number: ")

        if choice == "1":
            file_path = './Results/TotalSKPData.csv'
            results_path = './Results/DEX_Results.csv'
            absolute_path = os.path.abspath(results_path)
            os.makedirs(os.path.dirname(results_path), exist_ok=True)

            AlternativesDEX = ImportCSVtoDataFrame(file_path)
            DEXRanked = GetDEXRankingResults(AlternativesDEX)

            DEXRanked.to_csv(results_path, sep=';', index=True, header=True)

            print("\nDEX ranking completed successfully.")
            print(f'DEX ranking results are saved to CSV file successfully at:\n{absolute_path}')
            input("\nPress enter")
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

def option_3():  #AHP Ranking
    while True:
        clear_screen()
        print("\nAHP Ranking\n")
        print("Select option:")
        print("1. Rank dataset using AHP method")
        print("--------------------------------------------------")
        print("0. Return to main menu\n")

        choice = input("Insert option number: ")

        if choice == "1":
            file_path = './Results/TotalSKPData.csv'
            results_path = './Results/AHP_Results.csv'
            absolute_path = os.path.abspath(results_path)
            os.makedirs(os.path.dirname(results_path), exist_ok=True)

            AlternativesAHP = ImportCSVtoDataFrame(file_path)
            AHPReplaced = AHPReplaceValues(AlternativesAHP)
            AHPRanked = GetAHPRankingResults(AHPReplaced)

            AHPRanked.to_csv(results_path, sep=';', index=True, header=True)

            print("\nAHP ranking completed successfully.")
            print(f'AHP ranking results are saved to CSV file successfully at:\n{absolute_path}')
            input("\nPress enter")
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

def option_4():  #TOPSIS Ranking
    while True:
        clear_screen()
        print("\nTOPSIS Ranking\n")
        print("Select option:")
        print("1. Rank dataset using TOPSIS method")
        print("--------------------------------------------------")
        print("0. Return to main menu\n")

        choice = input("Insert option number: ")

        if choice == "1":
            file_path = './Results/TotalSKPData.csv'
            results_path = './Results/TOPSIS_Results.csv'
            absolute_path = os.path.abspath(results_path)
            os.makedirs(os.path.dirname(results_path), exist_ok=True)

            AlternativesTOPSIS = ImportCSVtoDataFrame(file_path)
            TOPSISReplaced = TOPSISReplaceValues(AlternativesTOPSIS)
            TOPSISRanked = GetTOPSISRankingResults(TOPSISReplaced)

            TOPSISRanked.to_csv(results_path, sep=';', index=True, header=True)

            print("\nTOPSIS ranking completed successfully.")
            print(f'TOPSIS ranking results are saved to CSV file successfully at:\n{absolute_path}')
            input("\nPress enter")
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

def option_5():  #PROMETHEE II Ranking
    while True:
        clear_screen()
        print("\nPROMETHEE II Ranking\n")
        print("Select option:")
        print("1. Rank dataset using PROMETHEE II method")
        print("--------------------------------------------------")
        print("0. Return to main menu\n")

        choice = input("Insert option number: ")

        if choice == "1":
            file_path = './Results/TotalSKPData.csv'
            results_path = './Results/PROMETHEE_Results.csv'
            absolute_path = os.path.abspath(results_path)
            os.makedirs(os.path.dirname(results_path), exist_ok=True)

            AlternativesPROMETHEE = ImportCSVtoDataFrame(file_path)
            PROMETHEEReplaced = PROMETHEEReplaceValues(AlternativesPROMETHEE)
            PROMETHEERanked = GetPROMETHEERankingResults(PROMETHEEReplaced)

            PROMETHEERanked.to_csv(results_path, sep=';', index=True, header=True)

            print("\nPROMETHEE ranking completed successfully.")
            print(f'PROMETHEE ranking results are saved to CSV file successfully at:\n{absolute_path}')
            input("\nPress enter")
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

def option_6():  #PAPRIKA Ranking
    while True:
        clear_screen()
        print("\nPAPRIKA Ranking\n")
        print("Select option:")
        print("1. Rank dataset using PAPRIKA method")
        print("--------------------------------------------------")
        print("0. Return to main menu\n")

        choice = input("Insert option number: ")

        if choice == "1":
            file_path = './Results/TotalSKPData.csv'
            results_path = './Results/PAPRIKA_Results.csv'
            absolute_path = os.path.abspath(results_path)
            os.makedirs(os.path.dirname(results_path), exist_ok=True)

            AlternativesPAPRIKA = ImportCSVtoDataFrame(file_path)
            PAPRIKAReplaced = PAPRIKAReplaceValues(AlternativesPAPRIKA)
            PAPRIKARanked = GetPAPRIKARankingResults(PAPRIKAReplaced)

            PAPRIKARanked.to_csv(results_path, sep=';', index=True, header=True)

            print("\nPAPRIKA ranking completed successfully.")
            print(f'PAPRIKA ranking results are saved to CSV file successfully at:\n{absolute_path}')
            input("\nPress enter")
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

def option_7():  #Statistics
    while True:
        clear_screen()
        print("\nCalculate comparison statistics")
        print("All previous rankings are required for this step!!!")
        print("Select option:")
        print("1. Draw rankings of first 10 alternatives")
        print("2. Calculate correlation coefficients (Spearman's, Pearson's, Kendall's)")
        print("--------------------------------------------------")
        print("0. Return to main menu\n")

        choice = input("Insert option number: ")

        if choice == "1":
            print("\nWill be added.\n")
        elif choice == "2":
            CalcCorrelations()
            input("\nPress enter")
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

def main():
    while True:
        clear_screen()
        main_menu()
        choice = input("Insert option number: ")

        if choice == "1":
            option_1()
        elif choice == "2":
            option_2()
        elif choice == "3":
            option_3()
        elif choice == "4":
            option_4()
        elif choice == "5":
            option_5()
        elif choice == "6":
            option_6()
        elif choice == "7":
            option_7()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

if __name__== "__main__":
    main()