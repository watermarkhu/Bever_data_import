# -*- coding: utf-8 -*-
import pandas as pd

print("\n\n____________________________________________________________________________")

# Vraag naar namen van bestanden
fname = input("Naam csv-bestand features (zonder '.csv'): ")
ename = input("Naam csv-bestand errors (zonder '.csv'): ")
tname = input("Naam csv-bestand text (zonder '.csv') [enter to skip]: ")

# Als textbestand bestaat, voeg error features to aan technical desciption
if tname != "":
    print("\nText bestand toevoegd. Begin handmatig toevoegen van extra Technical description. \
    \nVoor elke error worden de bijhorende Product Code, Feature Code, en Feature Setting afgedrukt. \
    \nTyp dan de extra Technical description, en druk op enter om door te gaan.\
    \nDruk meteen op enter om te skippen. \
    \nEindig met // om ook de feature setting te veranderen.\
    \nDruk 2x op control-C om de script te onderbreken. Druk dus maar 1 keer om te kopieren.")

    # Lees text bestand uit naar pandas dataframes
    tlist = pd.read_csv(tname + ".csv", sep = ";", encoding ="ISO-8859-1")

# Lees de bestanden naar pandas dataframes
flist = pd.read_csv(fname + ".csv", sep = ";", encoding = "ISO-8859-1")
elist = pd.read_csv(ename + ".csv", sep = ";", encoding = "ISO-8859-1")
elen = elist.shape[0]

# Loop over alle errors om daar langs te gaan
errorrows = []
for ei, row in elist.iterrows():
    ePC = str(elist.loc[ei,"Product Code"])
    eFC = str(elist.loc[ei,"Feature Code"])
    efs = str(elist.loc[ei,"feature_setting"])
    eEr = str(elist.loc[ei,"Errors"])
    if ePC == "nan": ePC = ""
    if eFC == "nan": eFC = ""
    if efs == "nan": efs = ""
    if eEr == "nan": eEr = ""

    # Zoek naar rownumbers in features die errors bevatten
    for fi, row in flist.iterrows():
        fPC = str(flist.loc[fi,"PRODUCT_CODE"])
        fFC = str(flist.loc[fi,"FEATURE_CODE"])
        if fPC == "nan": fPC = ""
        if fFC == "nan": fFC = ""

        if (ePC == fPC) & (eFC == fFC):
            if fi not in errorrows:
                errorrows.append(fi)
                break

    # Zoeken naar desbetreffende product in text bestand
    if tname !="":
        for ti, row in tlist.iterrows():
            tPC = str(tlist.loc[ti,"Product Code"])
            tTd = str(tlist.loc[ti,"Technical description draft NL"])
            tWN = str(tlist.loc[ti,"Web Name NL"])
            if tPC == "nan": tPC = ""
            if tTd == "nan": tTd = ""
            if tWN == "nan": tWN = ""

            if ePC == tPC:
                # Print de error voor de gebruiker
                print("\n\n\nError "+str(ei+1)+"/"+str(elen) + \
                ": " + ePC + " " + tWN + ": " + eFC + ": " + efs)
                print("\n"+eEr)
                nTd = str(tTd[:])
                # Verwijder laatste enter indien van toepassing
                if nTd != "" and nTd[len(nTd)-1] == "\n":
                    nTd = nTd[:len(nTd)-1]
                # Laat de gebruiker nieuwe regel TD toevoegen
                print("\nHuidige Technical description:\n" + tTd)
                aTd = input("\nExtra desciption: ")
                # Skip functie als error niet nodig als TD
                if aTd != "":
                    if aTd[-2:] == "//":
                        newcode = input("\nNew Product Code (enter for "+eFC+"): ")
                        aTd = aTd[:-2]
                        newsetting = input("\nNew feature setting: ")

                        flist.at[fi,"FEATURE_SETTING"] = newsetting
                        errorrows = errorrows[:-1]
                        if newcode != "":
                            flist.at[fi,"FEATURE_CODE"] = newcode
                    nTd += "\n" + aTd
                    tlist.at[ti, "Technical description draft NL"] = nTd
                print("____________________________________________________________________________")

# Verwijder feature op basis van de rownumbers
if len(errorrows) != 0:
    len_before = flist.shape[0]
    flist.drop(sorted(errorrows), inplace=True)
    len_after = flist.shape[0]
    len_removed = len_before - len_after

    # Exporteer nieuw features bestand
    flist.to_csv(fname +"_noerror.csv", sep=";", index=False, encoding ="ISO-8859-1")

    # Maak rapport aan over verwijderde features
    print("\n"+ str(len_removed) + " entries removed of "
        + str(elist.shape[0]) + " errors." )
elif len(errorrows) != elist.shape(0):
    print("Something probably went wrong...")
else:
    print("No corresponding errors found")

if tname != "":
    # Verwijder alle laatste enters in TD
    for ti, row in tlist.iterrows():
        tTd = str(tlist.loc[ti,"Technical description draft NL"])
        if tTd != "" and tTd[len(tTd)-1] == "\n":
            tlist.at[ti, "Technical description draft NL"] = tTd[:len(tTd)-1]

    # Exporteer nieuw text bestand
    tlist.to_csv(tname +"_added.csv", sep=";", index=False, encoding ="ISO-8859-1")

# Eindbericht
print("\nKlaar met scipt, bestanden staan klaar in de folder voor import.\
\n____________________________________________________________________________\n\n")
