import os, csv

location = "New_Cards/" #change this name to location of new card images. You will need to add these images to the Cards folder once changed
filename=""
csv_output=" New_Card_Names.csv" #this allows you to copy/paste the new card filenames into the Keyforge_Cards.csv and create a new dictonary from them
output=[]
files = os.listdir(location)
k=0

old=["Woe_","_",".jpg"] #replace the strings in this list --->
replaced=["","-",".png"] #with the strings in this list

for i in range(len(files)):
    filename=files[i]
    for j in range(len(old)):
        filename=filename.replace(old[j],replaced[j])
    filename=filename.lower()
    os.rename(location+files[i],location+filename)
    print(filename)
    output.append(filename)

with open(csv_output, 'w', newline="") as f:
    writer =csv.writer(f)
    for item in output:
        if item != "":
            item=item.replace(".png","")
            writer.writerow([item])
    f.close()
