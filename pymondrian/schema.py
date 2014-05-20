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
        self._default_role = Attribute('defaultRole', default_role)
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

    @property
    def default_role(self):
        return self._default_role

    @default_role.setter
    def default_role(self, default_role):
        self._default_role.value = default_role

    def add_cube(self, cube):
        for e in self._cubes:
            if e.name == cube.name:
                raise Exception('''Cube "{0}" already exists in schema
                                "{1}"'''.format(cube.name, self.name))
        self._cubes.append(cube)

    def remove_cube(self, cube):
        super(Schema, self)._remove_child(cube, self._cubes, type(Cube))

    def get_cube(self, cube_name):
        for e in self._cubes:
            if e.name == cube_name:
                return e

        return None


class Cube(SchemaElement):
    def __init__(self, name, description=None, caption=None, cache=True,
                 enabled=True, visible=True, default_measure=None):
        SchemaElement.__init__(self, name)
        self._description = Attribute('description', description)
        self._caption = Attribute('caption', caption)
        self._cache = Attribute('cache', cache)
        self._enabled = Attribute('enabled', enabled)
        self._visible = Attribute('visible', visible)
        self._default_measure = Attribute('defaultMeasure', default_measure)
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

    @property
    def default_measure(self):
        return self._default_measure

    @default_measure.setter
    def default_measure(self, default_measure):
        self._default_measure = default_measure

    def add_dimension(self, dimension):
        for e in self._dimensions:
            if e.name == dimension.name:
                raise Exception('''Dimension "{0}" already exists in cube
                                "{1}"'''.format(dimension.name, self.name))
        self._dimensions.append(dimension)

    def remove_dimension(self, dimension):
        super(Cube, self)._remove_child(dimension, self._dimensions,
                                        type(Dimension))

    def get_dimension(self, dimension_name):
        for e in self._dimensions:
            if e.name == dimension_name:
                return e
        return None

    def add_measure(self, measure):
        for e in self._measures:
            if e.name == measure.name:
                raise Exception('''Measure "{0}" already exists in cube
                                "{1}"'''.format(measure.name, self.name))
        self._measures.append(measure)

    def remove_measure(self, measure):
        super(Cube, self)._remove_child(measure, self._measures, type(Measure))

    def get_measure(self, measure_name):
        for e in self._measures:
            if e.name == measure_name:
                return e
        return None


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
    def __init__(self, name, visible=True, has_all=True, all_member_name=None,
                 all_member_caption=None, all_level_name=None,
                 primary_key=None, primary_key_table=None,
                 default_member=None, member_reader_class=None, caption=None,
                 description=None, unique_key_level_name=None):
        SchemaElement.__init__(self, name)
        self._visible = Attribute('visible', visible)
        self._has_all = Attribute('hasAll', has_all)
        self._all_member_name = Attribute('allMemberName', all_member_name)
        self._all_member_caption = Attribute('allMemberCaption',
                                             all_member_caption)
        self._all_level_name = Attribute('allLevelName', all_level_name)
        self._primary_key = Attribute('primaryKey', primary_key)
        self._primary_key_table = Attribute('primaryKeyTable',
                                            primary_key_table)
        self._default_member = Attribute('defaultMember', default_member)
        self._member_reader_class = Attribute('memberReaderClass',
                                              member_reader_class)
        self._caption = Attribute('caption', caption)
        self._description = Attribute('description', description)
        self._unique_key_level_name = Attribute('uniqueKeyLevelName',
                                                unique_key_level_name)
        self._atable = Table('dim_' + name.lower())
        self._levels = []

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        self._visible.value = visible

    @property
    def has_all(self):
        return self._has_alll

    @has_all.setter
    def has_all(self, has_all):
        self._has_all.value = has_all

    @property
    def all_member_name(self):
        return self._all_member_name

    @all_member_name.setter
    def all_member_name(self, all_member_name):
        self._all_member_name.value = all_member_name

    @property
    def all_member_caption(self):
        return self._all_member_caption

    @all_member_caption.setter
    def all_member_caption(self, all_member_caption):
        self._all_member_caption.value = all_member_caption

    @property
    def all_level_name(self):
        return self._all_level_name

    @all_level_name.setter
    def all_level_name(self, all_level_name):
        self._all_level_name.value = table

    @property
    def primary_key(self):
        return self._primay_key

    @primary_key.setter
    def primary_key(self, primary_key):
        self._primary_key.value = primary_key

    @property
    def primary_key_table(self):
        return self._primary_key_table

    @primary_key_table.setter
    def primary_key_table(self, primary_key_table):
        self._primary_key_table.value = primary_key_table

    @property
    def default_member(self):
        return self._default_member

    @default_member.setter
    def default_member(self, default_member):
        self._default_member.value = default_member

    @property
    def member_reader_class(self):
        return self._member_reader_class

    @member_reader_class.setter
    def member_reader_class(self, member_reader_class):
        self._member_reader_class.value = member_reader_class

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        self._caption.value = caption

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description.value = description

    @property
    def unique_key_level_name(self):
        return self._unique_key_level_name

    @unique_key_level_name.setter
    def unique_key_level_name(self, unique_key_level_name):
        self._unique_key_level_name.value = unique_key_level_name

    @property
    def table(self):
        return self._atable

    @table.setter
    def tale(self, table):
        self._atable = table

    def add_level(self, level, level_position=None):
        for e in self._levels:
            if e.name == level.name:
                raise Exception('''Level "{0}" already exists in hierarchy
                                "{1}"'''.format(level.name, self.name))

        if level_position is None:
            self._levels.append(level)
        else:
            self._levels.insert(level_position, level)

    def remove_level(self, level):
        super(Hierarchy, self)._remove_child(level, self._levels, type(Level))

    def get_level(self, level_name):
        for e in self._levels:
            if e.name == level_name:
                return e
        return None


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
        super(Dimension, self)._remove_child(hierarchy, self._hierarchies,
                                             type(Hierarchy))


class Level(SchemaElement):
    def __init__(self, name, column=None, name_column=None, visible=True,
                 level_type='Regular', approx_row_count=None, table=None,
                 ordinal_column=None, parent_column=None, ttype=None,
                 null_parent_value=None, internal_type=None, formatter=None,
                 unique_members=False, hide_member_if=None, caption=None,
                 description=None, caption_column=None):
        SchemaElement.__init__(self, name)
        self._column = Attribute('column', column)
        self._name_column = Attribute('nameColumn', name_column)
        self._level_type = Attribute('levelType', level_type)
        self._approx_row_count = Attribute('approxRowCount', approx_row_count)
        self._table = Attribute('table', table)
        self._ordinal_column = Attribute('ordinalColumn', ordinal_column)
        self._parent_column = Attribute('parentColumn', parent_column)
        self._type = Attribute('type', ttype)
        self._null_parent_value = Attribute('nullParentValue',
                                            null_parent_value)
        self._internal_type = Attribute('internalType', internal_type)
        self._formatter = Attribute('formatter', formatter)
        self._unique_members = Attribute('uniqueMembers', unique_members)
        self._hide_member_if = Attribute('hideMemberIf', hide_member_if)
        self._caption = Attribute('caption', caption)
        self._description = Attribute('description', description)
        self._caption_column = Attribute('captionColumn', caption_column)

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

    @property
    def approx_row_count(self):
        return self._approx_row_count

    @approx_row_count.setter
    def approx_row_count(self, approx_row_count):
        self._approx_row_count.value = approx_row_count

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, table):
        self._table.value = table

    @property
    def ordinal_column(self):
        return self._ordinal_column

    @ordinal_column.setter
    def ordinal_column(self, ordinal_column):
        self._ordinal_column.value = ordinal_column

    @property
    def parent_column(self):
        return self._parent_column

    @parent_column.setter
    def parent_column(self, parent_column):
        self._parent_column.value = parent_column

    @property
    def ttype(self):
        return self._type

    @ttype.setter
    def ttype(self, ttype):
        self._type.value = ttype

    @property
    def null_parent_value(self):
        return self._null_parent_value

    @null_parent_value.setter
    def null_parent_value(self, null_parent_value):
        self._null_parent_value.value = null_parent_value

    @property
    def internal_type(self):
        return self._internal_type

    @internal_type.setter
    def internal_type(self, internal_type):
        self._internal_type.value = internal_type

    @property
    def formatter(self):
        return self._formatter

    @formatter.setter
    def formatter(self, formatter):
        self._formatter.value = formatter

    @property
    def unique_members(self):
        return self._unique_members

    @unique_members.setter
    def unique_members(self, unique_members):
        self._unique_members.value = unique_members

    @property
    def hide_member_if(self):
        return self._hide_member_if

    @hide_member_if.setter
    def hide_member_if(self, hide_member_if):
        self._hide_member_if.value = hide_member_if

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        self._caption.value = caption

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description.value = description

    @property
    def caption_column(self):
        return self._caption_column

    @caption_column.setter
    def caption_column(self, caption_column):
        self._caption_column.value = caption_column


class Measure(SchemaElement):
    def __init__(self, name, column=None, aggregator='sum', datatype=None,
                 format_string=None, formatter=None, caption=None,
                 description=None, visible=True):
        SchemaElement.__init__(self, name)
        self._column = Attribute('column', column)
        self._aggregator = Attribute('aggregator', aggregator)
        self._datatype = Attribute('datatype', datatype)
        self._format_string = Attribute('formatString', format_string)
        self._formatter = Attribute('formatter', formatter)
        self._caption = Attribute('caption', caption)
        self._description = Attribute('description', description)
        self._visible = Attribute('visible', visible)

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

    @property
    def datatype(self):
        return self._datatype

    @datatype.setter
    def datatype(self, datatype):
        self._datatype.value = datatype

    @property
    def format_string(self):
        return self._format_string

    @format_string.setter
    def format_string(self, format_string):
        self._format_string.value = format_string

    @property
    def formatter(self):
        return self._formatter

    @formatter.setter
    def formatter(self, formatter):
        self._formatter.value = formatter

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        self._caption.value = caption

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description.value = description

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        self._visible.value = visible
