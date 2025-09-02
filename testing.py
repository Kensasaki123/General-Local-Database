import Write

data = Write.readingFiles()

names = list(data.keys())
print(names)
        
for idx, name in enumerate(names, start=1):
            print(f"{idx} : {name}")

choice = 1
if 1 <= choice <= len(names): 
        final_choice = names[int(choice) - 1]
        database_data = data[final_choice]
        
print(database_data)
