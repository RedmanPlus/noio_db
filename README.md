# noio_db

An Object Relational Mapper (ORM) built to work with any IO

![linting](https://github.com/RedmanPlus/noio_db/actions/workflows/lint.yml/badge.svg)
![coverage](https://github.com/RedmanPlus/noio_db/actions/workflows/test.yml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/noio-db/badge/?version=latest)](https://noio-db.readthedocs.io/en/latest/?badge=latest)

## Inspirations
Implements a No IO architecture proposed by Cory Benfield in his talk on PyCon 2016 - https://www.youtube.com/watch?v=7cC3_jGwl_U&t=1503s

Heavily inspired by tiangolo's SQLModel - https://github.com/tiangolo/sqlmodel

## Motivation
Though in his talk Cory talks generally about HTTP protocols and their usage for HTTP libraries, this architecure holds much potential for the ORM libraries as well, since much of the problems with current ORM's and their conversion from sync to async comes from communication with the database.

By implementing an ORM as a NoIO system that can get dat from any type of a driver, we can create ORM code that is CPU-bound simply and just wrap it with asyncio functions for making it async.

Also it is desired to use SQLModel's benefits of pydantic models without SQLAlchemy's query building interface and sessions