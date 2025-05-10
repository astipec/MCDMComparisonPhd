import os

from GenAllAlternatives import GenerateDataFrame

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    print("\nMAIN MENU")
    print("Select option:")
    print("1. Generate dataset with all possible combinations")
    print("--------------------------------------------------")
    print("0. Exit program\n")

def option_1():
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

def main():
    while True:
        clear_screen()
        main_menu()
        choice = input("Insert option number: ")

        if choice == "1":
            option_1()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

if __name__== "__main__":
    main()