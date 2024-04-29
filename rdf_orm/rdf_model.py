from typing import Union
from uuid import uuid4

from rdflib import URIRef, RDF, Graph
from rdflib.term import Node, BNode, Literal


class PropertyNotSetException(Exception):
    """Required property of RDFModel is not set."""
    pass


class MapTo:
    """Class to represent bidirectional relationships between individuals"""
    def __init__(self, value: Node, inverse: Node = None):
        self.value = value
        self.inverse = inverse


class RDFModel:
    """RDF Model"""
    class_uri: URIRef = None
    mapping: dict = None
    g: Graph
    rdf: str
    uri: Union[URIRef, BNode]

    def __init__(self):
        if self.class_uri is None:
            raise PropertyNotSetException(f'class_uri in {self.__class__.__name__} class is not defined.')
        if self.mapping is None:
            raise PropertyNotSetException(f'mapping in {self.__class__.__name__} class is not defined.')

        # This gets set in self._rdf()
        # self._g = Graph()

    def assign_constructor_vars(self, local_vars: locals):
        for key, val in local_vars.items():
            if key != 'self' and key != 'kwargs' and key != '__class__':
                setattr(self, key, val)

        # Generate a blank node if self.uri is not set.
        if not hasattr(self, 'uri'):
            self.uri = BNode(str(uuid4()))

    def __str__(self):
        if hasattr(self, 'label'):
            return f'<{self.label}>'
        else:
            return f'<{self.uri}>'

    @property
    def g(self) -> Graph:
        """Lazy load the rdflib.Graph object."""
        self._rdf()
        return self._g

    def _add(self, s: Node, p: Node, o: Node):
        if isinstance(p, URIRef):
            self._g.add((
                s,
                p,
                o
            ))
        elif isinstance(p, MapTo):
            self._g.add((
                s,
                p.value,
                o
            ))
            self._g.add((
                o,
                p.inverse,
                s
            ))
        else:
            raise TypeError(f'Unexpected type {type(p)} for value {p}')

    def _rdf(self, format: str = 'turtle'):
        # Set/reset g
        self._g = Graph()

        self._g.add((self.uri, RDF.type, self.class_uri))
        for key, rdf_property in self.mapping.items():
            value = getattr(self, key)
            # Check for optional values and skip if they are None.
            if value is not None:
                if isinstance(value, RDFModel):
                    self._add(
                        self.uri,
                        rdf_property,
                        value.uri
                    )
                    # if type(value.uri) == BNode:
                    #     self._g += value.g
                    self._g += value.g
                elif isinstance(value, list) or isinstance(value, tuple):
                    for item in value:
                        if isinstance(item, RDFModel):
                            self._add(
                                self.uri,
                                rdf_property,
                                item.uri
                            )
                            # if type(item.uri) == BNode:
                            #     self._g += item.g
                            self._g += item.g
                        elif isinstance(item, URIRef):
                            self._add(
                                self.uri,
                                rdf_property,
                                item
                            )
                        else:
                            raise TypeError(f'Unexpected type {type(item)} for value {item}')
                elif isinstance(value, Literal) or isinstance(value, URIRef):
                    self._add(
                        self.uri,
                        rdf_property,
                        value
                    )
                else:
                    raise TypeError(f'Unexpected type {type(value)} for value {value}')
        return self._g.serialize(format=format)

    @property
    def rdf(self):
        return self._rdf()
