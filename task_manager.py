# =====Importing Libraries===========

from datetime import date
from datetime import datetime
import os.path


# I could include functions for each read/write version of opening the file. - Reading, you only need to open once really. Writing different.


# =====Defining Functions===========


def reg_user():
    # This block gets the user to create a new profile by inputting a new username and password, checking that
    # they've entered the password correctly, and storing the user details in the user text file.
    # Only the 'admin' is allowed to register users.
    # The admin cannot create a username that already exists. It loops back to the start of the function if so.
    if input_name != "admin":
        print("\nOnly admins can create new users, please select a different option.\n")

    else:
        with open('user.txt', 'a+') as open_user_file:
            open_user_file.seek(0)  # Move file descriptor to start of the file (not end as standard in a+ mode)
            user_file_content = open_user_file.read()
            new_username = input("Create a new username: ")
            while new_username in user_file_content:
                new_username = input("\nThis username is taken. Please enter another username: \n")

            new_password = input("Create a password: ")
            password_check = input("Please confirm your password: ")

            if new_password != password_check:
                password_check = input("Your passwords don't match, please re-enter your password: ")

            open_user_file.write(f"\n{new_username}, {new_password}")

    print('\n✨ User created, thanks! ✨\n')


def add_task():
    # This block prompts the user to add a task, taking in the assignee, task, description of task, date due,
    # current date (for date inputted), status of task completion. It checks that the user is in the system before
    # proceeding with assigning the task. It writes all of this info to a new line in the task.txt file.

    assignee = input("\nEnter the assignee's username: ")

    if assignee not in user_names:
        assignee = input("\nThis username is not in the system, please enter a known user or create a new user: \n")
    else:
        pass

    task = str(input("Enter your task: "))

    task_description = str(input("Enter your task description: "))

    date_due = str(input("Enter the task due date (e.g. 10 October 2023): "))

    current_date = date.today()
    current_date = current_date.strftime("%d %B %Y")

    task_status = 'No'

    with open('tasks.txt', 'a+') as addto_task_file:
        addto_task_file.write(f"\n{assignee}, {task}, {task_description}, {date_due}, {current_date}, {task_status}")


def view_all():
    # This block reads all tasks in the file and presents them in a readable format. It uses a for loop to iterate
    # through the lines in the tasks file.

    task_num = 1
    with open('tasks.txt', 'r') as read_tasks_file:
        for line in read_tasks_file:
            rtf_line = line.split(", ")
            print(f"""
        -------------------[Task: {task_num}]--------------------
        Task:               {rtf_line[1]}
        Assigned to:        {rtf_line[0]}
        Date assigned:      {rtf_line[4]}
        Due date:           {rtf_line[3]}
        Task complete?      {rtf_line[-1]}
        Task description:   
            {rtf_line[2]}
        -----------------------------------------------\n""")
            task_num += 1


def view_mine():
    # This block reads each line in the tasks file and presents it to the user if the assignee matches
    # their username.

    task_num = 0
    my_tasks = []
    with open('tasks.txt', 'r') as read_tasks_file:
        print("\n=== MY TASKS ===")
        for line in read_tasks_file:
            rtf_line = line.split(", ")
            if input_name == rtf_line[0]:
                my_tasks.append(rtf_line)
                print(f"""
-------------------[Task: {task_num + 1}]---------------------
    Task:               {rtf_line[1]}
    Assigned to:        {rtf_line[0]}
    Date assigned:      {rtf_line[4]}
    Due date:           {rtf_line[3]}
    Task complete?      {rtf_line[-1]}
    Task description:   
        {rtf_line[2]}
-----------------------------------------------\n""")
                task_num += 1

    num_my_tasks = len(my_tasks)

    # DONE - Code to select a task or return to main menu
    # DONE - Allow the user to select either a specific task (by entering a number) or input ‘-1’ to return to the main menu.
    # o If the user selects a specific task, they should be able to choose to either mark the task as complete or edit the task.
    # If the user chooses to mark a task as complete, the ‘Yes’/’No’ value that describes whether the task has been completed or
    # not should be changed to ‘Yes’.
    # When the user chooses to edit a task, the username of the person to whom the task is assigned
    # or the due date of the task can be edited. The task can only be edited if it has not yet been completed.

    menu = int(input('''\nWould you like to:
    1  - Mark a task as complete
    2  - Edit a task assignee
    3  - Edit a task due date
    4  - Return to main menu
    : '''))

    if menu == 4:
        menu_selector()  # Back to main menu using menu_selector function.

    else:
        while menu not in [1, 2, 3, 4]:  # Error handling for invalid menu option
            menu = int(input("Option not in menu. Please select another option: \n"))
        user_selection = int(input("Select a task number: \n"))  # User selection for task number
        edited_tasks_content = ''  # Empty variable for edited tasks content to write back to file.

        while user_selection not in range(num_my_tasks + 1):  # Error handling for invalid task number input.
            user_selection = int(input("Task number does not exist. Please select a valid task number: \n"))

        if menu == 1:  # Menu choice. Code to mark task as complete follows
            r_tasks_file = open('tasks.txt', 'r')
            for line in r_tasks_file:
                split_line = line.split(', ')
                if split_line == my_tasks[user_selection - 1]:
                    split_line[-1] = "Yes" + "\n"  # Change last position to Yes from No
                split_line = ', '.join(split_line)  # Change line back into string
                edited_tasks_content += split_line  # Collate all edited strings
            with open('tasks.txt', 'w+') as write_tasks_file:
                write_tasks_file.write(edited_tasks_content)  # Write amended tasks to txt file."""
            print("\n✨ Saved as complete. ✨ \n")

        elif menu == 2:  # Code to change the assignee. Stops change if task is marked as complete already.
            r_tasks_file = open('tasks.txt', 'r')
            for line in r_tasks_file:
                split_line = line.split(', ')
                if split_line == my_tasks[user_selection - 1]:
                    if 'Yes' in split_line[-1]:
                        print(
                            "This task is already complete, you can't change the assignee.\n Choose another option from the menu:")
                        menu_selector()
                    else:
                        new_assignee = str(input("Enter the new assignee: \n")).lower()
                        split_line[0] = new_assignee
                split_line = ', '.join(split_line)  # Change line back into string
                edited_tasks_content += split_line  # Collate all edited strings
            with open('tasks.txt', 'w+') as write_tasks_file:
                write_tasks_file.write(edited_tasks_content)  # Write amended tasks to txt file."""
            print("\n✨ Assignee change. ✨ \n")
            r_tasks_file.close()

        elif menu == 3:  # Code to edit a task due date
            r_tasks_file = open('tasks.txt', 'r')
            for line in r_tasks_file:
                split_line = line.split(', ')
                if split_line == my_tasks[user_selection - 1]:
                    if 'Yes' in split_line[-1]:
                        print(
                            "This task is already complete, you can't edit it.\n Choose another option from the menu:")
                        menu_selector()
                    else:
                        new_due_date = input("Enter the new due date (e.g. 10 January 2023): \n")
                        split_line[-3] = new_due_date
                split_line = ', '.join(split_line)  # Change line back into string
                edited_tasks_content += split_line  # Collate all edited strings
            with open('tasks.txt', 'w+') as write_tasks_file:
                write_tasks_file.write(edited_tasks_content)  # Write amended tasks to txt file."""
            print("\n✨ Due date changed. ✨ \n")


def view_stats():
    # This block presents the stats (total number of tasks and users) to the admin. It does this by reding the
    # total number of lines in the tasks file (for number of tasks), and then by iterating through the lines in the
    # text file and adding the username if it's the first instance of. It then counts the number of user (for
    # total users).

    if os.path.exists('task_overview.txt') and os.path.exists(
            'user_overview.txt'):  # Check if both overview files exist (i.e. a report has been generated)/
        if os.stat("task_overview.txt").st_size == 0:  # If the file has been created but is empty, generate a report.
            generate_reports()
    else:
        generate_reports()  # Generate report files if the file doesn't exist at all.

    with open('task_overview.txt', 'r') as read_t_f:
        task_content = read_t_f.readlines()
        for line in task_content:
            line = line.replace('\n', '')
            print(line)

    with open('user_overview.txt', 'r') as read_u_f:
        user_content = read_u_f.readlines()
        for line in user_content:
            line = line.replace('\n', '')
            print(line)


def menu_selector():
    while True:
        if input_name == 'admin':
            # Presenting the admin menu to the user.
            menu = input('''\n=== MAIN MENU ===
Select one of the following options:
        
    g - Generate report
    s - Display stats 
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    e - Exit
    : ''').lower()

        else:
            # Presenting the menu to the user and making sure that the user input is converted to lower case.
            menu = input('''\n=== MAIN MENU ===
Select one of the following options:
            
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    e - Exit
    : ''').lower()

        if menu == 'r':
            # New code using reg_user(menu_choice) function.
            reg_user()

        elif menu == 'a':
            # New code using add_task() function.
            add_task()

        elif menu == 'va':
            # New code using view_all() function.
            view_all()

        elif menu == 'vm':
            # New code using view_mine() function.
            view_mine()

        elif menu == 'e':
            print('Goodbye!')
            exit()

        elif menu == 's':
            # New code using view_stats() function.
            view_stats()

        elif menu == 'g':
            generate_reports()
            # New code using generate_reports() function.

        else:
            print("You have made a wrong choice, Please try again")


def generate_reports():
    # Task overview report

    with open('tasks.txt', 'r') as read_tasks_file:
        tasks_file_content = read_tasks_file.readlines()

    # Total tasks
    total_tasks = len(tasks_file_content)

    # Report date
    current_date = date.today().strftime("%d %B %Y")

    # Total completed / uncompleted tasks
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    for line in tasks_file_content:
        split_line = line.split(', ')
        if 'Yes' in split_line[-1]:
            completed_tasks += 1
        else:
            uncompleted_tasks += 1
            task_due_date = split_line[-3]
            # Convert both dates into datetime format for comparison.
            obj_current_date = datetime.strptime(current_date, "%d %B %Y")
            obj_task_due_date = datetime.strptime(task_due_date, "%d %B %Y")
            if obj_task_due_date < obj_current_date:
                overdue_tasks += 1

    # Write overview report logic to task overview file.
    with open('task_overview.txt', 'w+') as write_task_overview_file:
        write_task_overview_file.write(f""" 
            -----------------------------------------------
                TASK OVERVIEW REPORT: {current_date}
        
                Total tasks:        | {total_tasks}
                    Completed:      | {completed_tasks}
                    Incomplete:     | {uncompleted_tasks}
                    Overdue:        | {overdue_tasks}
                    % Incomplete:   | {int((uncompleted_tasks / total_tasks) * 100)}%
                    % Overdue:      | {int((overdue_tasks / total_tasks) * 100)}%
        
            -----------------------------------------------
                """)

    # USER OVERVIEW REPORT

    with open('user.txt', 'r') as read_user_file:
        users = read_user_file.readlines()

        # Total users - this is a list of user strings with each user only appearing once.
        all_users = []

        for line in users:
            split_line = line.split(', ')  # Each line is now a list separated by ', '

            if split_line[0] not in all_users:
                all_users.append(split_line[0])
            else:
                pass

        total_users = len(all_users)

        write_user_overview_file = open('user_overview.txt', 'w+')
        new_file_content = (f""" 
            -----------------------------------------------
                USER OVERVIEW REPORT: {current_date}
        
                Total users:        | {total_users}
                Total tasks:        | {total_tasks}
                
                USER DETAILS:""")

    # LATEST ATTEMPT at printing stats for each user

    obj_current_date = datetime.strptime(current_date, "%d %B %Y")

    read_tasks_file = open('tasks.txt', 'r')

    user_stats_dict = {}  # Create an empty user dictionary

    for user in all_users:  # For loop to create a nested dictionary containing the stats for each user
        user_stats_dict[user] = {'Total tasks': 0,
                                 'Complete tasks': 0,
                                 'Incomplete tasks': 0,
                                 'Overdue tasks': 0,
                                 '% Complete': 0,
                                 '% Incomplete': 0,
                                 '% Overdue': 0, }

    for line in read_tasks_file:  # For loop to count tasks and add to dictionary for each user
        split_line = line.split(', ')
        current_user = split_line[0]
        user_stats_dict[current_user]['Total tasks'] += 1  # Counts total tasks and edits dictionary count for each user
        if 'No' in split_line[-1]:  # Check if task is complete
            user_stats_dict[current_user][
                'Incomplete tasks'] += 1  # Add 1 to incomplete tasks for current user (in dictionary).
            task_due_date = split_line[-3]  # For incomplete task, also check if overdue
            obj_task_due_date = datetime.strptime(task_due_date, "%d %B %Y")
            if obj_task_due_date < obj_current_date:
                user_stats_dict[current_user]['Overdue tasks'] += 1  # Add 1 to count of incomplete and overdue tasks
        elif 'Yes' in split_line[-1]:
            user_stats_dict[current_user]['Complete tasks'] += 1  # Add 1 to completed tasks if complete

    for user in all_users:  # For loop to calculate percentages now that all users have totals.
        try:
            user_stats_dict[user]['% Complete'] = int(
                user_stats_dict[user]['Complete tasks'] / user_stats_dict[user]['Total tasks'] * 100)
        except ZeroDivisionError:
            user_stats_dict[user]['% Complete'] = 0

        try:
            user_stats_dict[user]['% Incomplete'] = int(
                user_stats_dict[user]['Incomplete tasks'] / user_stats_dict[user]['Total tasks'] * 100)
        except ZeroDivisionError:
            user_stats_dict[user]['% Incomplete'] = 0

        try:
            user_stats_dict[user]['% Overdue'] = int(
                user_stats_dict[user]['Overdue tasks'] / user_stats_dict[user]['Total tasks'] * 100)
        except ZeroDivisionError:
            user_stats_dict[user]['% Overdue'] = 0

    for user in user_stats_dict:  # For loop to add each user overview to a string
        new_file_content += (f"""
        
        USER: {user}
        
        Total Tasks:                | {user_stats_dict[user]['Total tasks']}
            % of All Tasks:         | {int(user_stats_dict[user]['Total tasks'] / total_tasks * 100)}%
                
            Complete Tasks:         | {user_stats_dict[user]['Complete tasks']}
                % Complete:         | {user_stats_dict[user]['% Complete']}%
            Incomplete Tasks:       | {user_stats_dict[user]['Incomplete tasks']}
                % Incomplete:       | {user_stats_dict[user]['% Incomplete']}%
            Overdue Tasks:          | {user_stats_dict[user]['Overdue tasks']}
                % Overdue Tasks:    | {user_stats_dict[user]['% Overdue']}%
                    
        -----------------------------------------------""")

    read_tasks_file.close()

    with open('user_overview.txt', 'w+'):  # Write all user stats content (complete string) to the overview file.
        write_user_overview_file.write(new_file_content)

    print(f"\n✨ Report generated, please see text files. ✨\n")


# ====Login Section====

# Take username and password from user
print("\n==== WELCOME TO YOUR TASK MANAGER ====\n")
input_name = input("Enter your username: ")
input_password = input("Enter your password: ")

# Prepare existing user data for checks. Starting with creating and listing out the user file content
# and removing any unnecessary characters.

with open('user.txt', 'r') as read_user_file:
    all_user_file_content = read_user_file.read()

list_login_details = all_user_file_content.split()
for i in range(len(list_login_details)):
    list_login_details[i] = list_login_details[i].replace(',', '')

# Create empty variables for storing split out usernames and passwords.
user_names = []
passwords = []
name1 = ""
password1 = ""

# Loop through login details list and sort usernames and passwords.
while True:
    if len(list_login_details) > 0:
        name1 = list_login_details.pop(0)
        user_names.append(name1)
        password1 = list_login_details.pop(0)
        passwords.append(password1)
    else:
        break

# Logic to check if login details are correct. Checks if username and password are stored in relevant list.
# Then checks if username and password match using indexing. Asks user to re-enter details if incorrect.

username_index = 0
password_index = 0

while True:
    if input_name in user_names:
        username_index = user_names.index(input_name)
        pass
    else:
        input_name = input("Incorrect username, please re-enter: ")
        continue
    if input_password in passwords:
        password_index = passwords.index(input_password)
        pass
    else:
        input_password = input("Incorrect password, please re-enter: ")
        continue
    if user_names[username_index] == input_name and passwords[password_index] == input_password:
        print(f"\n✨ Login details correct. Welcome {input_name}! ✨\n")
        break
    else:
        input_password = input("Incorrect password, please re-enter: ")
        continue

menu_selector()
