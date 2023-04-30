from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nltk.tree import *

from django.shortcuts import render
from django.views.generic import TemplateView

# Endpoint returns all possible permutations of NPs in the tree (up to a maximum specified with the 'limit' url param, default is 20)
class NP_paraphrase(APIView):   
    #Initialize values
    source = ''
    nps = []
    results = set()
    maxResults = 0 

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
    def swap_nodes(self, tree, node1, node2):
        #Have to use temp trees to avoid "Can not insert a subtree that already has a parent." value error
        temp1 = tree[node1].copy(deep=True)
        temp2 = tree[node2].copy(deep=True)
        tree[node1] = temp2
        tree[node2] = temp1

    #Recursive backtracking algorithm to find permutations in a group of NPs 
    def permutateNPs(self, tree, group, start, end, subgroup=None):
        if len(self.results) == self.maxResults:
            return
        if start == end:
            if subgroup:
                self.permutateNPs(tree, subgroup, 0, len(subgroup))
                    
            self.results.add(tree._pformat_flat("", "()", False))
        else:
            for i in range(start, end):
                first = group[i]
                second = group[start]
                if first != second:
                    self.swap_nodes(tree, first, second)
                first, second = second, first    
                self.permutateNPs(tree, group, start+1, end, subgroup=subgroup)
                if first != second:
                    self.swap_nodes(tree, first, second)
                first, second = second, first
                
    #Return a set of possible permutations of separate permutations
    def permutate_tree(self, tree):
        self.traverse(tree)
        for i,group in enumerate(self.nps):
            for j in range(i+1,len(self.nps)):
                group2 = self.nps[j]
                self.permutateNPs(tree, group, 0, len(group), subgroup=group2)
    
    #Put results in a JSON frienly list of dictonaries
    def seralize_permutations(self):
        return([{"tree": x} for x in self.results])

    def get (self, request, format=None):

        #Resetting between separate API calls.
        self.results = set()
        self.nps = [] 

        self.source = request.GET['tree']
        self.maxResults = int(request.GET.get('limit', 20))
        
        try:
            tree = ParentedTree.fromstring(self.source)
        except Exception:
            return Response({"error": "Bad tree formating"}, status=status.HTTP_400_BAD_REQUEST)
        
        self.traverse(tree)            
        self.permutate_tree(tree)

        if len(self.results) == 0:
            return Response({"error": "Sentence has no extra permutation"}, status=status.HTTP_202_ACCEPTED)
        
        trees_json = self.seralize_permutations()
        return Response(trees_json, status=status.HTTP_200_OK)

#Simple template form for testing
class testing_view(TemplateView):
    template_name="drf_endpoints/index.html"
    def get(self, request):
        return render(request, self.template_name)



