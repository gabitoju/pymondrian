# -*- coding: utf-8 -*-

'''
The MIT License (MIT)

Copyright (c) 2014 Juan Gabito

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


from xml.etree.cElementTree import Element
from pymondrian.core.attribute import Attribute


class Annotations(object):
    def __init__(self):
        self._annotations = []

    def add(self, annotation, parent):
        for _annot in self._annotations:
            if _annot.name == annotation.name:
                raise Exception('''Annotaion "{0}" already exists in object
                                "{1}"'''.format(annotation.name, parent.name))
        self._annotations.append(annotation)

    def has_annotations(self):
        return len(self._annotations) > 0

    def to_xml(self):
        node = Element(self.__class__.__name__, {})

        for _annot in self._annotations:
            node.append(_annot.to_xml())

        return node


class Annotation(object):
    def __init__(self, name, value):
        self._name = Attribute('name', name)
        self._value = Attribute('value', value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name.value = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value.value = value

    def to_xml(self):
        node = Element(self.__class__.__name__, self._name.to_xml())
        node.text = str(self._value)
        return node


class SchemaElement(object):
    def __init__(self, name):
        self._name = Attribute('name', name)
        self._annotations = Annotations()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name.value = value

    def add_annotation(self, annotation):
        self._annotations.add(annotation, self)

    def remove_child(self, child, collection, obj_type):
        if type(child) is int:
            if child >= 0 and child < len(collection):
                del collection[child]
        elif type(child) is str:
            child_index = -1
            for _annot in collection:
                child_index += 1
                if _annot.name == child:
                    del collection[child_index]
                    break
        elif isinstance(child, obj_type):
            child_index = collection.index(child)
            del collection[child_index]

    def to_xml(self):
        node = Element(self.__class__.__name__, {})
        for _el in dir(self):
            if _el and _el.startswith('_'):
                attr = getattr(self, _el)
                if isinstance(attr, Attribute) and attr.value:
                    node.attrib.update(attr.to_xml())
                elif (isinstance(attr, SchemaElement) or
                      (isinstance(attr, Annotations) and
                        attr.has_annotations())):
                    node.append(attr.to_xml())
                elif isinstance(attr, list):
                    for element in attr:
                        node.append(element.to_xml())

        return node

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)
