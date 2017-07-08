import sqlite3 as lite
import sys
import datetime
import os
import lxml.etree as etree

class OutputTable(object):
    '''
    classdocs
    '''


    def __init__(self, filename = None, databaseName = None, tableName = None):
        '''
        Constructor
        '''
        if filename is not None:
            d = etree.parse(open(filename))
            databaseName = str(d.xpath('//info/databaseName[1]/text()')[0])
            tableName = str(d.xpath('//info/tableName[1]/text()')[0])
        self.createOutputTable(databaseName, tableName)
        
    def createOutputTable(self, databaseName, tableName):
        self.databaseName = databaseName
        self.tableName = tableName


class CommandLineOutputTable(OutputTable):

    def printResults(self, resultsInfoOrdered):
        print resultsInfoOrdered

class SQLiteOutputTable(OutputTable):
        
    def printResults(self, resultsInfoOrdered):
        con = None
        date = datetime.datetime.now()
        combinedList = [date] + resultsInfoOrdered
        valuesStringQuestionMark = "?" + ", " * (len(combinedList) - 2) + "?"
        print "databaseName", self.databaseName
        try:
            con = lite.connect(self.databaseName)
            con.execute("INSERT INTO " + self.tableName +" VALUES(" + valuesStringQuestionMark + ")", combinedList)
            con.commit()
        
        except lite.Error, e:
            
            if con:
                con.rollback()
                
            print "Error %s:" % e.args
            sys.exit(1)
            
        finally:
            
            if con:
                con.close()