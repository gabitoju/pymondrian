PyMondrian
==========

PyMondrian is a Python schema an DW generator for the Mondrian OLAP engine.

With PyMondrian you create Python objetcs that are mapped into a Mondrian schema, that is, schema, cubes, dimensions, hierarchies, levels, annotations, meassures, etc.

PyMondrian also generates the DDL SQL scripts to create the datawarehouse tables.

The XML schema can be generated to a file or returned as a string.

The generated schema is based on Mondrian 3 according to the XML model for Mondrian schemas available at [http://mondrian.pentaho.com/documentation/xml_schema.php]().

Usage
-----

A working example is available at [https://github.com/gabitoju/pymondrian/blob/master/example.py]().

Current version features
-----

PyMondrian 0.2 generates the most basic schema in order to have a working OLAP Mondrian cube.

The available elements are:
- Schema
- Annotation
- Table
- Dimension
- Level
- Meassure

Basic DDL SQL generation is supported for MySQL.

Using not implemented attributes
-----

Even though not all the attributes of the available elements have been implemented, it is possible to add them in a very simple way.

This code snippet shows how to do that:
    
    # Import the Attribute class
    from pymondrian.core.attribute import Attribute

    # Let's add the formatString to a meassure
    format_string = Attribute(xml_attribute_name='formatString', value='####')
    
    # Now we assign it to the meassure like this
    cuantity._format_string = format_string

You can name the attribute whatever way you like it but thw following rules must be respected:
- The xml_attribute_name property should be named as the Mondrian attribute is named
- The property that contains the Attribute instance must start with '_'

API
-----


Todo
-----

- Implement Calculated Member and Key Expressions
- Generate API documentation
- Improve documentation
- Implement remaining elements
- <del>Implement DDL SQL generator</del>
- <del>Implement all the attributes of the current available elements</del>
