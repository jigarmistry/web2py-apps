# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return redirect("manage_users")

def getusers():
    if request.env.request_method == "POST":
        personname = request.post_vars["person"]
        result = db(db.chatusers.personname == personname).select()
        if len(result) == 1:
            return dict({"login":"yes","msg":"You are successfully logged in."})
        else:
            return dict({"login":"no","msg":"You are not valid user."})
    else:
        return "Thanks"


@auth.requires_login()
def manage_users():
    grid = SQLFORM.smartgrid(db.chatusers,user_signature=False,csv=False)
    return locals()

def getlogs():
    if request.env.request_method == "POST":
        person = request.post_vars["person"]
        msg = request.post_vars["msg"]
        datestamp = request.post_vars["datestamp"]
        if msg != "S":
            db.logs.insert(msg=msg,person=person,datestamp=datestamp)
        rows = db().select(db.logs.ALL,orderby=~db.logs.id,limitby=(0,10))
        return dict(logs=rows)
    elif request.env.request_method == "GET":
        return "Thanks"

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
