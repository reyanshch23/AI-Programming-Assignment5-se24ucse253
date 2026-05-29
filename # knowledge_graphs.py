# knowledge_graphs.py
# Demonstrates building a simple Knowledge Graph in Python using a dict-based
# triple store, and shows how RDFLib (a standard Python KG library) works.

# -------------------------------------------------------
# SECTION 1: What is a Knowledge Graph?
# -------------------------------------------------------
# A Knowledge Graph (KG) represents knowledge as a set of triples:
#   (Subject, Predicate, Object)
# e.g. ("Paris", "isCapitalOf", "France")
#       ("Paris", "locatedIn", "Europe")
#
# Popular tools for KGs:
#   - RDFLib       : Python library for RDF graphs (W3C standard)
#   - Neo4j        : Graph database with Cypher query language
#   - Protege      : GUI tool to build OWL ontologies
#   - Apache Jena  : Java framework for semantic web
#   - Wikidata     : Open KG with SPARQL endpoint
#   - GraphDB      : Enterprise triple store
#
# Common formats: RDF/XML, Turtle (.ttl), JSON-LD, N-Triples
# -------------------------------------------------------

# -------------------------------------------------------
# SECTION 2: Build a simple KG manually (no external libs)
# -------------------------------------------------------

class SimpleKG:
    """
    Triple store: stores (subject, predicate, object) triples.
    Supports basic querying.
    """
    def __init__(self):
        self.triples = []

    def add(self, subject, predicate, obj):
        self.triples.append((subject, predicate, obj))

    def query(self, subject=None, predicate=None, obj=None):
        results = []
        for s, p, o in self.triples:
            if (subject is None or s == subject) and \
               (predicate is None or p == predicate) and \
               (obj is None or o == obj):
                results.append((s, p, o))
        return results

    def print_all(self):
        print("Knowledge Graph Triples:")
        for s, p, o in self.triples:
            print(f"  ({s}, {p}, {o})")

def build_travel_kg():
    kg = SimpleKG()

    # Places
    kg.add("Paris", "isA", "City")
    kg.add("Paris", "locatedIn", "France")
    kg.add("Paris", "locatedIn", "Europe")
    kg.add("Paris", "hasAttraction", "EiffelTower")
    kg.add("Paris", "hasAttraction", "Louvre")
    kg.add("EiffelTower", "isA", "Landmark")
    kg.add("EiffelTower", "builtIn", "1889")

    kg.add("Kyoto", "isA", "City")
    kg.add("Kyoto", "locatedIn", "Japan")
    kg.add("Kyoto", "locatedIn", "Asia")
    kg.add("Kyoto", "hasAttraction", "FushimiInari")
    kg.add("FushimiInari", "isA", "Temple")

    # Food
    kg.add("Crepes", "isA", "Food")
    kg.add("Crepes", "originatesFrom", "France")
    kg.add("Paris", "hasCuisine", "Crepes")
    kg.add("Matcha", "isA", "Food")
    kg.add("Kyoto", "hasCuisine", "Matcha")

    # Costs
    kg.add("Paris", "avgDailyCostUSD", "200")
    kg.add("Kyoto", "avgDailyCostUSD", "150")

    return kg

def demo_kg():
    print("===== Knowledge Graph Demo =====\n")
    kg = build_travel_kg()
    kg.print_all()

    print("\n--- Query: All attractions in Paris ---")
    results = kg.query(subject="Paris", predicate="hasAttraction")
    for r in results:
        print(" ", r)

    print("\n--- Query: What is FushimiInari? ---")
    results = kg.query(subject="FushimiInari", predicate="isA")
    for r in results:
        print(" ", r)

    print("\n--- Query: What cities are in Europe? ---")
    results = kg.query(predicate="locatedIn", obj="Europe")
    for r in results:
        print(f"  {r[0]} is located in Europe")

    print("\n--- Query: All foods and their origins ---")
    results = kg.query(predicate="originatesFrom")
    for r in results:
        print(f"  {r[0]} originates from {r[2]}")

# -------------------------------------------------------
# SECTION 3: Equivalent RDFLib code (standard library)
# Shows how this maps to real KG tools
# -------------------------------------------------------

RDFLIB_EXAMPLE = """
# This is how the same KG would be built with RDFLib:

from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS

EX = Namespace("http://example.org/travel#")
g = Graph()

g.add((EX.Paris, RDF.type, EX.City))
g.add((EX.Paris, EX.locatedIn, EX.France))
g.add((EX.Paris, EX.hasAttraction, EX.EiffelTower))
g.add((EX.EiffelTower, RDF.type, EX.Landmark))

# SPARQL query
result = g.query('''
    SELECT ?city ?attraction WHERE {
        ?city <http://example.org/travel#hasAttraction> ?attraction .
    }
''')
for row in result:
    print(row)

# Save as Turtle format
g.serialize("travel_kg.ttl", format="turtle")
"""

if __name__ == '__main__':
    demo_kg()
    print("\n===== Equivalent RDFLib code =====")
    print(RDFLIB_EXAMPLE)
    print("\nTools summary:")
    tools = [
        ("RDFLib",     "Python library", "SPARQL queries, RDF/OWL",      "pip install rdflib"),
        ("Neo4j",      "Graph DB",       "Cypher queries, visualization", "neo4j.com"),
        ("Protege",    "GUI editor",     "OWL ontologies, reasoning",     "protege.stanford.edu"),
        ("Apache Jena","Java framework", "Inference, SPARQL",             "jena.apache.org"),
        ("Wikidata",   "Open KG",        "Public knowledge, SPARQL",      "query.wikidata.org"),
    ]
    print(f"{'Tool':<15} {'Type':<15} {'Features':<35} {'Access'}")
    print("-" * 80)
    for t in tools:
        print(f"{t[0]:<15} {t[1]:<15} {t[2]:<35} {t[3]}")