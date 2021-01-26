#SDP2021
#GROUP21
#CREATED BY: REECE WALKER
#PREVIOUS VERSION BY: *BLANK*
#CURRENT VERSION BY: REECE WALKER

#TODO:
#   POSSIBLE TO DO SQL INJECTION AND HANG UP PROGRAM IF AN EDIT COMMAND IS
#   USED WITHIN 'querry_database' 

import pyodbc
import copy

#CLASS FOR DEFINING A CONNECTION TO DATABASE, CONTAINS METHODS FOR RUNNING
#SQL CODE ON THE DATABASE GIVEN AN INPUT
class Database_Connector:

    #CONSTRUCTOR FOR CLASS
    def __init__(self, server_name, database_name):
        self.server_name = server_name
        self.database_name = database_name

    #PRIVATE METHOD FOR CREATING A 'pyodbc.connection' THAT IS USED BY OTHER
    #METHODS THAT NEED TO CONNECT TO A DATABASE
    #
    #@RETURNS:
    #   Type 'pyodbc.connection' containing the connection to a database
    def __create_connection(self):
        conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=' + self.server_name + ';'
        'Database=' + self.database_name + ';'
        'Trusted_Connection=yes;')
        return conn

    #USED WHEN QUERRYING DATABASE, RETURNS ANSWER TO QUERRY PASSED TO IT
    #
    #@PARAM:
    #   querry_string: String containing SQL querry
    #
    #@RETURNS:
    #   Type 'pyodbc.cursor' containing result of querry
    def querry_database(self, querry_string):
        conn = self.__create_connection()
        cursor = conn.cursor()
        querry_result = conn.execute(querry_string)
        return querry_result

    #USED TO EDIT/UPDATE DATABASE AND COMMITS CHANGE
    #
    #@PARAM:
    #   command_string:
    #       String containing SQL command such as 'UPDATE' or 'INSERT'
    def edit_database(self, command_string):
        conn = self.__create_connection()
        cursor = conn.cursor()
        conn.execute(command_string)
        conn.commit()
