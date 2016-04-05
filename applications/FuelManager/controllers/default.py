# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return redirect("log")

@auth.requires_login()
def log():
    db.vehicle.id.readable = False
    db.log.id.readable = False
    db.log.mileage.writable = False
    headers = {'log.kms':"OddoMeter(kms)",'log.liters':'Liters','log.mileage':'Mileage(km/l)','log.cost':'Cost(Rs.)','log.date':'Date'}
    grid = SQLFORM.smartgrid(db.log,linked_tables=['vehicle'],user_signature=False,paginate=10,oncreate=oncreatelog, onupdate=oncreatelog, onvalidation=myvalidation,csv=False,headers=headers,orderby=~db.log.kms)
    return locals()

def myvalidation(form):
    pass

def oncreatelog(form):
    row =  db().select(db.log.ALL,orderby=~db.log.id, limitby=(0,2))
    if len(row) > 1:
        row1 = row[1]
        row0 = row[0]
        mileage = float((row0.kms - row1.kms)/float(row1.liters))
        mileage = float("{0:.2f}".format(mileage))
        row0.update_record(mileage=mileage)

@auth.requires_login()
def vehicles():
    db.vehicle.id.readable = False
    db.log.id.readable = False
    db.log.mileage.writable = False
    grid = SQLFORM.smartgrid(db.vehicle,linked_tables=['log'],user_signature=False,paginate=10,csv=False,oncreate=oncreatelog,onupdate=oncreatelog)
    return locals()

@auth.requires_login()
def services():
    db.service.id.readable = False
    headers = {'service.kms':"OddoMeter(kms)",'service.cost':'Cost(Rs.)','service.date':'Date'}
    grid = SQLFORM.smartgrid(db.service,linked_tables=['vehicle'],user_signature=False,paginate=10,csv=False,headers=headers,orderby=db.service.date)
    return locals()

@auth.requires_login()
def reports():
    from collections import defaultdict
    rows = db().select(db.log.ALL)

    dict_vehicle = defaultdict(dict)
    for row in rows:
        date = row.date.strftime("%m-%Y")
        dict_vehicle[row.vehicle].setdefault(date, []).append(row.cost)

    dict_report = defaultdict(dict)
    for k,v in dict_vehicle.items():
        vehicle_name = db(db.vehicle.id==k).select(db.vehicle.name)
        for t,h in v.items():
            dict_report[vehicle_name[0].name][t] = sum(h)
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
