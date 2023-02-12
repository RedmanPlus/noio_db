# TODOs

List of all enhancements for the library

## version 0.3.0 requirements:

- Add DELETE commands to the AST
- Add ALTER TABLE commands to the AST
- Add supportive methods to the model and query classes to handle object deletion
- Add primitive migration manager

## version 0.4.0 requirements:

- Redo BaseDriver, make it accept different engine interfaces
- Implement async driver interface, handle object creation and manipulation operation asyncronously
- Add multiple pre-existing base drivers

## version 0.5.0 requirements:

- Handle relations, add basic relation manager
- Handle more SQL data types, expand mapping

## version 0.6.0 requirements:

- Add supportive methods to the existing ones (more complex select/update queries)
- Add SQL functions (SUM, COUNT, AVG, etc)
- Add constraints

## version 0.7.0 requirements:

- Add transaction handling methods
- Add handling multiple AST's by a transaction

## version 1.0.0 requirements:

- Add async support for all features
- Add documentation
- END GOAL: try using noio_db with FastAPI