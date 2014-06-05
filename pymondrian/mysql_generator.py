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

from pymondrian.generator import DDLGenerator


class MySQLGenerator(DDLGenerator):
    def generate(self, schema, file_name=None, output=0):
        ddls = []
        for cube in schema.cubes:
            table = cube.fact
            foreign_keys = []
            measures = []

            dimensions_dll = []
            for dimension in cube.dimensions:
                foreign_keys.append(dimension.foreign_key)
                dimensions_dll.append(self._generate_dimension_dll(dimension))

            for measure in cube.measures:
                measures.append(measure)

            fact_ddl = []
            fact_ddl.append('CREATE TABLE {0} ('.format(table.name))
            pks = []
            used_column = {}
            for _fk in foreign_keys:
                fact_ddl.append('\t{0} INT NOT NULL,'.format(_fk))
                pks.append(str(_fk))

            for mea in measures:
                if mea.column.value not in used_column:
                    data_type = ''
                    if mea.datatype is None or mea.datatype == 'Integer':
                        data_type = 'INT'
                    else:
                        data_type = 'DECIMAL(11,2)'

                    fact_ddl.append('\t{0} {1} NOT NULL,'.format(mea.column,
                                    data_type))
                    used_column[mea.column.value] = 1

            fact_ddl.append('\tPRIMARY KEY ({0})'.format(', '.join(pks)))
            fact_ddl.append(');')

            ddls.append('\n'.join(dimensions_dll))
            ddls.append('\n'.join(fact_ddl))

        if output == 0:
            if not file_name:
                ddl_file = '{0}'.sql(schema.name)
            else:
                ddl_file = file_name

            with open(ddl_file, 'w') as f:
                f.write('\n'.join(ddls))
        else:
            return '\n'.join(ddls)

    def _generate_dimension_dll(self, dimension):

        hierarchy = dimension.get_hierarchy(0)
        dim_ddl = []
        dim_ddl.append('CREATE TABLE {0} ('.format(hierarchy.table))

        dim_ddl.append('\t{0} INT PRIMARY KEY AUTO_INCREMENT,'
                       .format(dimension.foreign_key))

        levels = hierarchy.levels

        used_column = {}
        used_column[dimension.foreign_key.value] = 1

        for level in levels:
            if level.column.value not in used_column:
                dim_ddl.append('\t{0} INT NOT NULL,'.format(level.column))
                used_column[level.column.value] = 1

            if (level.name_column.value and level.name_column.value
                    not in used_column):
                dim_ddl.append('\t{0} VARCHAR(255) NOT NULL,'
                               .format(level.name_column))
                used_column[level.name_column.value] = 1

        dim_ddl[-1] = dim_ddl[-1].replace(',', '')
        dim_ddl.append(');')

        return '\n'.join(dim_ddl)
