import csv
csvfile = open("test.csv", newline='')
reader = csv.DictReader(csvfile)
set = {}

phraseTag, intentTag, ticketTag = reader.fieldnames[0], reader.fieldnames[2], reader.fieldnames[1]
# Si suppone che il file ha nella prima colonna la frase e nella seconda l'intent

for row in reader:
    if row[intentTag] not in set: set[row[intentTag]] = []
    set[row[intentTag]].append({"phrase": row[phraseTag], "ticketTag": row[ticketTag], "intentTag": row[intentTag]})

for intent in set:
    #print(set[intent])
    defTicket = set[intent][0]["ticketTag"]
    print("Checking "+intent)
    for row in set[intent]:
        #print(row)
        if row["ticketTag"] != defTicket:
            print("\t|Intent: "+row["intentTag"]+"\tDefault ticket: "+defTicket+"  Actual ticket: "+row["ticketTag"]+"\tPhrase: "+row["phrase"])
    print("-"*130)
