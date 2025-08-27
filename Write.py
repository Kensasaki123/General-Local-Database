import json
import os

def writingFiles(newData):
    file_path = "DataBase.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                all_data = json.load(file)
            except json.JSONDecodeError:
                all_data = {}
    else:
        all_data = {}


    all_data.update(newData)

    with open(file_path, "w") as file:
        json.dump(all_data, file, indent=4)

    print(f"JSON file updated at {file_path}")

def readingFiles():
        file_path = "DataBase.json"
        if not os.path.exists(file_path):
             print("No database file found.")
             return {}
        
        with open(file_path, "r") as file:
             try:
                  databases = json.load(file)
             except json.JSONDecodeError:
                  print("Database file is empty or corrupted.")
                  return {}

        return databases

def deleteElement():
     file_path = "DataBase.json"

     if not os.path.exists(file_path):
          print("Database file not found")
          return
     
     with open(file_path, "r") as file:
          try:
               data = json.load(file)
          except json.JSONDecodeError:
              print("Database file is empty or corrupted.")
              return
          
     name = list(data.keys())
     if not name:
        print("No databases found.")
        return
     
     for i, dbname in enumerate(name, start=1):
        print(f"{i}. {dbname}")

     choice = input("Enter the Number of the database to delete: ")



     if choice.isdigit() and 1 <= int(choice) <= len(name):
        chosen_name = name[int(choice) - 1]
        del data[chosen_name]
        print(f"Database '{chosen_name}' deleted successfully.")
     else:
        print("Invalid choice.")
        return
     

     with open(file_path, "w") as file:
          json.dump(data, file, indent=4)