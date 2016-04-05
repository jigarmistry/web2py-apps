# -*- coding: utf-8 -*-

db = DAL("sqlite://storage.sqlite")

db.define_table("vehicle",
               Field ("name",requires=IS_NOT_EMPTY()),
               Field ("brand",requires=IS_NOT_EMPTY()),
               Field ("photo","upload"),
               format = '%(name)s')

db.vehicle.name.requires = IS_NOT_IN_DB(db, db.vehicle.name)

db.define_table("log",
               Field("kms","double",requires=IS_NOT_EMPTY()),
               Field("liters","double",requires=IS_NOT_EMPTY()),
               Field("mileage","double",default=0.0),
               Field("cost","double",requires=IS_NOT_EMPTY()),
               Field("date","date",requires = IS_NOT_EMPTY(),represent=lambda value, x: value.strftime('%d-%b-%Y')),
               Field("vehicle","reference vehicle"))

db.define_table("service",
                Field("name",requires=IS_NOT_EMPTY()),
                Field("description",default="-"),
                Field("service_type",requires=IS_IN_SET(("Free","Paid"))),
                Field("kms","double",requires=IS_NOT_EMPTY()),
                Field("cost","double",requires=IS_NOT_EMPTY()),
                Field("date","date",requires = IS_NOT_EMPTY(),represent=lambda value, x: value.strftime('%d-%b-%Y')),
                Field("vehicle","reference vehicle"))
