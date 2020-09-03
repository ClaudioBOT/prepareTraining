import csv, random

def getSetFromCSV(fileName):
    csvfile = open(fileName + ".csv", newline='')
    reader = csv.DictReader(csvfile)
    set = {}

    if (len(reader.fieldnames) != 2):
        print("La tabella ha un numero di colonne diverso da 2")
        return set
    phraseTag, intentTag = reader.fieldnames[0], reader.fieldnames[1]
    # Si suppone che il file ha nella prima colonna la frase e nella seconda l'intent

    for row in reader:
        if row[intentTag] not in set: set[row[intentTag]] = []
        set[row[intentTag]].append(row[phraseTag])
    return set

def exportCSV(fileName, set, phraseTag, intentTag):
    csvfile = open(fileName + ".csv", "w+")
    writer = csv.DictWriter(csvfile, fieldnames = [phraseTag, intentTag])
    for intent in set:
        for phrase in set[intent]:
            writer.writerow({phraseTag: phrase, intentTag: intent})

def popRandom(list):
    if (len(list)>0):
        return list.pop(random.randint(0,len(list)-1))

def prepareTraining(dataFile, min, max, perc):
    
    # Importo il set
    # Si suppone che il file ha nella prima colonna la frase e nella seconda l'intent
    train_set = getSetFromCSV(dataFile)
    test_set = {}

    remove_set =[]

    for intent in train_set:
        # Taglio l'intent tra il min e il max
        intLen = len(train_set[intent])
        if intLen < min :
            remove_set.append(intent)
        elif intLen > max :
            for _ in range(0, intLen - max): popRandom(train_set[intent])

    for elem in remove_set: train_set.pop(elem) # Elimino intent senza sufficenti esempi

    # Divido l'intent nei 2 set secondo perc
    for intent in train_set:
        intLen = len(train_set[intent])
        test_set[intent] = []
        for _ in range(0, int((intLen/100)*perc)):
            test_set[intent].append(popRandom(train_set[intent]))

    # Esporto i 2 set in formato csv
    exportCSV("test_set", test_set, 'COLUMN1', 'COLUMN2')
    exportCSV("train_set", train_set, 'COLUMN1', 'COLUMN2')

    # Stampo le statistiche
    print("-"*57)
    print(f"|        The files has {len(train_set)} intent in the criteria:        |")
    for intent in train_set:
        print(f"| {intent}:\t tot:{len(train_set[intent])+len(test_set[intent])}\ttrain:{len(train_set[intent])}\ttest:{len(test_set[intent])} |")
    print("-"*57)


if __name__ == "__main__":
    dataFile = "data"
    min = 100
    max = 110
    perc = 30
    prepareTraining(dataFile, min, max, perc)
else:
    print("Hi! To use the library launch prepareTraining with the source file name, the min and number of exeamples and the prec between test set and train set")
    print(f'Like {__name__}.prepareTraining("data", 100, 110, 30)')
