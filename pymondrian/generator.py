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

from abc import ABCMeta, abstractmethod
from xml.etree.ElementTree import tostring
import xml.dom.minidom


def generate(schema, file_name=None, output=0):
    xml_node = xml.dom.minidom.parseString(tostring(schema.to_xml()))
    if output == 0:
        if not file_name:
            s_file = '{0}.xml'.format(schema.name)
        else:
            s_file = file_name
        with open(s_file, 'w') as schema_file:
            xml_node.writexml(schema_file, indent=' ', addindent='  ',
                              newl='\n')
    else:
        return xml_node.toprettyxml()


class DDLGenerator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate(self, schema, file_name=None, output=0):
        pass
