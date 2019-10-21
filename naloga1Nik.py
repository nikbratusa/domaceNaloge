import csv
import math
from itertools import combinations
import itertools


def flatten(l):
    for i in l:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i


def read_file(file_name):
    """
    Read and process data to be used for clustering.
    :param file_name: name of the file containing the data
    :return: dictionary with element names as keys and feature vectors as values
    """

    # odpiranje csv datoteke
    f = open("eurovision-final.csv", "rt", encoding="latin1")

    #stevec da v prvi vrstici dobimo samo imena drzav
    count = 0

    #slovar vseh drzav ki bo vseboval vse glasove le teh
    data = {}
    #imena vseh drzav da jih lahko v slovarju poiscemo,ko se sprehajamo čez glasove
    drzave = []
    #da bodo drzave na istih indeksih kot ocene v vrsticah,ki jih kasneje berem dodam na zacetek "prazne elemente"
    for i in range(16):
        drzave.append("Free")

    #sprehod cez vse vrstice(292),katerih dolzina je 75
    for line in csv.reader(f):

        if(count == 0):
            #potrebujemo samo imena drzav zato izberemo takšen razpon saj so na koncu se nepomembni podatki
            for i in range(16, 63):
                #dodam vse drzave na list drzav in kljuce v seznam
                drzave.append(line[i])
                data[line[i]] = []
        else:
            for j in range(16, 63):
                #dodam glasove posamezne drzave v list pod vsak ključ, če takrat država ni glasovala to označim
                if(line[j] == ""):
                    data[drzave[j]].append("NoVote")
                else:
                    data[drzave[j]].append(float(line[j]))
        #stevec povecam (samo zaradi prve vrstice)
        count = count + 1

    """
    #testni izpisi,če je vse pravilno dodano
    print(len(data))
    print(data.keys())
    print(drzave)
    print(len(drzave))
    """
    print(data["United Kingdom "])
    """
    print(len(data["Albania "]))
    """
    return data



class HierarchicalClustering:
    def __init__(self, data):
        """Initialize the clustering"""
        self.data = data
        # self.clusters stores current clustering. It starts as a list of lists
        # of single elements, but then evolves into clusterings of the type
        # [[["Albert"], [["Branka"], ["Cene"]]], [["Nika"], ["Polona"]]]
        self.clusters = [[name] for name in self.data.keys()]


    def row_distance(self, r1, r2):
        """
        Distance between two rows.
        Implement either Euclidean or Manhattan distance.
        Example call: self.row_distance("Polona", "Rajko")
        """
        #naredimo list kjer bomo shranjevali posamezne člene evklidske razdalje
        s = []

        for x, y in zip(self.data[r1], self.data[r2]):
            # pogledamo, če sta oba glasova veljavna
            if (x != "NoVote" and y != "NoVote"):
                x = float(x)
                y = float(y)
                s.append((x - y) ** 2)

        # vse clene lista sestejemo
        sumOfS = sum(s)
        #print(sumOfS)

        #na koncu se rezultat korenimo in dobimo evklidsko razdaljo
        result = math.sqrt(sumOfS)

        return result


    def cluster_distance(self, c1, c2):
        """
        Compute distance between two clusters.
        Implement either single, complete, or average linkage.
        Example call: self.cluster_distance(
            [[["Albert"], ["Branka"]], ["Cene"]],
            [["Nika"], ["Polona"]])
        """

        flatlist1 = list(flatten(c1))
        flatlist2 = list(flatten(c2))
        s = 0

        for x in flatlist1:
            for y in flatlist2:
                s = s + self.row_distance(x, y)

        s = s / (len(flatlist1) * len(flatlist2))
        #print(s)

        return s


    def closest_clusters(self):
        """
        Find a pair of closest clusters and returns the pair of clusters and
        their distance.

        Example call: self.closest_clusters(self.clusters)
        """
        #poiscemo najbljizje skupine in njihovo razdaljo,upostevamo ce je slucajno razdalja nič
        dis, pair = min((self.cluster_distance(c1, c2), (c1, c2)) for c1, c2 in combinations(self.clusters, 2) if self.cluster_distance(c1,c2) > 0)
        return dis, pair

    def run(self):
        """
        Given the data in self.data, performs hierarchical clustering.
        Can use a while loop, iteratively modify self.clusters and store
        information on which clusters were merged and what was the distance.
        Store this later information into a suitable structure to be used
        for plotting of the hierarchical clustering.
        """
        #sedaj se implementiramo algoritem za hierarhično razvrščanje v skupino, katere psevdokoda nam je bila dana
        #vsak primer ze tvori svojo skupino zato nam tega ni treba narediti tukaj

        while (len(self.clusters) != 5):

            #z naso ze napisano metodo poiscemo najblizji si skupini

            dis, pair = self.closest_clusters()
            #ju locimo vsako za sebe
            first = pair[0]
            second = pair[1]

            #ti dve skupini poiscemo med vsemi in si zapolnimo njujna indeksa
            for i in range(0, len(self.clusters)):
                if (self.clusters[i] == first):
                    firstIx = i
                elif (self.clusters[i] == second):
                    secondIx = i
                else:
                    pass


            newCluster = [self.clusters[firstIx], self.clusters[secondIx]]

            self.clusters[firstIx] = newCluster
            self.clusters.pop(secondIx)
            print(self.clusters)

        return 0

    def plot_tree(self):
            """
            Use cluster information to plot an ASCII representation of the cluster
            tree.
            """
    pass


if __name__ == "__main__":
    DATA_FILE = "eurovision-final.csv"
    hc = HierarchicalClustering(read_file(DATA_FILE))
    hc.run()
    hc.plot_tree()
