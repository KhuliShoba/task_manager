# Task Manager

A comprehensive task management application built in Python that allows users to manage tasks, track completion status, generate reports, and view statistics.

## Features

- **User Management**
  - User registration with role-based access control (Admin/Non-Admin)
  - User authentication with plain text passwords
  - Role verification and management

- **Task Management**
  - Create, view, update, and delete tasks
  - Assign tasks to users
  - Track task completion status
  - Set due dates with validation (no past dates allowed)
  - Edit task details (reassign user, change due date)
  - Only incomplete tasks can be edited

- **Task Operations**
  - View all tasks in the system
  - View tasks assigned to current user
  - Mark tasks as complete/incomplete
  - Delete tasks (with automatic backup)
  - View completed tasks (Admin only)
  - Reset completed tasks to incomplete (Admin only)

- **Reporting & Analytics**
  - Generate comprehensive task overview reports
  - Generate user overview reports with detailed statistics
  - Display statistics in user-friendly format
  - Auto-generate reports if they don't exist

- **Task Overview Report (task_overview.txt)**
  - Total number of tasks tracked
  - Total completed tasks
  - Total incomplete tasks
  - Incomplete and overdue tasks
  - Percentage of incomplete tasks
  - Percentage of overdue tasks

- **User Overview Report (user_overview.txt)**
  - Total registered users
  - Total tracked tasks
  - Per-user task statistics:
    - Total tasks assigned
    - Percentage of total tasks
    - Completion percentage
    - Incomplete percentage
    - Overdue percentage

- **Data Integrity**
  - Automatic file backup before destructive operations
  - File path constants for easy configuration
  - Error handling and logging system
  - Comprehensive audit trail (task_manager.log)

- **Advanced Features**
  - Recursive task selection with validation
  - Interactive task editing with multi-field updates
  - Role-based menu system (different options for Admin vs Non-Admin)
  - Helper functions for modular code (read_all_tasks, write_all_tasks)

## File Structure

```
task_manager/
├── task_manager.py          # Main application
├── user.txt                 # User database (username, password, role)
├── task.txt                 # Task database (task_id, username, title, description, due_date, assigned_date, complete)
├── task_overview.txt        # Generated task statistics report
├── user_overview.txt        # Generated user statistics report
├── task_manager.log         # Application audit log
└── README.md               # This file
```

## User Roles

### Admin
- Register new users
- View all users
- View all tasks
- Delete tasks
- View completed tasks
- Reset completed tasks to incomplete
- Verify and update user roles
- Generate reports
- Display statistics

### Non-Admin
- Add tasks
- View all tasks
- View own tasks
- Update task completion status
- Generate reports (view only)
- Display statistics (view only)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/KhuliShoba/task_manager.git
cd task_manager
```

2. Ensure Python 3 is installed:
```bash
python3 --version
```

## Usage

1. Run the application:
```bash
python3 task_manager.py
```

2. Login with your credentials:
   - Username: (enter registered username)
   - Password: (enter password)

3. Select from the menu options based on your role

## Sample Users

The application comes with the following sample users (found in user.txt):
- **lethabo** / **1234** (Admin)
- **lethu** / **890123** (Admin)
- **Max2** / **123456** (Admin)
- **Khuli** / **12345** (Non-Admin)
- **Thembi** / **456789** (Non-Admin)
- **motho** / **123456** (Non-Admin)

## Data Format

### user.txt Format
```
username, password, role
```
Example:
```
lethabo, 1234, Admin
Khuli, 12345, Non-Admin
```

### task.txt Format
```
task_id, username, title, description, due_date, assigned_date, complete
```
Example:
```
1, lethabo, Complete project, Finish the Python project, 2026-02-28, 2026-02-17, No
```

## Features in Detail

### Task Selection with Recursion
The `get_valid_task_number()` recursive function provides robust task selection:
- Validates task ID exists
- Ensures input is an integer
- Recursively re-prompts on invalid input
- Base case: Enter -1 to return to main menu

### Report Generation
- `generate_reports()` creates comprehensive statistics
- `display_statistics()` shows reports in formatted output
- Auto-generates reports if files don't exist

### Error Handling
- File I/O error handling with logging
- Input validation with descriptive error messages
- Backup creation before destructive operations

## Technical Details

- **Language:** Python 3
- **File I/O:** CSV-like format with comma-separated values
- **Logging:** Python logging module writing to task_manager.log
- **Date Validation:** Prevents past due date assignments
- **User Validation:** Checks user existence before task assignment
- **Data Persistence:** All data stored in text files

## Future Enhancements

- Password hashing support
- Database integration (SQLite/PostgreSQL)
- Web-based interface
- Email notifications
- Task priority levels
- Task categories/tags
- Recurring tasks

## Author

Khuli Shoba

## License

This project is part of HyperionDev Data Science Curriculum - Capstone Project

## Support

For issues or questions, please create an issue in the GitHub repository.
