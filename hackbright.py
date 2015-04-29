"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])

def make_new_student(first_name, last_name, github):

    QUERY = """
        INSERT INTO Students
        VALUES (?, ?, ?)
        """ 
    db_cursor.execute(QUERY,(first_name, last_name, github))
    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_by_title(title):
    """Given a title name, print description and max grade"""

    QUERY = """
        SELECT title, description, max_grade
        FROM Projects
        WHERE title = ?
        """
    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    print "%s is about %s. The max grade is %s." % (
        row[0], row[1], row[2])

def get_grade(project_title, student_github):
    """Given a github username and project title, return the grade"""

    QUERY = """
        SELECT grade, project_title, student_github
        FROM grades
        WHERE project_title = ?
        AND student_github = ?
    """

    db_cursor.execute(QUERY, (project_title, student_github))
    row = db_cursor.fetchone()
    print "The grade for %s is: %s. Done by: %s" % (
        row[1], row[0], row[2])

    """When indexing from the row, refer to order we are SELECTing"""
    

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "title":
            title = args[0]
            get_by_title(title)

        elif command == "grade":
            project_title, student_github = args
            get_grade(project_title, student_github)



if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
