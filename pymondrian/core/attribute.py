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


class Attribute(object):
    def __init__(self, xml_attribute_name=None, value=None):
        self._xml_attribute_name = xml_attribute_name
        self._value = value

    @property
    def xml_attribute_name(self):
        return self._xml_attribute_name

    @xml_attribute_name.setter
    def xml_attribute_name(self, xml_attribute_name):
        self._xml_attribute_name = xml_attribute_name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def to_xml(self):
        return {self._xml_attribute_name: str(self._value)}

    def __eq__(self, other):
        if type(other) is Attribute:
            return self.value == other.value
        else:
            return self.value == other

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return u'{0}: {1}'.format(self.__class__, self.value)
