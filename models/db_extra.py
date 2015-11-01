# -*- coding: utf-8 -*-
import datetime

###########################################################################################################
#Defining table for storing notifications
db.define_table('general_notifications',
                Field('title'),
                Field('general_notifications_file','upload'),
                Field('general_notifications_content','text'))
#Managing validators for table : general_notifications
db.general_notifications.title.requires=IS_NOT_EMPTY()
db.general_notifications.general_notifications_content.requires=IS_NOT_EMPTY()
############################################################################################################

###############################################################################################################
#Defining table for storing complaints
db.define_table('complaint_register',
                Field('complaint_subject'),
                Field('complaint_register_file','upload',requires=IS_LENGTH(10485760, 1024)),
                Field('complaint_register_content','text'),
                Field('complaint_register_isread','boolean',default=False),
                auth.signature)
#Managing validators for table : complaint_register
db.complaint_register.complaint_subject.requires=IS_NOT_EMPTY()
db.complaint_register.complaint_register_content.requires=IS_NOT_EMPTY()
####################################################################################################################

################################################################################################################################
#Defining table for storing reserved food
db.define_table('reserve_food',
                Field('reserve_eating_place'),
                Field('reserve_caterer'),
                Field('reserve_date','date'),
                Field('reserve_meal'),
                Field('author_id'))

db.reserve_food.reserve_meal.requires=IS_IN_DB(db,'Meal.meal_name')
db.reserve_food.reserve_eating_place.requires=IS_IN_DB(db,'mess_provider.place_of_mess')
db.reserve_food.reserve_caterer.requires=IS_IN_DB(db,'mess_provider.caterer_name')
#################################################################################################################################

##################################################################################################################################
db.define_table('mess_places',
                Field('place_name'))

db.define_table('mess_provider',
                Field('caterer_name'),
                Field('place_of_mess',requires=IS_IN_DB(db,'mess_places.place_name')),
                Field('email',requires=IS_EMAIL()),
                Field('account_curr_balance',default=0),
                Field('phone_number'))

db.mess_provider.account_curr_balance.writable=False
##################################################################################################################################

######################################################################################################################################
db.define_table('mess_menu',
                Field('caterer_name'),
                Field('place_of_mess'),
                Field('mess_time'),
                Field('week_day'),
                Field('eating_item'))

db.mess_menu.caterer_name.requires=IS_IN_DB(db,'mess_provider.caterer_name')
db.mess_menu.place_of_mess.requires=IS_IN_DB(db,'mess_provider.place_of_mess')
db.mess_menu.mess_time.requires=IS_IN_DB(db,'Meal.meal_name')
db.mess_menu.week_day.requires=IS_IN_SET(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])

db.define_table('meals_timing',
                Field('mess_place'),
                Field('mess_time'),
                Field('eating_time',requires=IS_TIME()),
                Field('advance_booking'),
                Field('advance_cancellation'))
db.meals_timing.mess_place.requires=IS_IN_DB(db,'mess_provider.place_of_mess')
db.meals_timing.mess_time.requires=IS_IN_DB(db,'Meal.meal_name')

#########################################################################################################################################
#Types of account

db.define_table('account_type',
                Field('acc_type'))
#########################################################################################################################################

########################################################################################################################################
#Rate of food

db.define_table('Meal',
                Field('meal_name'),
                Field('meal_rate'))
db.Meal.meal_name.requires= IS_NOT_IN_DB(db,'Meal.meal_name')
