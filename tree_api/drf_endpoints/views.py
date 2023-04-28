from rest_framework.views import APIView
from rest_framework.response import Response
from nltk.tree import *

def extract_np(psent):
    for subtree in psent.subtrees():
        if subtree.label() == 'NP':
            yield ' '.join(word for word, tag in subtree.leaves())

class NP_phrase (APIView):
    # Endpoint returns all possible permutations of NPs in the tree (up to a maximum specified with the 'limit' url param, default is 20)



    def get (self, request, format=None):
        tree = self.request.query_params.get('tree')
        limit = self.request.query_params.get('limit')
        tree2 = Tree.fromstring(tree)

        return Response(f'{tree2}')


