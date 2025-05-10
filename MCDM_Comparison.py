import os
import pandas as pd

from GenAllAlternatives import GenerateDataFrame
from DEX_RANKING import GetDEXRankingResults

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    print("\nMAIN MENU")
    print("Select option:")
    print("1. Generate dataset with all possible combinations")
    print("2. DEX Ranking (baseline)")
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
        print("1. Rank dataset using DEX method\n")
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

def main():
    while True:
        clear_screen()
        main_menu()
        choice = input("Insert option number: ")

        if choice == "1":
            option_1()
        elif choice == "2":
            option_2()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

if __name__== "__main__":
    main()