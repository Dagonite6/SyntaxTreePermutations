# SyntaxTreePermutations
## Django API that returns all possible permutations of NPs in a parsed syntax tree.
​

### Root folder also has:

​
`permutator.py` a class-based implementation of the algorithm used inside of the `NP_paraphrase` Django view, for possible future separate use.


`results.json` an example of a response returned by the API endpoint.

​
## Instalation:
1. Clone repo.

2. Install Python venv and activate the new environment:

```    

pip install virtualenv

virtualenv venv

source venv/bin/activate

```    

    
3. Install prerequisites:  ```pip install -r requirements.txt```

4. Navigate into tree_api and run the django project: ```python manage.py runserver```


## Usage:


   API endpoint, returns all possible permutations of NPs in the tree (up to a maximum specified with the 'limit' url param):
```
path: 127.0.0.1:8000/api/paraphrase/

HTTP method: GET
query parameters:

tree: str (required)

limit: int (optional, default: 20)

```

Testing UI (sends GET requests from form data, prints returned JSON onto the page):

```
path: http://127.0.0.1:8000/api/paraphrase/testing/
```