import csv
import math
from itertools import combinations



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
    f = open("eurovision-finals-1975-2019.csv", "rt", encoding="utf8")
    count = 0
    data = {}
    allCountriesVoting = []

    with open("eurovision-finals-1975-2019.csv", "rt", encoding="utf8") as voting:
        reader = csv.reader(voting, delimiter=',')
        votes = list(reader)

    for l in votes:
        if count == 0:
            count += 1
        else:
            if l[2] not in allCountriesVoting:
                allCountriesVoting.append(l[2])
                data[l[2]] = []


    for country in data.keys():
        indexCountry = allCountriesVoting.index(country)
        for i in range(len(allCountriesVoting)):
            if i == indexCountry:
                data[country].append("NoVote")
            else:
                sum = 0
                divider = 0
                for l in votes:
                    if l[2] == country and l[3] == allCountriesVoting[i]:
                        sum += float(l[4])
                        divider += 1
                if divider == 0:
                    data[country].append("NoVote")
                else:
                    res = sum/divider
                    data[country].append(res)

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
        firstRow = self.data[r1]
        secondRow = self.data[r2]
        sum = 0

        for f, s in zip(firstRow, secondRow):
            if (f != "NoVote" and s != "NoVote"):
                x = (f - s) ** 2
                sum = sum + x

        result = math.sqrt(sum)

        return result

    def cluster_distance(self, c1, c2):
        """
        Compute distance between two clusters.
        Implement either single, complete, or average linkage.
        Example call: self.cluster_distance(
            [[["Albert"], ["Branka"]], ["Cene"]],
            [["Nika"], ["Polona"]])
        """
        firstCluster = list(flatten(c1))
        secondCluster = list(flatten(c2))
        sum = 0
        dolzina = len(firstCluster) * len(secondCluster)


        for f in firstCluster:
            for s in secondCluster:
                sum += self.row_distance(f, s)
                """
                distance = self.row_distance(f,s)
                if counter == 0:
                    minDistance = distance
                    counter += 1
                elif distance < minDistance:
                    minDistance = distance
                """
        result = sum / dolzina

        return result

    def closest_clusters(self):
        """
        Find a pair of closest clusters and returns the pair of clusters and
        their distance.

        Example call: self.closest_clusters(self.clusters)
        """
        dis, pair = min((self.cluster_distance(c1, c2), (c1, c2)) for c1, c2 in combinations(self.clusters, 2) if
                        self.cluster_distance(c1, c2) > 0)
        return dis, pair

    def run(self):
        """
        Given the data in self.data, performs hierarchical clustering.
        Can use a while loop, iteratively modify self.clusters and store
        information on which clusters were merged and what was the distance.
        Store this later information into a suitable structure to be used
        for plotting of the hierarchical clustering.
        """
        # 1.vsak primer naj tvori svojo skupino - to storimo že pri inicializaciji

        # 2.ponavljaj, dokler ne ostane ena sama skupina
        while(len(self.clusters) != 2):
            # 3.poisci najblizji si skupini
            distance, closestClusters = self.closest_clusters()

            # 4. zdruzi skupini Ca in Cb v skupino Cab
            newCluster = [closestClusters[0], closestClusters[1]]

            # 5. nadomesti skupini Ca in Cb s skupino Cab
            self.clusters.remove(closestClusters[0])
            self.clusters.remove(closestClusters[1])
            self.clusters.append(newCluster)

        print(self.clusters)


        allCountriesVoting = list(self.data.keys())
        for country in allCountriesVoting:
            noVotes = []
            votes = []
            c = list(self.data[country])
            #print("---------------------------------")
            #print(country + ":")
            for i in range(len(c)):
                if c[i] == "NoVote" or float(c[i]) == 0.0:
                    if allCountriesVoting[i] not in noVotes:
                        noVotes.append(allCountriesVoting[i])
                else:
                    if float(c[i]) > 6:
                        if allCountriesVoting[i] not in votes:
                            votes.append(allCountriesVoting[i])
            #print(noVotes)
            #print(votes)



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
