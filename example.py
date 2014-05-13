# -*- coding: utf-8 -*-

from pymondrian.schema import Schema, Cube, Table, Dimension, Level, Measure
from pymondrian.generator import generate
from pymondrian.core.attribute import Attribute

# Create a new schema
sales_schema = Schema(name='SalesSchema',
                      description='A sales schema for testing')

# Create a cube
sales = Cube('Sales')
# Set de fact table
sales.fact = Table('fact_sales')
# Add cube to the schema
sales_schema.add_cube(sales)

# We now add the dimensions to the cube
dim_date = Dimension(name='Date', type='TimeDimension', foreign_key='DateKey')
'''
By default the dimension has a hierarchy that has the same name as the
dimension and a table called dim_dimension_name_in_lower_case, eg dim_date.
We add the levels to that hierarchy.
'''
year = Level(name='Year', column='Year', level_type='TimeYears')
month = Level(name='Month', column='Month', name_column='MonthName',
              level_type='TimeMonths')
day = Level(name='Day', column='DateKey', name_column='Day', level_type='TimeDays')
dim_date.add_level_to_hierarchy(hierarchy=0, level=year)
dim_date.add_level_to_hierarchy(hierarchy=0, level=month)
dim_date.add_level_to_hierarchy(hierarchy=0, level=day)

# Add dimension to the cube
sales.add_dimension(dim_date)

# This is a standard dimension, so we ommit the type
dim_product = Dimension(name='Product', foreign_key='ProductKey')
category = Level(name='Category', column='CategoryKey',
                 name_column='CategoryName')
name = Level(name='Product', column='ProductKey',
             name_column='ProductName')
dim_product.add_level_to_hierarchy(hierarchy=0, level=category)
dim_product.add_level_to_hierarchy(hierarchy=0, level=name)

sales.add_dimension(dim_product)

# We then add a meassure
cuantity = Measure(name='Cuantity', column='Cuantity')
# Set the aggregation function
cuantity.aggregator = 'avg'
# formatString is not yeat implemented but you can do this to add it
cuantity._format_string = Attribute(xml_attribute_name='formatString', value='####')
# Add it to the cube
sales.add_measure(cuantity)


# Get cube by name
nm_cube = sales_schema.get_cube('Sales')
print nm_cube.name

# Try to get a cube that doesn't exits
none_cube = sales_schema.get_cube('Dumb_Cube')
print none_cube

# Finally, we call the generation process generating to a file
generate(sales_schema)


# We can also print it to stdout
print generate(sales_schema, output=1)
