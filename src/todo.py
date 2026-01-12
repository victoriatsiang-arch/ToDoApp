
from datetime import datetime
from dotenv import load_dotenv 
import os
toDoList = []

import pymysql # type: ignore
import logging
global database
global logger

def configureLogging():
    # Only configure if no handlers exist (so pytest can override)
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            filename="todo.log",
            filemode="a",
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
# Make logger global so all functions can access it
configureLogging()
logger = logging.getLogger("todo")
logger.warning("connection established")
    

def connect2DB(): #can pass in param args to make it more user friendly
    try:
        load_dotenv()  # This loads variables from the .env file
        db_password = os.getenv("PASSWORD")
        #configureLogging()
        # Establishing the connection
        connection = pymysql.connect(
            host     = "riku.shoshin.uwaterloo.ca", #"127.0.0.1"
            user     = "vtsiang", 
            database = "se101_vtsiang",
            password = db_password)
        logger.warning("connection established")
        return connection

    except pymysql.Error as err:
        logger.warning("connection not established")
        return None
    
def add(task):
    #configureLogging()
    connection = connect2DB()
    if (connection != None):
        cursor = connection.cursor()
        check_matching = """
        SELECT COUNT(*) FROM ToDoData WHERE item = %s AND type = %s
        AND started = %s AND due = %s AND done = %s"""
        tempTask = (task[0],task[1], task[2], task[3], task[4])
        
        cursor.execute(check_matching, tempTask)
        result = cursor.fetchone()
        logger.info(f"Add task? {(result == (0,))}")
        if(result == (0,)):
            query = """INSERT INTO ToDoData (item, type, started, due, done) VALUES (%s, %s,%s,%s,%s)"""
            cursor.execute(query, tempTask)
            connection.commit()
            cursor.close()
            connection.close()
            return("Task appended!")
        else:
            logger.warning("task already there")
            cursor.close()
            connection.close()
            return("Task already there!")
    else:
        logger.warning("Query Error")
        return None

def update(task):
    #configureLogging()
    connection = connect2DB()
    if (connection != None):
        cursor = connection.cursor()
        query = """UPDATE ToDoData SET type = %s, started = %s, due = %s, done = %s WHERE item = %s"""
        tempTask = (task[1], task[2], task[3], task[4], task[0])
        cursor.execute(query, tempTask)
        logger.info(f"cursor rowcount: {cursor.rowcount}")
        if cursor.rowcount > 0:
            connection.commit()
            cursor.close()
            connection.close()
            return ("update successful")
        else:
            cursor.close()
            connection.close()
            return ("update unsuccessful")
    else:
        logger.warning("connection not established")
        return None

def next():
    #configureLogging()
    connection = connect2DB()
    cursor = connection.cursor()
    if (connection != None):
        query = """SELECT *, ABS(DATEDIFF(due, NOW())) AS day_diff
            FROM ToDoData
            ORDER BY day_diff
            LIMIT 1;"""
        cursor.execute(query)
        result = cursor.fetchone()
        return result
    else:
        cursor.close()
        connection.close()
        return "Opps no tasks in here!"