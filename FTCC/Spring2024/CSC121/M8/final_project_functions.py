# Functions for the final project
# 05/03/2024
# Harley Coughlin


import student as student_class
import csv


# reads a csv file and converts the info into a list of Student objects
def read_content():
    """Reads StudentInfo.csv and creates Student instances, returns list of objects"""
    try:
        with open("StudentInfo.csv", 'rt', newline='') as csv_file:
            # eating the header
            header = csv_file.readline()
            # loading StudentInfo into a list
            csv_reader = csv.reader(csv_file)
            # initializing list for student objects
            student_list = []
            # for each line in the csv
            # unpacking the line
            for last, first, id in csv_reader:
                # append the student object to the list
                student_list.append(student_class.Student(id, first, last))
            # return the list
            return student_list
    except FileNotFoundError:
        print("StudentInfo.csv not found in the current directory")
    except Exception as err:
        print("Something went wrong in read_content: " + str(err))


# just a helper function for formatting
def get_lengths(student_list):
    """Gets formatting information, returns int, int, int"""
    header = ['Last Name', 'First Name', 'Email']
    max_fname_len = 0
    max_lname_len = 0
    max_email_len = 0
    # get the lengths of the info from the student objects
    # get the formatting things
    for student in student_list:
        # get the max length of student first names
        fname_len = len(student.get_first_name())
        if fname_len > max_fname_len:
            max_fname_len = fname_len
        # get the max length of student last names
        lname_len = len(student.get_last_name())
        if lname_len > max_lname_len:
            max_lname_len = lname_len
        # get the max length of student emails
        email_len = len(student.get_email())
        if email_len > max_email_len:
            max_email_len = email_len
    # if the max name length is shorter than the length of the corresponding
    # header label, set max length to the length of the header instead
    max_fname_len = max_fname_len if max_fname_len > len(header[1]) else len(header[1])
    max_lname_len = max_lname_len if max_lname_len > len(header[0]) else len(header[0])
    return max_fname_len, max_lname_len, max_email_len


# creates a txt and csv file
def write_report(student_list):
    """Writes two files, one csv and one txt"""
    header_csv = ['ID #', 'Last Name', 'First Name', 'Login', 'Email', 'Active']
    # open the csv to write
    with open("student_accounts.csv", 'w', newline='') as csv_file:
        # create the csv writer
        writer = csv.writer(csv_file)
        # write the header
        writer.writerow(header_csv)
        for student in student_list:
            student_info = student.get_stu_id(), student.get_last_name(), student.get_first_name(), student.get_login(), student.get_email(), student.get_active()
            # write the Student info
            writer.writerow(student_info)

    header_txt = ['ID #', 'First Name', 'Last Name', 'Login', 'Active', 'Email']
    # open the text file to write
    with open("stu_accounts_txt.txt", 'w', newline='') as txt_file:
        # get the formatting details from the helper function
        fname_len, lname_len, email_len = get_lengths(student_list)
        # the magic numbers come from the set length of ID, login, and Active status
        title_len = 9 + fname_len + lname_len + 9 + 9 + email_len
        # print the Title, nicely formatted
        print(f"{'Student Login Information':^{title_len}}", file=txt_file)
        print(f"{'':-^{title_len}}", file=txt_file)
        # print the header, adding + 1 so theres a space between fields
        print(f"{header_txt[0]:<9}{header_txt[1]:<{fname_len + 1}}{header_txt[2]:<{lname_len + 1}}{header_txt[3]:<9}{header_txt[4]:<7}{header_txt[5]:<}", file=txt_file)
        # for student in the student list
        for student in student_list:
            # retrieve/print the student info
            student_info = student.get_stu_id(), student.get_last_name(), student.get_first_name(), student.get_login(), student.get_active(), student.get_email()
            print(f"{student_info[0]:<9}{student_info[1]:<{fname_len + 1}}{student_info[2]:<{lname_len + 1}}{student_info[3]:<9}{str(student_info[4]):<7}{student_info[5]:<}", file=txt_file)


def update_student_info(id, last, first):
    """Adds student added from add_student_record to StudentInfo.csv"""
    with open("StudentInfo.csv", "at", newline='') as csv_file:
        print(f"{last},{first},{id}", file=csv_file)


def add_student_record(student_list):
    """Adds student record, returns list of Student instances"""
    # while loop
    keep_going = True
    while keep_going:
        # bool for controlling flow
        valid_id = True
        # prompt for ID from user
        id = input("Enter new Student ID or 'q' to return to Main Menu: ")
        # q to return to main
        if id.lower() == 'q':
            return None
        else:
            # try to convert id to int
            try:
                id = int(id)
                # for each student in the list
                for student in student_list:
                    # if the id exists already
                    if id == int(student.get_stu_id()):
                        # tell the user and return to id input
                        print(f"{id} is already in use.\n")
                        valid_id = False
                        break
            # handle values other than 'q' and ints
            except ValueError:
                print("Please enter a valid integer\n")
                continue
            # append the new student to the student list
            if valid_id:
                fname = input("Enter the Student's first name: ")
                lname = input("Enter the Student's last name: ")
                update_student_info(id, lname, fname)
                student_list.append(student_class.Student(id, fname, lname))
                return student_list


def delete_student_record(student_list):
    """Sets a Student instance active attribute to False, returns a list of Student instances"""
    # while loop
    keep_going = True
    while keep_going:
        id_exists = False
        # prompt for id
        id = input("Enter Student ID for deletion or 'q' to return to Main Menu: ")
        # q to return to main
        if id.lower() == 'q':
            return None
        else:
            # try to convert id to int
            try:
                id = int(id)
                # for each student in the list
                for student in student_list:
                    # if the id exists already
                    if id == int(student.get_stu_id()):
                        id_exists = True
                        # set the student to inactive
                        student.set_active()
                if not id_exists:
                    # if the student isn't found
                    print("Student ID not found\n")
                    continue
                else:
                    print("Student deactivated")
            except ValueError:
                print("Please enter a valid integer\n")
                continue
        return student_list


def search_by_last_name(student_list):
    """Searches student list, prints instance if found"""
    # while loop
    keep_going = True
    while keep_going:
        lname_exists = False
        # prompt for last name
        lname = input("Enter Student last name to search for or 'q' to return to Main Menu: ")
        # q to return to main
        if lname.lower() == 'q':
            keep_going = False
        else:
            # for each student in the list
            for student in student_list:
                if lname == student.get_last_name():
                    lname_exists = True
            if lname_exists:
                # the student is found
                print()
                print(student)
                print()
            else:
                print("Student not found\n")
                continue


def search_by_id(student_list):
    """Searches student list, prints instance if found"""
    # while loop
    keep_going = True
    while keep_going:
        id_exists = False
        # prompt for id
        id = input("Enter Student ID for deletion or 'q' to return to Main Menu: ")
        # q to return to main
        if id.lower() == 'q':
            keep_going = False
        else:
            # try to convert id to int
            try:
                id = int(id)
                # for each student in the list
                for student in student_list:
                    if id == int(student.get_stu_id()):
                        id_exists = True
                        print()
                        print(student)
                        print()
                if not id_exists:
                    # if the student isn't found
                    print("Student not found\n")
                    continue
            except ValueError:
                print("Please enter a valid integer\n")
                continue
