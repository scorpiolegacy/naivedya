# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################


from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.settings.extra_fields['auth_user'] = [
    Field('roll_no',default='None'),
    Field('account_class'),
    Field('profile_set',default=False)]
auth.define_tables(username=False,signature=False)

#auth.settings.showid = False

db.define_table('user_details',
    Field('user_id','integer'),
    Field('phone_number',requires=IS_MATCH('\d{10}')),
    Field('preferred_mess'),
    Field('preferred_caterer'),
    Field('state_name','string'),
    Field('account_initial_balance'),
    Field('account_curr_balance'),
    Field('your_booking_preference',requires=IS_IN_SET(['''Don't Book Food Automatically''','Book Food Automatically'])))

#List of sates :
state_name=['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana ', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']

#Managing validators for table : auth_user
db.auth_user.account_class.requires=IS_IN_DB(db,'account_type.acc_type')
db.user_details.user_id.writable=True;
db.user_details.user_id.readable=True;
db.user_details.account_initial_balance.writable=True
db.user_details.account_curr_balance.writable=True
db.user_details.preferred_mess.requires=IS_IN_DB(db,'mess_provider.place_of_mess')
db.user_details.preferred_caterer.requires=IS_IN_DB(db,'mess_provider.caterer_name')
db.user_details.state_name.requires=IS_IN_SET(state_name)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'upendra.k14@iiits.in'
mail.settings.login = 'upendra.k14@iiits.in:scorpio9460073825'
mail.settings.tls = True

## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
auth.settings.login_next = URL('default','index')
auth.settings.logout_next = URL('default','index')
#auth.settings.manager_actions = dict(db_admin=dict(role='user_12',heading='Manage Database',tables = db.tables))

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
