# PyMondrian


PyMondrian is a Python schema an DW generator for the Mondrian OLAP engine.

With PyMondrian you create Python objetcs that are mapped into a Mondrian schema, that is, schema, cubes, dimensions, hierarchies, levels, annotations, meassures, etc.

PyMondrian also generates the DDL SQL scripts to create the datawarehouse tables.

The XML schema can be generated to a file or returned as a string.

The generated schema is based on Mondrian 3 according to the XML model for Mondrian schemas available at [http://mondrian.pentaho.com/documentation/xml_schema.php]().

## Usage

A working example is available at [https://github.com/gabitoju/pymondrian/blob/master/example.py]().

## Current version features

PyMondrian 0.1 generates the most basic schema in order to have a working OLAP Mondrian cube.

The available elements are:
- Schema
- Annotation
- Table
- Dimension
- Level
- Meassure

DDL SQL generation is not yeat supported.

## API

## Todo
- Implement all the attributes of the current available elements
- Implement Calculated Member and Key Expressions
- Implement DDL SQL generator
- Generate API documentation
- Improve documentation
- Implement remaining elements
