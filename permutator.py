from nltk.tree import *
import json
source = ("(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS restaurants) ) ) ) ) ) ) )")

class Permutator:
    results = set() 
    nps = []
    def __init__(self, source, limit=20) -> None:
        self.tree = ParentedTree.fromstring(source)
        self.limit = limit

    #Collect array of arrays with all children NPs and their parent just in case for future
    def traverse(self, root):
        if len(root) == 0:
            return
        level = []
        for node in root:
            if type(node) == ParentedTree:
                if node.label() == "NP":
                    level.append(node.treeposition())       
                self.traverse(node)
        if len(level) > 1:
            self.nps.append(level)

    #Helper function to swap two nodes on a tree
    def swap_nodes(self, node1, node2):
        #Have to use temp trees to avoid "Can not insert a subtree that already has a parent." value error
        temp1 = self.tree[node1].copy(deep=True)
        temp2 = self.tree[node2].copy(deep=True)
        self.tree[node1] = temp2
        self.tree[node2] = temp1

    #Recursive backtracking algorithm to find permutations in a group of NPs 
    def permutateNPs(self, group, start, end, subgroup=None):
        if len(self.results) >= self.limit:
            return
        if start == end:
            if subgroup:
                self.permutateNPs(subgroup, 0, len(subgroup))
                    
            self.results.add(self.tree._pformat_flat("", "()", False))
        else:
            for i in range(start, end):
                first = group[i]
                second = group[start]
                if first != second:
                    self.swap_nodes(first, second)
                first, second = second, first    
                self.permutateNPs(group, start+1, end, subgroup=subgroup)
                if first != second:
                    self.swap_nodes(first, second)
                first, second = second, first
                
    #Return a set of all possible permutations of separate permutations
    def permutate_tree(self):
        self.traverse(self.tree)
        for i,group in enumerate(self.nps):
            for j in range(i+1,len(self.nps)):
                group2 = self.nps[j]
                self.permutateNPs(group, 0, len(group), subgroup=group2)
    
    def seralize_permutations(self):
        return([{"tree": x} for x in self.results])


perm = Permutator(source)
perm.permutate_tree()
trees_json = perm.seralize_permutations()
with open('results.json', 'w') as json_file:
  json.dump(trees_json, json_file)



 


    

