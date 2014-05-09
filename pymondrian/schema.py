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


from core.attribute import Attribute
from core.element import SchemaElement


class Schema(SchemaElement):
    def __init__(self, name, description=None, measures_caption=None,
                 default_role=None):
        SchemaElement.__init__(self, name)
        self._description = Attribute('description', description)
        self._measures_caption = Attribute('measuresCaption', measures_caption)
        self._cubes = []

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description.value = description

    @property
    def measures_caption(self):
        return self._measures_caption

    @measures_caption.setter
    def measures_caption(self, measures_caption):
        self._measures_caption.value = measures_caption

    def add_cube(self, cube):
        for e in self._cubes:
            if e.name == cube.name:
                raise Exception('''Cube "{0}" already exists in schema
                                "{1}"'''.format(cube.name, self.name))
        self._cubes.append(cube)


class Cube(SchemaElement):
    def __init__(self, name, description=None, caption=None, cache=True,
                 enabled=True, visible=True):
        SchemaElement.__init__(self, name)
        self._description = Attribute('description', description)
        self._caption = Attribute('caption', caption)
        self._cache = Attribute('cache', cache)
        self._enabled = Attribute('enabled', enabled)
        self._visible = Attribute('visible', visible)
        self._afact = None
        self._dimensions = []
        self._measures = []

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description.value = description

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, cache):
        self._cache.value = cache

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        self._enabled.value = enabled

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        self._visible.value = visible

    @property
    def fact(self):
        return self._afact

    @fact.setter
    def fact(self, fact):
        self._afact = fact

    def add_dimension(self, dimension):
        for e in self._dimensions:
            if e.name == dimension.name:
                raise Exception('''Dimension "{0}" already exists in cube
                                "{1}"'''.format(dimension.name, self.name))
        self._dimensions.append(dimension)

    def add_measure(self, measure):
        for e in self._measures:
            if e.name == measure.name:
                raise Exception('''Measure "{0}" already exists in cube
                                "{1}"'''.format(measure.name, self.name))
        self._measures.append(measure)


class Table(SchemaElement):
    def __init__(self, name, schema=None, alias=None):
        SchemaElement.__init__(self, name)
        self._schema = Attribute('schema', schema)
        self._alias = Attribute('alias', alias)

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, schema):
        self._schema.value = schema

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, alias):
        self._alias.value = alias


class Hierarchy(SchemaElement):
    def __init__(self, name, visible=True, has_all=True):
        SchemaElement.__init__(self, name)
        self._visible = Attribute('visible', visible)
        self._has_all = Attribute('hasAll', has_all)
        self._atable = Table('dim_' + name.lower())
        self._levels = []

    def add_level(self, level, level_position=None):
        for e in self._levels:
            if e.name == level.name:
                raise Exception('''Level "{0}" already exists in hierarchy
                                "{1}"'''.format(level.name, self.name))

        if level_position is None:
            self._levels.append(level)
        else:
            self._levels.insert(level_position, level)


class CubeDimension(SchemaElement):
    def __init__(self, name, caption=None, visible=True, description=None,
                 foreign_key=None, high_cardinality=False):
        SchemaElement.__init__(self, name)
        self._caption = Attribute('caption', caption)
        self._visible = Attribute('visible', visible)
        self._description = Attribute('description', description)
        self._foreign_key = Attribute('foreignKey', foreign_key)
        self._high_cardinality = Attribute('highCardinality', high_cardinality)

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        self._caption.value = caption

    @property
    def visible(self):
        return self.visible

    @visible.setter
    def visible(self, visible):
        self._visible.value = visible

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description.value = description

    @property
    def foreign_key(self):
        return self._foreign_key

    @foreign_key.setter
    def foreign_key(self, foreign_key):
        self._foreign_key.value = foreign_key

    @property
    def high_cardinality(self):
        return self._high_cardinality

    @high_cardinality.setter
    def high_cardinality(self, high_cardinality):
        self._high_cardinality.value = high_cardinality


class Dimension(CubeDimension):
    def __init__(self, name, type="StandardDimension", caption=None,
                 description=None, usage_prefix=None, visible=True,
                 foreign_key=None):
        CubeDimension.__init__(self, name, caption, visible, description,
                               foreign_key)
        self._type = Attribute('type', type)
        self._usage_prefix = Attribute('usagePregix', usage_prefix)
        self._hierarchies = []
        self.add_hierarchy(Hierarchy(name))

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type.value = type

    @property
    def usage_prefix(self):
        return self._usage_prefix

    @usage_prefix.setter
    def usage_prefix(self, usage_prefix):
        self._usage_prefix.value = usage_prefix

    def add_hierarchy(self, hierarchy):
        for e in self._hierarchies:
            if e.name == hierarchy.name:
                raise Exception('''Hierarchy "{0}" already exists in dimension
                                "{1}"'''.format(hierarchy.name, self.name))
        self._hierarchies.append(hierarchy)

    def add_level_to_hierarchy(self, hierarchy, level,
                               level_position=None):
        if type(hierarchy) is int and hierarchy < len(self._hierarchies):
            self._hierarchies[hierarchy].add_level(level, level_position)
        if type(hierarchy) is str or type(hierarchy) is Hierarchy:
            hierachy_name = str(hierarchy)
            for h in self._hierarchies:
                if h.name == hierachy_name:
                    h.add_level(level, level_position)

    def get_hierarchy(self, hierarchy):
        if type(hierarchy) is int:
            if hierarchy >= 0 and hierarchy < len(self._hierarchies):
                return self._hierarchies[hierarchy]
        elif type(hierarchy) is str:
            hierarchy_index = -1
            for e in self._hierarchies:
                hierarchy_index += 1
                if e.name == hierarchy:
                    return self._hierarchies[hierarchy_index]
        elif type(hierarchy) is Hierarchy:
            hierarchy_index = self._hierarchies.index(hierarchy)
            return self._hierarchies[hierarchy_index]
                    
    def remove_hierarchy(self, hierarchy):
        if type(hierarchy) is int:
            if hierarchy >= 0 and hierarchy < len(self._hierarchies):
                self._hierarchies.pop(hierarchy)
        elif type(hierarchy) is str:
            hierarchy_index = -1
            for e in self._hierarchies:
                hierarchy_index += 1
                if e.name == hierarchy:
                    del self._hierarchies[hierarchy_index]
                    break
        elif type(hierarchy) is Hierarchy:
            hierarchy_index = self._hierarchies.index(hierarchy)
            del self._hierarchies[hierarchy_index]


class Level(SchemaElement):
    def __init__(self, name, column=None, name_column=None, visible=True,
                 level_type='Regular'):
        SchemaElement.__init__(self, name)
        self._column = Attribute('column', column)
        self._name_column = Attribute('nameColumn', name_column)
        self._level_type = Attribute('levelType', level_type)

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, column):
        self._column.value = column

    @property
    def name_column(self):
        return self._name_column

    @name_column.setter
    def name_column(self, name_column):
        self._name_column.value = name_column

    @property
    def level_type(self):
        return self._level_type

    @level_type.setter
    def level_type(self, level_type):
        self._level_type.value = level_type


class Measure(SchemaElement):
    def __init__(self, name, column=None, aggregator='sum'):
        SchemaElement.__init__(self, name)
        self._column = Attribute('column', column)
        self._aggregator = Attribute('aggregator', aggregator)

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, column):
        self._column.value = column

    @property
    def aggregator(self):
        return self._aggregator

    @aggregator.setter
    def aggregator(self, aggregator):
        self._aggregator.value = aggregator

