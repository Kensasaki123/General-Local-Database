import Write

DataList = {}

def main():
  process1()

def process1():
   

   while True:

      print("********Database Module********")
      print("1. Create a Database")
      print("2. Retrive Data from a Database")
      print("3. Delete a Database")
      print("4. Edit the Database")
      print("5. Exit the system")  
      option = input("Your choice, choose the respected number: ")
      if(option == "1"):
         nameDb, structured_columns, structured_rows = createDatabase()
         if nameDb and structured_columns and structured_rows:
          print(nameDb, structured_columns, structured_rows)
         TempDataList = {}

         TempDataList[nameDb] = {
            "columns": structured_columns,
            "rows": structured_rows
         }
         DataList[nameDb] = {
            "columns": structured_columns,
            "rows": structured_rows
         }
         Write.writingFiles(TempDataList)

      elif(option == "2"):
         retriveDatabase()
      elif(option == "3"):
         DeleteDatabase()
      elif(option == "4"):
         EditDatabase()
      elif(option == "5"):
         ExitSys()

def createDatabase():
 while True:
   print("Name of the DataBase")
   nameDb = input("= ")
   print("No. of Rows:")
   
   while True:
      row_input = (input("= "))
      if not row_input.isdigit():
         print("Invalid input! Please enter a number for rows.")
         continue
      intdbRow = int(row_input)
      break
   
   while True:
      print("No. of Columns:")
      raw_column = (input("= "))
      if not raw_column.isdigit():
         print("Invalid input! Please enter a number for columns.")
         continue
      intdbColumn = int(raw_column)  
      break
   
   structured_columns = [] 

   for i in range(intdbColumn):
     col_name = input(f"Column {i+1} name:")
     structured_columns.append(col_name)

   structured_rows = []
   
   for i in range(intdbRow):
        row_data = {}
        for j in range(intdbColumn):
            key = structured_columns[j]
            value = input(f"Enter value for Row {i+1}, column '{key}': ")
            row_data[key] = value
        structured_rows.append(row_data.copy())

   print(f"Strcutured Data in `{nameDb}:")
   for i, row in enumerate(structured_rows):
      print(f"Row {i+1}: {row}")

   print(f"Database `{nameDb}` created.\n")
   return nameDb, structured_columns, structured_rows

def retriveDatabase():
   data = Write.readingFiles()
   
   names = list(data.keys())

   print("Available DataBases:")
   for idx, name in enumerate(names, start=1):
      print(f"{idx}. {name}")

   choice = input("Enter the number of the database to retrieve: ")

   if choice.isdigit() and 1 <= int(choice) <= len(names):
      chosen_name = names[int(choice) - 1]
      db = data[chosen_name]
      print(f"\nDatabases: {chosen_name}")
      print(f"Columns: {db['columns']}")
      for i, row in enumerate(db["rows"]):
         print(f"Row {i+1}: {row}")
   else:
      print("Invalid choice.")

def DeleteDatabase():
   Write.deleteElement()

def EditDatabase():
  print

def ExitSys():
   return
   

if __name__ == "__main__":
    main()