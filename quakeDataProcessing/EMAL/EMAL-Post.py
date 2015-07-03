__author__ = 'patrickczeczko'

from Bio import Entrez

dataDic = {}

def grabEntrezRecord (TaxID):
    Entrez.email = "pkczeczk@ucalgary.ca"
    handle = Entrez.efetch(db='taxonomy',id=TaxID)
    record = Entrez.read(handle)
    handle.close()

    return record[0]['LineageEx'],record[0]['ScientificName']

def processCSV (file):
    inputFile = open(file,'r')
    for i,line in enumerate(inputFile):
        if i != 0:
            parse = line.split(',')
            TaxID = parse[1]
            print(i,TaxID)
            lineage,species = grabEntrezRecord(TaxID)

            noRank = False

            superKingdom = ['Superkingdom',None,None]
            Q1 = ['Q1',None,None]
            Order = ['Order',None,None]
            Family = ['Family',None,None]
            Genus = ['Genus',None,None]

            for entry in lineage:
                if entry['Rank'] == 'superkingdom':
                    superKingdom[1] = entry['ScientificName']
                    superKingdom[2] = entry['TaxId']
                elif entry['Rank'] == 'no rank' and noRank == False:
                    Q1[1] = entry['ScientificName']
                    Q1[2] = entry['TaxId']
                    noRank = True
                elif entry['Rank'] == 'order':
                    Order[1] = entry['ScientificName']
                    Order[2] = entry['TaxId']
                elif entry['Rank'] == 'family':
                    Family[1] = entry['ScientificName']
                    Family[2] = entry['TaxId']
                elif entry['Rank'] == 'genus':
                    Genus[1] = entry['ScientificName']
                    Genus[2] = entry['TaxId']

            dataDic[TaxID] = [parse[2], species, superKingdom, Q1, Order, Family, Genus]

            print(dataDic[TaxID])

processCSV("/Users/patrickczeczko/GithubRepos/viral-metagen/quakeData/EMALResult/MPT0.25.csv")
