# ===== Importing external modules ===========
from datetime import datetime
import re
import logging
import shutil
import os

# ===== File Path Constants =====
USER_FILE = "user.txt"
TASK_FILE = "task.txt"
TASK_OVERVIEW_FILE = "task_overview.txt"
USER_OVERVIEW_FILE = "user_overview.txt"
LOG_FILE = "task_manager.log"

# ===== Logging Configuration =====
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ===== User Class =====

class User:
    """
    Represents a user in the Task Manager system.
    Attributes:
        username (str): The user's unique username (3-20 alphanumeric + underscores)
        password (str): The user's password (minimum 6 characters)
        role (str): The user's role ('Admin' or 'Non-Admin')
    """
    
    def __init__(self, username, password, role):
        """
        Initialize a User object with username, password, and role.
        
        Args:
            username (str): The user's username
            password (str): The user's password
            role (str): The user's role ('Admin' or 'Non-Admin')
        """
        self.username = username
        self.password = password
        self.role = role
    
    def __str__(self):
        """
        Return string representation of the user.
        Format: username, password, role
        """
        return f"{self.username}, {self.password}, {self.role}"
    
    def display_info(self):
        """
        Display user information in formatted tabular output.
        """
        print(f"  {'Username':<30} | {self.username}")
        print(f"  {'Role':<30} | {self.role}")
        print("  " + "-" * 76)





# ===== Validation Functions =====

def validate_username(username):
    """
    Validate username format.
    Username must be 3-20 characters and contain only alphanumeric characters and underscores.
    Returns: (is_valid, error_message)
    """
    if not username:
        return False, "Username cannot be empty."
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 20:
        return False, "Username must be no more than 20 characters long."
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, ""


def validate_password(password):
    """
    Validate password strength.
    Password must be at least 6 characters long.
    Returns: (is_valid, error_message)
    """
    if not password:
        return False, "Password cannot be empty."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


def validate_date_format(date_string):
    """
    Validate date format (YYYY-MM-DD).
    Returns: (is_valid, error_message)
    """
    if not date_string:
        return False, "Date cannot be empty."
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."


def validate_due_date(date_string):
    """
    Validate due date is in correct format and not in the past.
    Returns: (is_valid, error_message)
    """
    is_valid, error_msg = validate_date_format(date_string)
    if not is_valid:
        return False, error_msg
    
    try:
        due_date = datetime.strptime(date_string, "%Y-%m-%d").date()
        if due_date < datetime.now().date():
            return False, "Due date cannot be in the past."
        return True, ""
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."


def validate_non_empty(input_string, field_name):
    """
    Validate that input is not empty.
    Returns: (is_valid, error_message)
    """
    if not input_string or not input_string.strip():
        return False, f"{field_name} cannot be empty."
    return True, ""


def validate_role(role):
    """
    Validate that role is either 'Admin' or 'Non-Admin'.
    Returns: (is_valid, error_message)
    """
    valid_roles = ['admin', 'non-admin']
    if role.lower() not in valid_roles:
        return False, "Role must be either 'Admin' or 'Non-Admin'."
    return True, ""


def get_validated_input(prompt, validator_func, field_name):
    """
    Helper function to get validated input from user.
    Repeatedly prompts until valid input is provided.
    
    Args:
        prompt (str): The input prompt to display
        validator_func: Validation function that returns (is_valid, error_message)
        field_name (str): Field name for error messages
    
    Returns:
        str: Valid user input
    """
    while True:
        user_input = input(prompt).strip()
        is_valid, error_msg = validator_func(user_input, field_name) if field_name else validator_func(user_input)
        if not is_valid:
            print(f"Error: {error_msg}")
            continue
        return user_input


def handle_file_error(operation, error):
    """
    Helper function to handle and display file I/O errors.
    
    Args:
        operation (str): Description of the operation that failed
        error: The exception that was raised
    """
    print_header("ERROR")
    print(f"  Error {operation}: {error}")
    print()
    logging.error(f"File operation failed - {operation}: {error}")


def user_exists(username):
    """
    Check if username exists in user.txt.
    
    Args:
        username (str): Username to check
        
    Returns:
        bool: True if user exists, False otherwise
    """
    try:
        with open(USER_FILE, "r") as user_file:
            for line in user_file:
                existing_user = line.strip().split(", ")[0]
                if existing_user == username:
                    return True
        return False
    except FileNotFoundError:
        return False


def backup_file(filename):
    """
    Create timestamped backup of file before destructive operations.
    
    Args:
        filename (str): File to backup
        
    Returns:
        bool: True if backup successful, False otherwise
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filename}.backup_{timestamp}"
        shutil.copy2(filename, backup_name)
        logging.info(f"Backup created: {backup_name}")
        return True
    except Exception as e:
        logging.error(f"Backup failed for {filename}: {e}")
        return False


def login_user():
    """
    Authenticate a user by username and password.
    Returns: User object if authentication successful, None otherwise.
    """
    print_header("USER LOGIN")
    
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ")
    
    try:
        with open(USER_FILE, "r") as user_file:
            for line in user_file:
                user_data = line.strip().split(", ")
                if len(user_data) == 3:
                    file_username, file_password, role = user_data
                    if file_username == username and file_password == password:
                        user = User(file_username, file_password, role)
                        print_header("SUCCESS")
                        print(f"  Welcome, {user.username}!")
                        print(f"  Role: {user.role}")
                        print()
                        logging.info(f"User {username} logged in successfully")
                        return user
        
        # Authentication failed
        print_header("ERROR")
        print("  Invalid username or password. Please try again.")
        print()
        logging.warning(f"Failed login attempt for username: {username}")
        return None
    except FileNotFoundError:
        print_header("ERROR")
        print("  No users found. Please register first.")
        print()
        return None
    except IOError as e:
        print_header("ERROR")
        print(f"  Error during login: {e}")
        print()
        logging.error(f"Login error: {e}")
        return None


# ===== Function Definitions =====

def print_header(title):
    """
    Print a formatted header for sections.
    """
    print("\n" + "=" * 80)
    print(f"  {title.center(76)}")
    print("=" * 80)


def verify_and_update_user_roles():
    """
    Check all existing users in user.txt for missing roles.
    For users without roles (old format: username, password),
    prompt to assign them a role and update the file.
    """
    try:
        with open(USER_FILE, "r") as user_file:
            lines = user_file.readlines()
        
        needs_update = False
        updated_lines = []
        
        print_header("USER ROLE VERIFICATION")
        
        for line in lines:
            user_data = line.strip().split(", ")
            
            # Check if user has a role (3 fields) or not (2 fields)
            if len(user_data) == 2:
                # Old format: username, password (no role)
                username, password = user_data
                needs_update = True
                
                print(f"\n  User '{username}' found without a role assignment.")
                
                # Ask user to assign role
                while True:
                    print(f"  Assign role for '{username}':")
                    print("    1 - Admin")
                    print("    2 - Non-Admin")
                    role_choice = input("  Enter your choice (1 or 2): ").strip()
                    
                    if role_choice == "1":
                        role = "Admin"
                        break
                    elif role_choice == "2":
                        role = "Non-Admin"
                        break
                    else:
                        print("  Error: Invalid choice. Please enter 1 or 2.")
                
                # Create updated user entry with role
                updated_user = User(username, password, role)
                updated_lines.append(str(updated_user) + "\n")
                print(f"  ✓ Role '{role}' assigned to '{username}'.")
                logging.info(f"Role '{role}' assigned to user '{username}'")
                
            elif len(user_data) == 3:
                # New format: username, password, role (already has role)
                updated_lines.append(line)
        
        # If updates were made, save the updated file
        if needs_update:
            backup_file(USER_FILE)
            with open(USER_FILE, "w") as user_file:
                user_file.writelines(updated_lines)
            print_header("SUCCESS")
            print("  All users have been updated with roles!")
            print()
        else:
            if lines:
                print("  All existing users already have roles assigned.")
                print()
    
    except FileNotFoundError:
        # No user.txt file exists yet, which is fine
        pass
    except IOError as e:
        print_header("ERROR")
        print(f"  Error updating user roles: {e}")
        print()
        logging.error(f"Error updating user roles: {e}")


def register_user():
    """
    Register a new user by collecting username, password, and role.
    Creates a User object and saves it to user.txt with hashed password.
    Validates username format, password strength, and role selection.
    Checks for duplicate usernames before saving.
    """
    # Get and validate username
    while True:
        username = input("Enter a username: ").strip()
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            print(f"Error: {error_msg}")
            continue
        # Check if username already exists
        username_exists = False
        try:
            with open(USER_FILE, "r") as user_file:
                for line in user_file:
                    existing_user = line.strip().split(", ")[0]
                    if existing_user == username:
                        username_exists = True
                        break
        except FileNotFoundError:
            pass  # File doesn't exist yet, so username is unique
        if username_exists:
            print(f"Error: Username '{username}' already exists. Please try a different username.")
            continue
        else:
            break  # Username is unique, proceed
    
    # Get and validate password
    while True:
        password = input("Enter a password: ")
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            print(f"Error: {error_msg}")
            continue
        break
    
    # Get and validate password confirmation
    while True:
        confirm_password = input("Confirm your password: ")
        if password == confirm_password:
            break
        else:
            print("Error: Passwords do not match. Please try again.")
    
    # Get and validate role
    while True:
        print("\n  Select user role:")
        print("    1 - Admin")
        print("    2 - Non-Admin")
        role_choice = input("  Enter your choice (1 or 2): ").strip()
        
        if role_choice == "1":
            role = "Admin"
            break
        elif role_choice == "2":
            role = "Non-Admin"
            break
        else:
            print("Error: Invalid choice. Please enter 1 or 2.")
    
    # Create User object with plain text password
    new_user = User(username, password, role)
    try:
        with open(USER_FILE, "a") as user_file:
            user_file.write(str(new_user) + "\n")
        print_header("SUCCESS")
        print(f"  User '{new_user.username}' successfully created!")
        print(f"  Role: {new_user.role}")
        print()
        logging.info(f"New user registered: {username} with role {role}")
    except IOError as e:
        handle_file_error("saving user", e)


def get_next_task_id():
    """
    Get the next available task ID by reading the task.txt file.
    Handles gaps from deletions by finding the maximum existing ID.
    Returns the next sequential ID (max_id + 1)
    """
    try:
        with open(TASK_FILE, "r") as task_file:
            max_id = 0
            for line in task_file:
                task_data = line.strip().split(", ")
                if len(task_data) == 7:
                    try:
                        task_id = int(task_data[0])
                        max_id = max(max_id, task_id)
                    except ValueError:
                        continue
            return max_id + 1
    except FileNotFoundError:
        return 1


def add_task():
    """
    Create a new task and assign it to a user.
    Validates all inputs before saving to task.txt.
    Checks that assigned user exists and due date is not in the past.
    Format: task_id, username, title, description, due_date, assigned_date, complete
    """
    # Validate task username exists
    while True:
        task_username = get_validated_input("Enter the username to assign the task to: ", validate_non_empty, "Username")
        if not user_exists(task_username):
            print(f"Error: User '{task_username}' does not exist. Please enter a valid username.")
            continue
        break
    
    task_title = get_validated_input("Enter the task title: ", validate_non_empty, "Task title")
    task_description = get_validated_input("Enter the task description: ", validate_non_empty, "Task description")
    task_due_date = get_validated_input("Enter the due date (YYYY-MM-DD): ", validate_due_date, None)
    
    # Get next task ID and save
    task_id = get_next_task_id()
    current_date = datetime.now().strftime("%Y-%m-%d")
    task_complete = "No"
    
    try:
        with open(TASK_FILE, "a") as task_file:
            task_file.write(f"{task_id}, {task_username}, {task_title}, {task_description}, {task_due_date}, {current_date}, {task_complete}\n")
        print_header("SUCCESS")
        print(f"  Task '{task_title}' successfully added!")
        print(f"  Task ID: {task_id}")
        print(f"  Assigned to: {task_username}")
        print()
        logging.info(f"Task created - ID: {task_id}, Title: {task_title}, Assigned to: {task_username}")
    except IOError as e:
        handle_file_error("saving task", e)


def display_task(task_id, username, title, description, due_date, assigned_date, complete):
    """
    Display a single task in formatted tabular output.
    Helper function to reduce code duplication.
    """
    print(f"  {'Task ID':<20} | {task_id}")
    print(f"  {'Username':<20} | {username}")
    print(f"  {'Task Title':<20} | {title}")
    print(f"  {'Description':<20} | {description}")
    print(f"  {'Due Date':<20} | {due_date}")
    print(f"  {'Assigned Date':<20} | {assigned_date}")
    print(f"  {'Status':<20} | {complete}")
    print("  " + "-" * 76)


def display_task_for_user(task_id, username, title, description, due_date, assigned_date, complete):
    """
    Display a task for the user's own view (excludes username field).
    Helper function for view_my_tasks() in formatted tabular output.
    """
    print(f"  {'Task ID':<20} | {task_id}")
    print(f"  {'Task Title':<20} | {title}")
    print(f"  {'Description':<20} | {description}")
    print(f"  {'Due Date':<20} | {due_date}")
    print(f"  {'Assigned Date':<20} | {assigned_date}")
    print(f"  {'Status':<20} | {complete}")
    print("  " + "-" * 76)


def read_all_tasks():
    """
    Read all tasks from file and return as list of tuples.
    Returns: List of 7-tuples (task_id, username, title, description, due_date, assigned_date, complete)
    """
    try:
        with open(TASK_FILE, "r") as task_file:
            tasks = []
            for line in task_file:
                task_data = line.strip().split(", ")
                if len(task_data) == 7:
                    tasks.append(tuple(task_data))
            return tasks
    except FileNotFoundError:
        return []


def write_all_tasks(tasks):
    """
    Write all tasks back to file.
    
    Args:
        tasks: List of 7-tuples to write
    """
    try:
        with open(TASK_FILE, "w") as task_file:
            for task_data in tasks:
                if len(task_data) == 7:
                    line = ", ".join(task_data) + "\n"
                    task_file.write(line)
    except IOError as e:
        handle_file_error("writing tasks", e)


def view_all_tasks():
    """
    Read and display all tasks from task.txt in formatted tabular manner.
    Parses each line and validates it has all 7 required fields (including task_id).
    Handles file I/O errors gracefully.
    """
    try:
        tasks = read_all_tasks()
        
        if len(tasks) == 0:
            print_header("ALL TASKS")
            print("  No tasks found.")
            print()
        else:
            print_header("ALL TASKS")
            for task_id, username, title, description, due_date, assigned_date, complete in tasks:
                display_task(task_id, username, title, description, due_date, assigned_date, complete)
            print(f"  Total tasks: {len(tasks)}")
            print()
    except IOError as e:
        print_header("ERROR")
        print(f"  Error reading tasks: {e}")
        print()
        logging.error(f"Error reading tasks: {e}")


def view_all_users():
    """
    Read and display all registered users from user.txt in formatted tabular manner.
    Creates User objects from file data and displays them.
    Handles file I/O errors gracefully.
    """
    try:
        with open(USER_FILE, "r") as user_file:
            users = []
            for line in user_file:
                user_data = line.strip().split(", ")
                if len(user_data) == 3:
                    username, password, role = user_data
                    user = User(username, password, role)
                    users.append(user)
            
            if len(users) == 0:
                print_header("ALL USERS")
                print("  No users found.")
                print()
            else:
                print_header("ALL USERS")
                for user in users:
                    user.display_info()
                print(f"  Total users: {len(users)}")
                print()
    except FileNotFoundError:
        print_header("ALL USERS")
        print("  No users found.")
        print()
    except IOError as e:
        print_header("ERROR")
        print(f"  Error reading users: {e}")
        print()
        logging.error(f"Error reading users: {e}")


def get_valid_task_number(user_tasks):
    """
    Recursive function to get a valid task ID from the user.
    Base case: User enters -1 to return to main menu.
    Recursive case: If user enters invalid task ID or non-integer, recursively call until valid.
    
    Args:
        user_tasks: List of task tuples assigned to the user
        
    Returns:
        task_id (str) or None: Valid task ID or None if user enters -1
    """
    task_id_input = input("  Enter a task ID to update its status/edit (or enter -1 to return): ").strip()
    
    # Base case: User enters -1 to return to main menu
    if task_id_input == "-1":
        return None
    
    # Empty input: Skip
    if not task_id_input:
        return None
    
    # Validate that input is an integer
    try:
        int(task_id_input)
    except ValueError:
        print(f"  Error: '{task_id_input}' is not a valid integer. Please enter a task ID or -1 to return.")
        # Recursive call for invalid input
        return get_valid_task_number(user_tasks)
    
    # Check if task ID exists in user's tasks
    for task_id, _, _, _, _, _, _ in user_tasks:
        if task_id == task_id_input:
            return task_id_input
    
    # Task ID not found: Recursive call
    print(f"  Error: Task ID '{task_id_input}' not found in your tasks.")
    return get_valid_task_number(user_tasks)


def view_my_tasks():
    """
    Display only tasks assigned to the specified user.
    Allows user to select a task by ID to view details, update completion status, or edit task details.
    Tasks can only be edited if they have not been completed.
    Uses recursive function get_valid_task_number() for task selection.
    """
    my_username = get_validated_input("Enter your username: ", validate_non_empty, "Username")
    
    try:
        all_tasks = read_all_tasks()
        user_tasks = [t for t in all_tasks if t[1] == my_username]
        
        print_header(f"MY TASKS - {my_username.upper()}")
        
        if len(user_tasks) == 0:
            print(f"  No tasks found for user '{my_username}'.")
            print()
            return
        
        # Display all user tasks
        for task_id, username, title, description, due_date, assigned_date, complete in user_tasks:
            display_task_for_user(task_id, username, title, description, due_date, assigned_date, complete)
        print(f"  Total tasks assigned to you: {len(user_tasks)}")
        print()
        
        # Allow user to select a task for status update or editing
        while True:
            # Use recursive function to get valid task number
            task_id_selection = get_valid_task_number(user_tasks)
            
            # Base case: User entered -1 to return to main menu
            if task_id_selection is None:
                break
            
            # Find the selected task
            selected_task = None
            for task_id, username, title, description, due_date, assigned_date, complete in user_tasks:
                if task_id == task_id_selection:
                    selected_task = (task_id, username, title, description, due_date, assigned_date, complete)
                    break
            
            # Display task action menu
            task_id, username, title, description, due_date, assigned_date, complete = selected_task
            print_header(f"TASK OPTIONS - {title}")
            print(f"  Current Status: {complete}")
            print()
            
            action_menu = input(
                "  What would you like to do?\n"
                "    1 - Mark as complete/incomplete\n"
                "    2 - Edit task (reassign or change due date)\n"
                "    3 - Back to task list\n"
                "  Enter your choice: "
            ).strip()
            
            if action_menu == '1':
                # Update completion status
                new_status = "No" if complete == "Yes" else "Yes"
                # Update the task in the file
                try:
                    all_file_tasks = read_all_tasks()
                    updated_tasks = []
                    for task_tuple in all_file_tasks:
                        tid, uname, ttitle, tdesc, tdue, tassigned, tstatus = task_tuple
                        if tid == task_id:
                            tstatus = new_status
                        updated_tasks.append((tid, uname, ttitle, tdesc, tdue, tassigned, tstatus))
                    
                    write_all_tasks(updated_tasks)
                    
                    print_header("SUCCESS")
                    print(f"  Task '{title}' has been marked as {'complete' if new_status == 'Yes' else 'incomplete'}!")
                    print()
                    logging.info(f"Task ID {task_id} status updated to {new_status}")
                except IOError as e:
                    handle_file_error("updating task status", e)
            
            elif action_menu == '2':
                # Edit task (only if not completed)
                if complete.strip().lower() == "yes":
                    print_header("ERROR")
                    print("  Cannot edit a completed task. Please mark it as incomplete first.")
                    print()
                else:
                    print_header("EDIT TASK")
                    print(f"  Task: {title}")
                    print(f"  Current Assigned User: {username}")
                    print(f"  Current Due Date: {due_date}")
                    print()
                    
                    # Ask which fields to edit
                    edit_options = input(
                        "  What would you like to edit?\n"
                        "    1 - Change assigned user only\n"
                        "    2 - Change due date only\n"
                        "    3 - Change both assigned user and due date\n"
                        "    4 - Cancel (back to task list)\n"
                        "  Enter your choice: "
                    ).strip()
                    
                    new_username = username
                    new_due_date = due_date
                    
                    if edit_options in ['1', '3']:
                        # Edit assigned user
                        new_username = get_validated_input(
                            "  Enter new username to assign this task to: ",
                            validate_non_empty,
                            "Username"
                        )
                    
                    if edit_options in ['2', '3']:
                        # Edit due date
                        new_due_date = get_validated_input(
                            "  Enter new due date (YYYY-MM-DD): ",
                            validate_date_format,
                            None
                        )
                    
                    if edit_options in ['1', '2', '3']:
                        # Update the task in the file
                        try:
                            all_file_tasks = read_all_tasks()
                            updated_tasks = []
                            task_updated = False
                            
                            for task_tuple in all_file_tasks:
                                tid, uname, ttitle, tdesc, tdue, tassigned, tstatus = task_tuple
                                if tid == task_id:
                                    uname = new_username
                                    tdue = new_due_date
                                    task_updated = True
                                updated_tasks.append((tid, uname, ttitle, tdesc, tdue, tassigned, tstatus))
                            
                            if task_updated:
                                write_all_tasks(updated_tasks)
                                
                                print_header("SUCCESS")
                                print(f"  Task '{title}' has been updated!")
                                if new_username != username:
                                    print(f"  New Assigned User: {new_username}")
                                if new_due_date != due_date:
                                    print(f"  New Due Date: {new_due_date}")
                                print()
                                logging.info(f"Task ID {task_id} updated - User: {new_username}, Due: {new_due_date}")
                                
                                # Reload tasks for the current user
                                all_tasks = read_all_tasks()
                                user_tasks = [t for t in all_tasks if t[1] == my_username]
                                
                                # Re-display tasks
                                print_header(f"MY TASKS - {my_username.upper()}")
                                if len(user_tasks) == 0:
                                    print(f"  No tasks found for user '{my_username}'.")
                                else:
                                    for t_id, t_user, t_title, t_desc, t_due, t_assigned, t_complete in user_tasks:
                                        display_task_for_user(t_id, t_user, t_title, t_desc, t_due, t_assigned, t_complete)
                                    print(f"  Total tasks assigned to you: {len(user_tasks)}")
                                print()
                        except IOError as e:
                            handle_file_error("updating task", e)
            
            elif action_menu == '3':
                # Back to task list
                break
            else:
                print("  Error: Invalid choice. Please enter 1, 2, or 3.")
            
            # Ask if user wants to select another task
            another = input("  Select another task? (y/n): ").strip().lower()
            if another != 'y':
                break
    
    except FileNotFoundError:
        print_header(f"MY TASKS - {my_username.upper()}")
        print("  No tasks found.")
        print()
    except IOError as e:
        handle_file_error("reading tasks", e)


# ...existing code...

def display_menu():
    print_header("MAIN MENU")
    menu = input(
        '''  r - Register a user
  a - Add task
  va - View all tasks
  vm - View my tasks
  vu - View all users
  vr - Verify and update user roles
  gr - Generate reports
  ds - Display statistics
  e - Exit

  Enter your choice: '''
    ).lower()
    return menu

def display_admin_menu():
    print_header(f"ADMIN MENU")
    menu = input(
        '''  r - Register a user (Admin only)
  a - Add task
  va - View all tasks
  vm - View my tasks
  vu - View all users (Admin only)
  vr - Verify and update user roles (Admin only)
  dt - Delete task (Admin only)
  vc - View completed tasks (Admin only)
  uc - Update task completion status
  rc - Reset completed task to incomplete (Admin only)
  gr - Generate reports
  ds - Display statistics
  lo - Logout
  e - Exit

  Enter your choice: '''
    ).lower()
    return menu

def display_non_admin_menu():
    print_header(f"USER MENU")
    menu = input(
        '''  a - Add task
  va - View all tasks
  vm - View my tasks
  uc - Update task completion status
  gr - Generate reports
  ds - Display statistics
  lo - Logout
  e - Exit

  Enter your choice: '''
    ).lower()
    return menu


def generate_reports():
    """
    Generate task_overview.txt and user_overview.txt reports.
    Creates comprehensive statistics about tasks and users in the system.
    """
    try:
        # Read all tasks
        tasks = read_all_tasks()
        
        # Calculate task statistics
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t[6].strip().lower() == "yes")
        incomplete_tasks = total_tasks - completed_tasks
        
        # Check overdue incomplete tasks
        current_date = datetime.now().date()
        overdue_tasks = 0
        for task in tasks:
            if task[6].strip().lower() == "no":
                try:
                    due_date = datetime.strptime(task[4], "%Y-%m-%d").date()
                    if due_date < current_date:
                        overdue_tasks += 1
                except ValueError:
                    continue
        
        # Calculate percentages
        incomplete_pct = (incomplete_tasks / total_tasks * 100) if total_tasks > 0 else 0
        overdue_pct = (overdue_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Write task_overview.txt
        with open(TASK_OVERVIEW_FILE, "w") as report:
            report.write("=" * 70 + "\n")
            report.write("TASK OVERVIEW REPORT\n")
            report.write("=" * 70 + "\n\n")
            report.write(f"Total number of tasks tracked: {total_tasks}\n")
            report.write(f"Total number of completed tasks: {completed_tasks}\n")
            report.write(f"Total number of uncompleted tasks: {incomplete_tasks}\n")
            report.write(f"Total number of uncompleted and overdue tasks: {overdue_tasks}\n")
            report.write(f"Percentage of incomplete tasks: {incomplete_pct:.2f}%\n")
            report.write(f"Percentage of overdue tasks: {overdue_pct:.2f}%\n")
            report.write("=" * 70 + "\n")
        
        # Generate user_overview.txt
        with open(USER_FILE, "r") as user_file:
            users = []
            for line in user_file:
                user_data = line.strip().split(", ")
                if len(user_data) == 3:
                    users.append(user_data[0])
        
        total_users = len(users)
        
        with open(USER_OVERVIEW_FILE, "w") as report:
            report.write("=" * 70 + "\n")
            report.write("USER OVERVIEW REPORT\n")
            report.write("=" * 70 + "\n\n")
            report.write(f"Total number of users registered: {total_users}\n")
            report.write(f"Total number of tasks tracked: {total_tasks}\n")
            report.write("\n" + "-" * 70 + "\n")
            report.write("USER TASK STATISTICS:\n")
            report.write("-" * 70 + "\n\n")
            
            for user in users:
                user_tasks = [t for t in tasks if t[1] == user]
                user_task_count = len(user_tasks)
                user_completed = sum(1 for t in user_tasks if t[6].strip().lower() == "yes")
                user_incomplete = user_task_count - user_completed
                user_overdue = sum(1 for t in user_tasks if t[6].strip().lower() == "no" and 
                                  datetime.strptime(t[4], "%Y-%m-%d").date() < current_date)
                
                user_task_pct = (user_task_count / total_tasks * 100) if total_tasks > 0 else 0
                user_completed_pct = (user_completed / user_task_count * 100) if user_task_count > 0 else 0
                user_incomplete_pct = (user_incomplete / user_task_count * 100) if user_task_count > 0 else 0
                user_overdue_pct = (user_overdue / user_task_count * 100) if user_task_count > 0 else 0
                
                report.write(f"User: {user}\n")
                report.write(f"  Total tasks assigned: {user_task_count}\n")
                report.write(f"  Percentage of total tasks: {user_task_pct:.2f}%\n")
                report.write(f"  Percentage of assigned tasks completed: {user_completed_pct:.2f}%\n")
                report.write(f"  Percentage of assigned tasks incomplete: {user_incomplete_pct:.2f}%\n")
                report.write(f"  Percentage of assigned tasks overdue: {user_overdue_pct:.2f}%\n")
                report.write("\n")
            
            report.write("=" * 70 + "\n")
        
        print_header("SUCCESS")
        print("  Reports generated successfully!")
        print(f"  - {TASK_OVERVIEW_FILE}")
        print(f"  - {USER_OVERVIEW_FILE}")
        print()
        logging.info("Reports generated successfully")
        
    except FileNotFoundError:
        print_header("ERROR")
        print("  No task file found.")
        print()
        logging.error("Reports generation failed - task file not found")
    except Exception as e:
        handle_file_error("generating reports", e)


def display_statistics():
    """
    Display statistics from report files in user-friendly format.
    Generates reports if they don't exist first.
    """
    # Generate reports if they don't exist
    if not os.path.exists(TASK_OVERVIEW_FILE) or not os.path.exists(USER_OVERVIEW_FILE):
        print("  Report files not found. Generating reports first...\n")
        generate_reports()
    
    try:
        # Read and display task_overview.txt
        print_header("TASK OVERVIEW STATISTICS")
        with open(TASK_OVERVIEW_FILE, "r") as report:
            print(report.read())
        
        # Read and display user_overview.txt
        print_header("USER OVERVIEW STATISTICS")
        with open(USER_OVERVIEW_FILE, "r") as report:
            print(report.read())
            
        logging.info("Statistics displayed successfully")
            
    except FileNotFoundError:
        print_header("ERROR")
        print("  Report files not found. Please try generating reports again.")
        print()
        logging.error("Statistics display failed - report files not found")
    except Exception as e:
        handle_file_error("reading reports", e)


def update_task_complete():
    """
    Update the task completion status from 'No' to 'Yes' using task ID.
    Allows both admin and non-admin users to mark their tasks as complete.
    Prompts for task ID to identify which task to update.
    """
    print_header("MARK TASK AS COMPLETE")
    task_id = get_validated_input("Enter the task ID to mark as complete: ", validate_non_empty, "Task ID")
    
    try:
        tasks = read_all_tasks()
        
        task_found = False
        updated_tasks = []
        
        for task_data in tasks:
            tid, username, title, description, due_date, assigned_date, complete = task_data
            
            if tid == task_id:
                complete = "Yes"
                task_found = True
                print_header("SUCCESS")
                print(f"  Task ID {task_id} ('{title}') has been marked as complete!")
                print()
                logging.info(f"Task ID {task_id} marked as complete")
            
            updated_tasks.append((tid, username, title, description, due_date, assigned_date, complete))
        
        if task_found:
            write_all_tasks(updated_tasks)
        else:
            print_header("ERROR")
            print(f"  Task ID '{task_id}' not found.")
            print()
    
    except IOError as e:
        handle_file_error("updating task", e)


def reset_task_incomplete():
    """
    Reset a completed task back to incomplete status (Admin only) using task ID.
    Changes task_complete attribute from 'Yes' to 'No'.
    Prompts for task ID to identify which task to reset.
    """
    print_header("RESET TASK TO INCOMPLETE")
    task_id = get_validated_input("Enter the task ID to reset to incomplete: ", validate_non_empty, "Task ID")
    
    try:
        all_tasks = read_all_tasks()
        task_found = False
        updated_tasks = []
        
        for task_tuple in all_tasks:
            tid, username, title, description, due_date, assigned_date, complete = task_tuple
            
            if tid == task_id:
                if complete.strip().lower() == "yes":
                    complete = "No"
                    task_found = True
                    print_header("SUCCESS")
                    print(f"  Task ID {task_id} ('{title}') has been reset to incomplete!")
                    print()
                    logging.info(f"Task ID {task_id} reset to incomplete")
                else:
                    print_header("INFO")
                    print(f"  Task ID {task_id} ('{title}') is already incomplete.")
                    print()
            
            updated_tasks.append((tid, username, title, description, due_date, assigned_date, complete))
        
        if task_found:
            write_all_tasks(updated_tasks)
        
        if not task_found:
            print_header("ERROR")
            print(f"  Task ID '{task_id}' not found.")
            print()
            logging.warning(f"Attempt to reset non-existent task ID {task_id}")
    
    except FileNotFoundError:
        print_header("ERROR")
        print("  No tasks found.")
        print()
        logging.error("Task file not found when resetting incomplete")
    except IOError as e:
        handle_file_error("resetting task", e)


def delete_task():
    """
    Delete a task from task.txt (Admin only).
    Prompts for task ID or task title to identify and delete the task.
    Creates backup before deletion.
    """
    print_header("DELETE TASK")
    
    task_identifier = input("Enter the task ID or task title to delete: ").strip()
    
    try:
        backup_file(TASK_FILE)
        tasks = read_all_tasks()
        
        found = False
        deleted_task_info = ""
        updated_tasks = []
        
        for task_data in tasks:
            task_id, username, title, description, due_date, assigned_date, complete = task_data
            # Match by task ID or task title
            if task_id == task_identifier or title == task_identifier:
                found = True
                deleted_task_info = f"Task ID {task_id} ('{title}')"
                continue
            updated_tasks.append(task_data)
        
        if found:
            write_all_tasks(updated_tasks)
            print_header("SUCCESS")
            print(f"  {deleted_task_info} has been deleted.")
            print()
            logging.info(f"Task deleted - {deleted_task_info}")
        else:
            print_header("ERROR")
            print(f"  Task '{task_identifier}' not found.")
            print()
    except Exception as e:
        handle_file_error("deleting task", e)


def view_completed_tasks():
    """
    View all completed tasks (Admin only).
    Displays tasks with 'Yes' completion status.
    """
    try:
        tasks = read_all_tasks()
        completed_tasks = [t for t in tasks if t[6].strip().lower() == "yes"]
        
        print_header("COMPLETED TASKS")
        
        if len(completed_tasks) == 0:
            print("  No completed tasks found.")
        else:
            for task_id, username, title, description, due_date, assigned_date, complete in completed_tasks:
                display_task(task_id, username, title, description, due_date, assigned_date, complete)
            print(f"  Total completed tasks: {len(completed_tasks)}")
        print()
    except IOError as e:
        print_header("ERROR")
        print(f"  Error reading tasks: {e}")
        print()
        logging.error(f"Error reading completed tasks: {e}")


def main():
    """
    Main program loop with role-based access control.
    Admin users have full access to all features.
    Non-Admin users have limited access (add task, view my tasks only).
    """
    print_header("WELCOME TO TASK MANAGER")
    
    # Verify and update existing users with roles on startup
    verify_and_update_user_roles()
    
    while True:
        # Login loop
        while True:
            current_user = login_user()
            if current_user:
                break
        
        # User session loop
        user_logged_in = True
        while user_logged_in:
            # Display menu based on user role
            if current_user.role.lower() == "admin":
                menu = display_admin_menu()
            else:
                menu = display_non_admin_menu()
            
            if menu == 'r':
                # Register user - Admin only
                if current_user.role.lower() == "admin":
                    print_header("REGISTER NEW USER")
                    register_user()
                else:
                    print("\n  ERROR: Only Admin users can register new users.\n")
            
            elif menu == 'a':
                # Add task - Available to all
                print_header("ADD NEW TASK")
                add_task()
            
            elif menu == 'va':
                # View all tasks - Now available to all users
                view_all_tasks()
            
            elif menu == 'vm':
                # View my tasks - Available to all
                view_my_tasks()
            
            elif menu == 'vu':
                # View all users - Admin only
                if current_user.role.lower() == "admin":
                    view_all_users()
                else:
                    print("\n  ERROR: Only Admin users can view all users.\n")
            
            elif menu == 'vr':
                # Verify and update roles - Admin only
                if current_user.role.lower() == "admin":
                    verify_and_update_user_roles()
                else:
                    print("\n  ERROR: Only Admin users can verify and update roles.\n")
            
            elif menu == 'dt':
                # Delete task - Admin only
                if current_user.role.lower() == "admin":
                    delete_task()
                else:
                    print("\n  ERROR: Only Admin users can delete tasks.\n")
            
            elif menu == 'vc':
                # View completed tasks - Admin only
                if current_user.role.lower() == "admin":
                    view_completed_tasks()
                else:
                    print("\n  ERROR: Only Admin users can view completed tasks.\n")
            
            elif menu == 'uc':
                # Update task completion status - Available to all users
                print_header("UPDATE TASK COMPLETION STATUS")
                update_task_complete()
            
            elif menu == 'rc':
                # Reset completed task to incomplete - Admin only
                if current_user.role.lower() == "admin":
                    print_header("RESET TASK TO INCOMPLETE")
                    reset_task_incomplete()
                else:
                    print("\n  ERROR: Only Admin users can reset completed tasks to incomplete.\n")
            
            elif menu == 'gr':
                # Generate reports - Admin only
                if current_user.role.lower() == "admin":
                    print_header("GENERATING REPORTS")
                    generate_reports()
                    print("  Reports generated successfully!")
                    print(f"    - {TASK_OVERVIEW_FILE}")
                    print(f"    - {USER_OVERVIEW_FILE}")
                    print()
                else:
                    print("\n  ERROR: Only Admin users can generate reports.\n")
            
            elif menu == 'ds':
                # Display statistics - Admin only
                if current_user.role.lower() == "admin":
                    print_header("TASK MANAGER STATISTICS")
                    display_statistics()
                else:
                    print("\n  ERROR: Only Admin users can view statistics.\n")
            
            elif menu == 'lo':
                # Logout
                print_header("LOGOUT")
                print(f"  Goodbye, {current_user.username}!")
                print()
                user_logged_in = False
            
            elif menu == 'e':
                # Exit
                print_header("THANK YOU")
                print("  Goodbye!!!")
                print()
                exit()
            
            else:
                print("\n  ERROR: You have entered an invalid input. Please try again.\n")


# ===== Program Execution =====
if __name__ == "__main__":
    main()