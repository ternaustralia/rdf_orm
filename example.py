from typing import List, Union

from rdf_orm import RDFModel, MapTo
from rdflib import Literal, URIRef, Namespace, Graph
from rdflib.namespace import OWL, RDFS, RDF

MyOntology = Namespace('https://example.com/')


# Create your models by subclassing RDFModel from rdf_orm.
class Price(RDFModel):
    # Set the class URI type of the model.
    class_uri = MyOntology.Price

    # Mapping dictionary to define how the class attributes are
    # mapped to RDF properties.
    mapping = {
        'currency': MyOntology.hasCurrency,
        'value': RDF.value
    }

    # Use Python type hints to state what the type is for attributes.
    # The below two lines are optional but recommended as it allows
    # IDEs to provide type hints.

    # We don't set a uri attribute on purpose on this Price class in the constructor.
    # The rdf_orm RDFModel will see this and generate a blank node for any relationships pointing to this object.
    currency: Literal
    value: Literal

    def __init__(self, currency: Literal, value: Literal):
        # Call the base class constructor
        super(Price, self).__init__()
        # Call the base class method and pass in the local variables of the
        # current scope and assign it to self.
        self.assign_constructor_vars(locals())


class Item(RDFModel):
    class_uri = MyOntology.Item

    mapping = {
        'label': RDFS.label,
        'price': MyOntology.hasPrice
    }

    uri: URIRef
    label: Literal
    price: Price

    def __init__(self, uri: URIRef, label: Literal, price: Price):
        super(Item, self).__init__()
        self.assign_constructor_vars(locals())


class OWLClass(RDFModel):
    class_uri = OWL.Class

    mapping = {
        'label': RDFS.label,
        # Use the MapTo class to define bidirectional relationships between individuals.
        'items': MapTo(MyOntology.hasItem, MyOntology.isItemOf)
    }

    uri: URIRef
    label: Literal
    # Use Python type hints to express attributes as lists of things.
    # In this case, 'items' is a list of Item or URIRef objects.
    items: List[Union[Item, URIRef]] = None

    def __init__(self, uri: URIRef, label: Literal, items: List[Union[Item, URIRef]] = None):
        super(OWLClass, self).__init__()
        self.assign_constructor_vars(locals())


if __name__ == '__main__':
    # Create a 'global' graph object. We will use this to store the generated data from rdf_orm models.
    g = Graph()

    # Create an instance of the OWLClass model with a list of items.
    individual = OWLClass(
        URIRef('individual-1'),
        Literal('Individual 1'),
        items=[Item(
            URIRef('item-1'),
            Literal('item 1'),
            Price(
                Literal('usd'),
                Literal(15))
        )]
    )

    # Modify the label.
    individual.label = Literal('Individual 1 modified')

    # Create some more standalone items.
    item_two = Item(
        URIRef('item-2'),
        Literal('item 2'),
        Price(
            Literal('aud'),
            Literal(5)
        ))
    item_three = Item(
        URIRef('item-3'),
        Literal('item 3'),
        Price(
            Literal('usd'),
            Literal(11)
        ))
    item_four = Item(
        URIRef('item-4'),
        Literal('item 4'),
        Price(
            Literal('aud'),
            Literal(3)
        )
    )

    # Each rdf_orm model has a local 'g' attribute.
    g += item_two.g + item_three.g

    # Concatenate a list of items to the individual's items.
    individual.items += [item_two, item_three]

    # Add another item using Python's list method 'append'
    individual.items.append(item_four)

    # Add the data of the individual instance to the global graph object.
    g += individual.g

    # Print the global graph object.
    print(g.serialize(format='turtle').decode('utf-8'))

    # Output of the print.
    """
    @prefix ns1: <https://example.com/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    
    <item-1> a ns1:Item ;
        rdfs:label "item 1" ;
        ns1:hasPrice [ a ns1:Price ;
                rdf:value 15 ;
                ns1:hasCurrency "usd" ] ;
        ns1:isItemOf <individual-1> .
    
    <item-2> a ns1:Item ;
        rdfs:label "item 2" ;
        ns1:hasPrice [ a ns1:Price ;
                rdf:value 5 ;
                ns1:hasCurrency "aud" ] ;
        ns1:isItemOf <individual-1> .
    
    <item-3> a ns1:Item ;
        rdfs:label "item 3" ;
        ns1:hasPrice [ a ns1:Price ;
                rdf:value 11 ;
                ns1:hasCurrency "usd" ] ;
        ns1:isItemOf <individual-1> .
    
    <item-4> a ns1:Item ;
        rdfs:label "item 4" ;
        ns1:hasPrice [ a ns1:Price ;
                rdf:value 3 ;
                ns1:hasCurrency "aud" ] ;
        ns1:isItemOf <individual-1> .
    
    <individual-1> a <http://www.w3.org/2002/07/owl#Class> ;
        rdfs:label "Individual 1 modified" ;
        ns1:hasItem <item-1>,
            <item-2>,
            <item-3>,
            <item-4> .
    """
