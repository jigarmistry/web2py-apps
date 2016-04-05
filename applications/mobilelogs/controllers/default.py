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
    response.flash = T("Hello World")
    return "Hello World !"

def logs():
    import os
    import csv
    from collections import OrderedDict

    csvfile = open(os.path.join(request.folder, 'private', 'MobileLog.csv'))
    mobilelogs = csv.reader(csvfile, delimiter=';', quotechar='|')

    dict_data = {}
    dict_months = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}

    list_arg = request.args
    com_date = ''
    if list_arg != []:
        for i in list_arg:
            com_date += i+'-'

    com_date = com_date[:-1]

    for row in mobilelogs:

        date = row[4][0:11]
        date_com = date

        if len(list_arg) == 1:
            date_com = date[0:4]
        elif len(list_arg) == 2:
            date_com = date[0:7]
        elif len(list_arg) == 3:
            date_com = date[0:10]
        else:
            date_com = com_date

        if date != 'Date' and date_com == com_date:
            if date not in dict_data.keys():
                dict_data[date] = []
                dict_data[date].append(row)
            else:
                dict_data[date].append(row)

    dict_data = OrderedDict(sorted(dict_data.items(), key=lambda t: t[0]))

    return dict(dict_data=dict_data,dict_months=dict_months)


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

def test():
    return response.json({"test":"test"})
