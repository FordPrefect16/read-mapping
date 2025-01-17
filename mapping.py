import time

def getGenome(file):                                    #return sequences and description from fasta file (input .fasta)
                                                        #returns array of array
    from Bio import SeqIO                                   #load SeqIO from Biopython package
    sequences = []                                          #create empty array for for-loop
    descriptions = []                                       #create empty array for for-loop
    for record in SeqIO.parse(file, "fasta"):               #loop through all entries in source file and store sequences and descriptions
        seq = record.seq
        des = record.description
        sequences.append(seq)
        descriptions.append(des)
    return(sequences, descriptions)


def getReads(file):                                     #return reads to map from source file as array (input preferably txt)
    reads = []
    with open(file) as read:
        for line in read.readlines():
            if "A" in line or "T" in line or "C" in line or "G" in line: #check if read or number, ignore numbering
                line = line[:-1]
                reads.append(line)
    read.close()
    return (reads)

def compStrand(sequence):                               #returns the complementary string of entered sequence as string
    sequence.upper()
    c = str()
    cStrand = str()
    bases = {                                               #create dict to check complementary bases
        "A":"T",
        "T":"A",
        "U":"A",
        "C":"G",
        "G":"C"
    }
    l = len(sequence)
    for i in range(l):                                      #loop through sequence and find complementary base, store in c
        s = sequence[i]
        if s in bases:
            c = bases[s]
            if s == "U":                                    #check if RNA sequence
                print("Sequence contains Uracil - complementary: A - RNA molecule?")
        if s not in bases:                                  #check for non-existing base
            c = "X"
            print("Position", i,"not a base, X added - please revise")
        cStrand += c                                        #add c to return string
    return(cStrand[::-1])                                   #output reverse complementary sequence



def Barplot(gotReads, mappedGenome, gotGenome, path):             #create a bar plot showing occurrence for all reads for each genome; input return from getReads, mapGenome and getGenome
    import matplotlib.pyplot as plt
    from datetime import datetime
    number = []
    l = len(gotGenome[1])
    for i in range(l):
        for entry in gotReads:
            m = mappedGenome[gotGenome[1][i], entry]
            number.append(len(m))
        fileName = str(path)+ "/"+str(datetime.today().strftime('%Y-%m-%d_'))+ str(gotGenome[1][i]) + ".png"
        plt.bar(range(len(number)), number)
        plt.xlabel("Read Number in File")
        plt.ylabel("Occurrences in Genome")
        plt.savefig(fileName)
        plt.clf()
    print("Boxplot created!")

def MapSummary(gotReads, mappedGenome, gotGenome, path):          #create a summary after the genome is mapped in a txt file for each genome; input return from getReads, mapGenome and getGenome
    from datetime import datetime
    summary = {}
    l = len(gotGenome[1])
    for i in range(l):
        fileName = str(path)+ "/" +str(datetime.today().strftime('%Y-%m-%d_'))+ str(gotGenome[1][i]) +".csv"            #create file name for current genome from fasta description
        for Read in gotReads:
            summary[Read] = mappedGenome[gotGenome[1][i], Read]      #create dictionary for read and positions (array)
        f = open(fileName, "w")                                     #create file
        f.write("Read; Forward Start 5' -> 3'; Reverse Start 5' -> 3'; Number of Hits \n")
        for element in summary:
            f.write(element)                                        #write read
            f.write("; ")
            f.write(", ".join(str(x) for x in summary[element][0]))    #write forward positions, separated by ";"
            f.write("; ")
            f.write(", ".join(str(x) for x in summary[element][1]))    #write backward positions, separated by ";"
            f.write("; [")
            f.write(str(len(summary[element])))                     #write number of found positions
            f.write("]")
            f.write("\n")
        f.close()                                                   #close and save
        summary = {}                                                #empty dictionary for next genome


def mapGenome(G_file, R_file, path ="."):                                      #return dictionary with genome description and read as key and starting positions in genome as value (returns list of list
    start = time.time()
    import re                                                       #use re for easier iterate search
    Genomes = getGenome(G_file)                                     #store sequences and description from fasta files (input .fasta)
    print("Finished evaluating 'getGenomes'!")
    Reads = getReads(R_file)                                        #store reads to map from source file as array (input preferably txt)
    print("Finished evaluating 'getReads'!")
    mapped = {}                                                     #create dictionary for output
    g = 0                                                           #
    for genome in Genomes[0]:
        Gen = Genomes[1][g]
        g = +1
        genome = str(genome)
        compgenome = compStrand(genome)
        for read in Reads:
            posFor = [i.start() for i in re.finditer(read, genome)]
            posRev = [i.start() for i in re.finditer(read, compgenome)]
            posOut = [posFor, posRev]
            mapped[Gen,read] = posOut
    print("Finished mapping reads!")
    #Barplot(Reads,mapped, Genomes, path)
    MapSummary(Reads,mapped, Genomes, path)
    end = time.time()
    print("Finished running code in",round(end-start),"s!")
    return(mapped)

#call

mapGenome("data/Ecoli_genome.fasta", "data/reads_new.fasta")
