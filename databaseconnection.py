# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 07:34:09 2020

@author: Carlos
"""
import mysql.connector
import json
from mysql.connector import errorcode

def create_tables(cursor):
    TABLES = {}
    TABLES['tweets']=("CREATE TABLE `tweets` ("
  "`id` bigint(20) NOT NULL AUTO_INCREMENT,"
  "`account` varchar(255) DEFAULT NULL,"
  "`imagetweet` varchar(255) DEFAULT NULL,"
  "`content` text,"
  "`datetweet` varchar(255) DEFAULT NULL,"
  "`metadata` text,"
  "`isFakeNew` int(11) DEFAULT '-1',"
  "`ELA` float(30,10) DEFAULT NULL,"
  "`isManipulated` int(11) DEFAULT NULL,"
  "PRIMARY KEY (`id`)"
  ") ENGINE=InnoDB AUTO_INCREMENT=9209 DEFAULT CHARSET=utf8mb4;")
      
    TABLES['googlesearch']=("CREATE TABLE `googlesearch` ("
  "`id` bigint(20) NOT NULL AUTO_INCREMENT,"
  "`tweetid` bigint(20) NOT NULL,"
  "`url` longtext NOT NULL,"
  "`title` text NOT NULL,"
  "`ping` text,"
  "`imageName` text,"
  "`src` text NOT NULL,"
  "`pathFile` varchar(255) DEFAULT NULL,"
  "`similarity` float(100,8) DEFAULT NULL,"
  "PRIMARY KEY (`id`),"
  "KEY `fk_tweet_search` (`tweetid`),"
  "CONSTRAINT `fk_tweet_search` FOREIGN KEY (`tweetid`) REFERENCES `tweets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE"
  ") ENGINE=InnoDB AUTO_INCREMENT=210624 DEFAULT CHARSET=utf8mb4;")

  
    
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()

def database_connection():
    DB_NAME="platon"
    try:
        with open("config.json") as json_data_file:
                data = json.load(json_data_file)
                mydb = mysql.connector.connect(
                    host=data["mysql"]["host"],
                    user=data["mysql"]["user"],
                    password=data["mysql"]["passwd"],
                    #database=data["mysql"]["db"]
                    database=DB_NAME
                    
            )
                
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
        try:
            mydb = mysql.connector.connect(
                    host=data["mysql"]["host"],
                    user=data["mysql"]["user"],
                    password=data["mysql"]["passwd"])
            cursor=mydb.cursor()
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            mydb.database=DB_NAME
            create_tables(cursor)
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
      else:
        print(err)
    print(mydb)
    return mydb
    
database_connection()