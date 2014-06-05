# -*- coding: utf-8 -*-

from pymondrian.schema import Schema, Cube, Table, Dimension, Level, Measure
from pymondrian.generator import generate
from pymondrian.core.attribute import Attribute
from pymondrian.mysql_generator import MySQLGenerator

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
day = Level(name='Day', column='DateKey', name_column='Day',
            level_type='TimeDays')
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

# More dimenions
dim_customer = Dimension(name='Customer', foreign_key='CustomerKey')
more_than_once = Level(name='More than Once', column='MoreThanOnceKey',
                       name_column='MoreThanOnceDes',
                       caption='Customer bought more than once?')
cus_name = Level(name='Customer Name', column='CustomerKey',
                 name_column='CustomerName')
dim_customer.add_level_to_hierarchy(hierarchy=0, level=more_than_once)
dim_customer.add_level_to_hierarchy(hierarchy=0, level=cus_name)

sales.add_dimension(dim_customer)

dim_supplier = Dimension(name='Supplier', foreign_key='SupplierKey')
sup_name = Level(name='Supplier Name', column='SupplierKey',
                 name_column='SupplierName')
dim_supplier.add_level_to_hierarchy(hierarchy=0, level=sup_name)

sales.add_dimension(dim_supplier)

quantity = Measure(name='Quantity', column='Quantity')
sales.add_measure(quantity)

subtotal = Measure(name='Subtotal', column='Subtotal', datatype='Numeric')
sales.add_measure(subtotal)

taxes = Measure(name='Taxes', column='Taxes', datatype='Numeric')
sales.add_measure(taxes)

total = Measure(name='Total', column='Total', datatype='Numeric')
sales.add_measure(total)

subtotal_avg = Measure(name='Subtotal Average', column='Subtotal',
                       aggregator='avg', datatype='Numeric')
sales.add_measure(subtotal_avg)

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

# Now we can get the DDL for MySQL
mysql_generator = MySQLGenerator()
mysql_generator.generate(sales_schema, file_name='t.sql')
