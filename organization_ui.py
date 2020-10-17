"""Assignment 2: User Interface

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains a code to create an interactable interface using the
classes specified in organization_hierarchy.py and the client code in
client_code.py.

Author: Anshul Agrawal
"""
from typing import Optional, List, Callable
from tkinter import *
from client_code import OrganizationSimulator


def format_superior(superior: Optional['Employee'] = None) -> str:
    """Return a string matching <superior>'s ID for the View Superior button.
    """
    if superior:
        return "View Superior (ID: {})".format(superior.eid)

    return "View Superior (N/A)"


def display_employee_list(employees: List['Employee'], label: str) -> None:
    """Opens a window that lists all the names and IDs of the employees in
    <employees>.
    """
    list_window = Toplevel(main_window)
    main_label = Label(list_window, text=label, anchor=W)
    main_label.grid(column=0, row=0, sticky=NSEW)

    for i in range(len(employees)):
        employee = employees[i]
        employee_label = "{} (ID: {})".format(employee.name, employee.eid)
        current_label = Label(list_window, text=employee_label, anchor=W)
        current_label.grid(column=0, row=i + 1, sticky=NSEW)


def update_subordinates() -> None:
    """Update the list of subordinates.
    """
    if simulation.displaying_direct:
        display_direct_btn.configure(state=DISABLED)
        display_all_btn.configure(state=NORMAL)
    else:
        display_direct_btn.configure(state=NORMAL)
        display_all_btn.configure(state=DISABLED)

    subordinates_list.delete(0, END)
    subordinates = simulation.current_subordinates

    for subordinate in subordinates:
        subordinate_string = "{} (ID: {})".format(subordinate.name,
                                                  subordinate.eid)
        subordinates_list.insert(END, subordinate_string)


def update_employee() -> None:
    """Updates the displayed employee to show current_employee's details.
    """
    (name, salary, rating, position, department) = \
        simulation.get_current_employee_details()

    superior_button_text = format_superior(simulation.get_current_superior())
    view_superior_btn.configure(text=superior_button_text)

    if superior_button_text == "View Superior (N/A)":
        view_superior_btn.configure(state=DISABLED)
    else:
        view_superior_btn.configure(state=NORMAL)

    if simulation.is_leader():
        switch_leader_employee_btn.configure(text="Become an employee")
        become_leader_btn.configure(state=NORMAL)
        department_employees_btn.configure(state=NORMAL)
    else:
        switch_leader_employee_btn.configure(text="Become a leader")
        become_leader_btn.configure(state=DISABLED)
        department_employees_btn.configure(state=DISABLED)

    employee_name_display.configure(text=name)
    employee_salary_display.configure(text=salary)
    employee_rating_display.configure(text=rating)
    employee_position_display.configure(text=position)
    employee_department_display.configure(text=department)

    # Update the average salary
    average_salary = simulation.get_average_salary()
    average_salary_display.configure(text="{:.2f}".format(average_salary))

    # Update the list of subordinates
    if simulation.displaying_direct:
        display_direct_subordinates_button()
    else:
        display_all_subordinates_button()


def create_single_prompt_window(instruction: str, button_label: str,
                                to_call: Callable[[str], None]) -> None:
    """Opens a window with instruction and button_label to prompt the user.
    Upon pressing the button with button_label, passes the entered data
    to to_call as a string.
    """
    new_window = Toplevel(main_window)

    def on_button_click() -> None:
        """Retrieve the entered text and calls to_call, closing this window.
        """
        entered_data = prompt_txt.get().strip()

        to_call(entered_data)
        new_window.destroy()

    # Instructions
    instructions_lbl = Label(new_window, text=instruction, anchor=W,
                             wraplength=300)
    instructions_lbl.grid(column=0, row=0, columnspan=2,
                          sticky=NSEW)

    # Prompt for the user
    prompt_txt = Entry(new_window)
    prompt_txt.grid(column=0, row=1, sticky=NSEW)

    # Add the button
    employee_window_add_btn = Button(new_window, text=button_label,
                                     command=on_button_click)
    employee_window_add_btn.grid(column=1, row=1, sticky=NSEW)


# === Button handlers ===
def view_head_button() -> None:
    """Updates the display to the head of the organization when clicked.
    """
    simulation.current_employee = simulation.get_organization_head()
    update_employee()


def view_superior_button() -> None:
    """Updates the display to the superior of the employee when clicked.
    """
    superior = simulation.get_current_superior()
    if superior:
        simulation.current_employee = superior
    update_employee()


def display_direct_subordinates_button() -> None:
    """Updates the display of the subordinates to list direct subordinates only.
    """
    simulation.display_direct_subordinates()
    update_subordinates()


def display_all_subordinates_button() -> None:
    """Updates the display of the subordinates to list all subordinates.
    """
    simulation.display_all_subordinates()
    update_subordinates()


def add_employee_button() -> None:
    """Open the 'add employee' window to prompt the user for employee details.
    """
    employee_window = Toplevel(main_window)

    def create_employee() -> None:
        """Creates a new employee, reading in data from employee_window.
        """
        name = employee_window_name_txt.get().strip()
        eid = int(employee_window_id_txt.get().strip())
        salary = float(employee_window_salary_txt.get().strip())
        rating = int(employee_window_rating_txt.get().strip())
        position = employee_window_position_txt.get().strip()
        superior = employee_window_superior_txt.get().strip()
        if not superior:
            superior = 0
        else:
            superior = int(superior)
        simulation.create_employee(name, eid, salary, rating, position,
                                   superior)

        update_employee()
        employee_window.destroy()

    # Instructions
    instructions = ("Enter the employee details below. \nIf Superior ID is " +
                    "empty, this employee will become the head of the " +
                    "organization.")
    employee_window_instructions = Label(employee_window, text=instructions,
                                         anchor=W, wraplength=300)
    employee_window_instructions.grid(column=0, row=0, columnspan=2,
                                      sticky=NSEW)

    # Label for their name
    employee_window_name_lbl = Label(employee_window, text="Name", anchor=W)
    employee_window_name_lbl.grid(column=0, row=1, sticky=NSEW)

    employee_window_name_txt = Entry(employee_window)
    employee_window_name_txt.grid(column=1, row=1, sticky=NSEW)

    # Label for their id number
    employee_window_id_lbl = Label(employee_window, text="ID", anchor=W)
    employee_window_id_lbl.grid(column=0, row=2, sticky=NSEW)

    employee_window_id_txt = Entry(employee_window)
    employee_window_id_txt.grid(column=1, row=2, sticky=NSEW)

    # Label for their salary
    employee_window_salary_lbl = Label(employee_window, text="Salary",
                                       anchor=W)
    employee_window_salary_lbl.grid(column=0, row=3, sticky=NSEW)

    employee_window_salary_txt = Entry(employee_window)
    employee_window_salary_txt.grid(column=1, row=3, sticky=NSEW)

    # Label for the rating
    employee_window_salary_lbl = Label(employee_window, text="Rating",
                                       anchor=W)
    employee_window_salary_lbl.grid(column=0, row=4, sticky=NSEW)

    employee_window_rating_txt = Entry(employee_window)
    employee_window_rating_txt.grid(column=1, row=4, sticky=NSEW)

    # Label for their position
    employee_window_position_lbl = Label(employee_window, text="Position",
                                         anchor=W)
    employee_window_position_lbl.grid(column=0, row=5, sticky=NSEW)

    employee_window_position_txt = Entry(employee_window)
    employee_window_position_txt.grid(column=1, row=5, sticky=NSEW)

    # Label for their superior id
    employee_window_superior_lbl = Label(employee_window, text="Superior (ID)",
                                         anchor=W)
    employee_window_superior_lbl.grid(column=0, row=6, sticky=NSEW)

    employee_window_superior_txt = Entry(employee_window)
    employee_window_superior_txt.grid(column=1, row=6, sticky=NSEW)

    # Add employee button
    employee_window_add_btn = Button(employee_window, text="Add Employee",
                                     command=create_employee)
    employee_window_add_btn.grid(column=0, row=7, columnspan=2,
                                 sticky=NSEW)


def view_selected_subordinate_button() -> None:
    """Display the selected subordinate.
    """
    if subordinates_list.curselection():
        index = subordinates_list.curselection()[0]
        selected_employee = simulation.current_subordinates[index]
        simulation.display_employee(selected_employee.eid)
        update_employee()


def higher_paid_button() -> None:
    """Display a list of the higher paid employees.
    """
    label = ("Displaying employees with a salary " +
             "higher than {}:").format(simulation.current_employee.salary)
    display_employee_list(simulation.get_higher_paid_employees(), label)


def common_superior_button(result: Optional[str] = None) -> None:
    """Prompt the user for another employee's ID and display their common
    superior.
    """
    instruction = ("Enter the ID for the employee you want to find a " +
                   "common superior with for the current displayed employee.")
    button_label = "Find Superior"
    if not result:
        create_single_prompt_window(instruction, button_label,
                                    common_superior_button)
    else:
        label = ("Displaying the closest common superior of the employees " +
                 "with IDs {} and {}").format(result,
                                              simulation.current_employee.eid)
        display_employee_list([simulation.get_common_superior(int(result))],
                              label)


def position_in_hierarchy_button() -> None:
    """Open a window that displays the current employee's full position in
    the hierarchy.
    """
    label = "The full position of {} (ID: {}) is:".format(
        simulation.current_employee.name, simulation.current_employee.eid)

    position_window = Toplevel(main_window)
    main_label = Label(position_window, text=label, anchor=W)
    main_label.grid(column=0, row=0, sticky=NSEW)

    position = simulation.get_position_in_hierarchy()
    position_label = Label(position_window, text=position, anchor=W)
    position_label.grid(column=0, row=1, sticky=NSEW)


def obtain_subordinates_button(result: Optional[str] = None) -> None:
    """Prompt the user for IDs (comma separated) and adds those employees as
    subordinates of the current employee.
    """
    if not result:
        instruction = ("Enter the IDs of the employees to take as " +
                       "subordinates. The IDs must be separated by commas.")
        button_label = "Obtain Subordinates"
        create_single_prompt_window(instruction, button_label,
                                    obtain_subordinates_button)
    else:
        ids = result.split(",")
        for i in range(len(ids)):
            ids[i] = int(ids[i].strip())
        simulation.obtain_subordinates(ids)
        update_employee()


def become_department_leader_button() -> None:
    """Move the the current employee up the hierarchy to become the leader of
    their department.
    """
    simulation.take_over_department()
    update_employee()


def change_employee_role(result: Optional[str] = None) -> None:
    """Change the employee into a leader (prompting for a department name) OR if
    the employee is already a leader, changes them into an employee.
    """
    if simulation.is_leader():
        simulation.become_employee()
        update_employee()
    else:
        if result:
            simulation.become_leader(result)
            update_employee()
        else:
            instruction = "Enter the name of the department to be created."
            button_label = "Create Department"
            create_single_prompt_window(instruction, button_label,
                                        change_employee_role)


def department_employees_button() -> None:
    """Display a list of the name and IDs of employees in the department.
    """
    department = simulation.get_current_employee_department()
    label = "Displaying the employees in the {} department.".format(department)
    employees = simulation.find_department_employees()
    display_employee_list(employees, label)


def change_department_name_button(result: Optional[str] = None) -> None:
    """Prompt the user for a new department name and changes the name of the
    leader's department. Unavailable if the current employee is not a leader.
    """
    if result:
        simulation.become_leader(result)
        update_employee()
    else:
        instruction = "Enter the new name of the department."
        button_label = "Change Name"
        create_single_prompt_window(instruction, button_label,
                                    change_department_name_button)


def view_employee_button(result: Optional[str] = None) -> None:
    """Prompt the user for an ID and display the employee with that ID.
    """
    if result:
        simulation.display_employee(int(result))
        update_employee()
    else:
        instruction = "Enter the ID of the employee to display."
        button_label = "Display"
        create_single_prompt_window(instruction, button_label,
                                    view_employee_button)


def fire_employee_button(result: Optional[str] = None) -> None:
    """Prompt the user for an ID and fire the employee with that ID.
    """
    if result:
        simulation.fire_employee(int(result))
        update_employee()
    else:
        instruction = "Enter the ID of the employee to fire."
        button_label = "Fire"
        create_single_prompt_window(instruction, button_label,
                                    fire_employee_button)


def find_employees_with_position_button(result: Optional[str] = None) -> None:
    """Prompt the user for a position and display a list of employees with
    that position.
    """
    if result:
        label = "Displaying employees with the position {}.".format(result)
        employees = simulation.find_employees_with_position(result)
        display_employee_list(employees, label)
    else:
        instruction = "Enter the position of the employees to find."
        button_label = "Find employees"
        create_single_prompt_window(instruction, button_label,
                                    find_employees_with_position_button)


def load_from_file_button(result: Optional[str] = None) -> None:
    """Prompt the user for a filename and load that file as the current
    organization.

    Displays the head of the organization afterwards.
    """
    if not result:
        instruction = ("Enter the name of the file with the organization " +
                       "data. This file must be located in the same " +
                       "folder as organization_ui.py.")
        button_label = "Load File"
        create_single_prompt_window(instruction, button_label,
                                    load_from_file_button)
    else:
        simulation.file_to_organization(result)
        update_employee()


def get_dst_string(dst: "DepartmentSalaryTree") -> str:
    """Return the string that represents the DepartmentSalaryTree <dst>.
    """
    label = "{}: ${:.2f}".format(dst.department_name, dst.salary)

    substrings = []
    for subdepartment in dst.subdepartments:
        substrings.append(get_dst_string(subdepartment))

    split_strings = [substring.split("\n") for substring in substrings]

    # Get the maximum number of lines from a dst's string
    max_lines = 0
    if split_strings:
        max_lines = max([len(s) for s in split_strings])

    # Create a list with max_lines empty lists in it
    new_string = [[] for _ in range(max_lines)]

    # Join each line of each dst's string
    for i in range(max_lines):
        for string in split_strings:
            sub_length = max([len(line) for line in string])

            if i < len(string):
                padding_needed = sub_length - len(string[i])
                new_string[i].append(string[i] + " " * padding_needed)
            else:
                # If there is no such line, just pad it with spaces
                new_string[i].append(" " * sub_length)

    # Put 3 spaces between each subtree
    new_string_joined = [(' ' * 3).join(s) for s in new_string]

    # Add in the value of the current Tree
    str_width = 0
    if new_string_joined:
        str_width = len(new_string_joined[0])

    left_padding = (str_width // 2) - (len(label) // 2)
    right_padding = (str_width - str_width // 2) - (len(label) // 2)

    new_string_joined.insert(0, "{}{}{}".format(" " * left_padding,
                                                label,
                                                " " * right_padding))

    # Return the new string
    return "\n".join(new_string_joined)


def fire_rated_employee_button() -> None:
    """Fire the lowest rated employee.
    """
    simulation.fire_lowest_rated_employee()
    update_employee()


def promote_rated_employee_button(result: Optional[str] = None) -> None:
    """Promote the highest rated employee.
    """
    if result:
        simulation.promote_employee(int(result))
        update_employee()
    else:
        instruction = "Enter the ID of the employee to promote."
        button_label = "Promote"
        create_single_prompt_window(instruction, button_label,
                                    promote_rated_employee_button)


def fire_under_rated_employee_button(result: Optional[str] = None) -> None:
    """Fire all employees under the given rating.
    """
    if result:
        simulation.fire_under_rating(int(result))
        update_employee()
    else:
        instruction = "Enter a rating. Employees with a rating under this " + \
                      "amount will be fired."
        button_label = "Fire"
        create_single_prompt_window(instruction, button_label,
                                    fire_under_rated_employee_button)


def display_department_salary_tree_button() -> None:
    """Display the department salary tree.
    """
    dst = simulation.get_department_salary_tree()

    result = get_dst_string(dst)

    # Open a window and have the GST string in a label
    dst_window = Toplevel(main_window)
    main_label = Label(dst_window, text=result, anchor=W,
                       font='TkFixedFont')
    main_label.grid(column=0, row=0, sticky=NSEW)


# === Initial set-up of the Organization Simulator ===
simulation = OrganizationSimulator()

# === Set up for the UI layout ===
# Set up the main window
main_window = Tk()
main_window.title("Organization Management System")

# Create the left column of buttons (current employee view)
view_superior_btn = Button(main_window, text="View Superior (N/A)",
                           command=view_superior_button, state=DISABLED, )
view_superior_btn.grid(column=0, row=0, columnspan=2, sticky=NSEW)

employee_header_label = Label(main_window, text="Employee", anchor=W)
employee_header_label.grid(column=0, row=1, columnspan=2,
                           sticky=NSEW)

# Employee Name
employee_name_label = Label(main_window, text="    Name", anchor=W)
employee_name_label.grid(column=0, row=2, sticky=NSEW)

employee_name_display = Label(main_window, text="", relief="groove",
                              anchor=W)
employee_name_display.grid(column=1, row=2, sticky=NSEW)

# Employee Salary
employee_salary_label = Label(main_window, text="    Salary", anchor=W)
employee_salary_label.grid(column=0, row=3, sticky=NSEW)

employee_salary_display = Label(main_window, text="", relief="groove",
                                anchor=W)
employee_salary_display.grid(column=1, row=3, sticky=NSEW)

# Employee Rating
employee_rating_label = Label(main_window, text="    Rating", anchor=W)
employee_rating_label.grid(column=0, row=4, sticky=NSEW)

employee_rating_display = Label(main_window, text="", relief="groove",
                                anchor=W)
employee_rating_display.grid(column=1, row=4, sticky=NSEW)

# Employee Position
employee_salary_label = Label(main_window, text="    Position",
                              anchor=W)
employee_salary_label.grid(column=0, row=5, sticky=NSEW)

employee_position_display = Label(main_window, text="", relief="groove",
                                  anchor=W)
employee_position_display.grid(column=1, row=5, sticky=NSEW)

# Employee Department
employee_department_label = Label(main_window, text="    Department", anchor=W)
employee_department_label.grid(column=0, row=6, sticky=NSEW)

employee_department_display = Label(main_window, text="", relief="groove",
                                    anchor=W)
employee_department_display.grid(column=1, row=6, sticky=NSEW)

# Subordinates
subordinates_label = Label(main_window, text="Subordinates", anchor=W)
subordinates_label.grid(column=0, row=7, columnspan=2, sticky=NSEW)

# Display direct subordinates button
display_direct_btn = Button(main_window,
                            text="Display Direct\nSubordinates",
                            command=display_direct_subordinates_button)
display_direct_btn.grid(column=0, row=8, sticky=NSEW)

# Display all subordinates button
display_all_btn = Button(main_window, text="Display All\nSubordinates",
                         command=display_all_subordinates_button)
display_all_btn.grid(column=1, row=8, sticky=NSEW)

# List of subordinates
subordinates_list = Listbox(main_window, selectmode=SINGLE)
subordinates_list.grid(column=0, row=9, columnspan=2, rowspan=9,
                       sticky=NSEW)

# View selected subordinate button
view_selected_btn = Button(main_window, text="View Selected Subordinate",
                           command=view_selected_subordinate_button)
view_selected_btn.grid(column=0, row=18, columnspan=2, sticky=NSEW)

# ===
# Draw a border for padding
separator_label = Label(main_window, text="  ")
separator_label.grid(column=2, row=0, rowspan=10, sticky=NSEW)

# Set up the second column (Employee Controls)
employee_controls_label = Label(main_window, text="Employee Controls",
                                anchor=W)
employee_controls_label.grid(column=3, row=0, sticky=NSEW)

# View higher paid employees button
higher_paid_btn = Button(main_window, text="Find higher paid employees",
                         command=higher_paid_button)
higher_paid_btn.grid(column=3, row=1, sticky=NSEW)

# Get common superior button
common_superior_btn = Button(main_window, text="Find common superior",
                             command=common_superior_button)
common_superior_btn.grid(column=3, row=2, sticky=NSEW)

# Get position in hierarchy button
position_hierarchy_btn = Button(main_window,
                                text="Find full position in hierarchy",
                                command=position_in_hierarchy_button)
position_hierarchy_btn.grid(column=3, row=3, sticky=NSEW)

# Obtain subordinates button
obtain_subordinates_btn = Button(main_window, text="Obtain subordinates",
                                 command=obtain_subordinates_button)
obtain_subordinates_btn.grid(column=3, row=4, sticky=NSEW)

# Become the department leader button
become_department_leader_btn = Button(main_window, text="Take over department",
                                      command=become_department_leader_button)
become_department_leader_btn.grid(column=3, row=5, sticky=NSEW)

# Leader controls
employee_controls_label = Label(main_window, text="Leader Controls",
                                anchor=W)
employee_controls_label.grid(column=3, row=7, sticky=NSEW)

# Become leader button  -- Switches to "Become an employee" if the current
# employee is a Leader
switch_leader_employee_btn = Button(main_window, text="Become a leader",
                                    command=change_employee_role)
switch_leader_employee_btn.grid(column=3, row=8, sticky=NSEW)

# Get department employees button
department_employees_btn = Button(main_window, text="Find department employees",
                                  command=department_employees_button)
department_employees_btn.grid(column=3, row=9, sticky=NSEW)

# Change department name button
become_leader_btn = Button(main_window, text="Change department name",
                           command=change_department_name_button)
become_leader_btn.grid(column=3, row=10, sticky=NSEW)

# Rating-related buttons
employee_controls_label = Label(main_window, text="Rating Controls",
                                anchor=W)
employee_controls_label.grid(column=3, row=7, sticky=NSEW)

# ===
# Draw a border for padding
separator_label = Label(main_window, text="  ")
separator_label.grid(column=4, row=0, rowspan=10, sticky=NSEW)

# Organization control buttons
employee_name_label = Label(main_window, text="Organization Controls",
                            anchor=W)
employee_name_label.grid(column=5, row=0, columnspan=2, sticky=NSEW)

# Average Salary
average_salary_label = Label(main_window, text="    Average Salary",
                             anchor=W)
average_salary_label.grid(column=5, row=1, sticky=NSEW)

average_salary_display = Label(main_window, text="$0", relief="groove",
                               anchor=W)
average_salary_display.grid(column=6, row=1, sticky=NSEW)

# View organization head button
view_head_btn = Button(main_window, text="View organization head",
                       command=view_head_button)
view_head_btn.grid(column=5, row=2, columnspan=2, sticky=NSEW)

# Add employee button
add_employee_btn = Button(main_window,
                          text="Add employee to organization",
                          command=add_employee_button)
add_employee_btn.grid(column=5, row=3, columnspan=2, sticky=NSEW)

# View employee button
view_employee_btn = Button(main_window, text="View employee",
                           command=view_employee_button)
view_employee_btn.grid(column=5, row=4, columnspan=2, sticky=NSEW)

# Fire employee button
fire_employee_btn = Button(main_window, text="Fire employee",
                           command=fire_employee_button)
fire_employee_btn.grid(column=5, row=5, columnspan=2, sticky=NSEW)

# Find employees with position button
find_position_btn = Button(main_window,
                           text="Find employees with position",
                           command=find_employees_with_position_button)
find_position_btn.grid(column=5, row=6, columnspan=2, sticky=NSEW)

# Fire lowest rated employee button
fire_rated_btn = Button(main_window, text="Fire lowest-rated employee",
                        command=fire_rated_employee_button)
fire_rated_btn.grid(column=5, row=7, columnspan=2, sticky=NSEW)

# Fire lowest rated employee button
fire_under_rated_btn = Button(main_window, text="Fire under-rated employees",
                              command=fire_under_rated_employee_button)
fire_under_rated_btn.grid(column=5, row=8, columnspan=2, sticky=NSEW)

# Change department name button
promote_rated_btn = Button(main_window, text="Promote employee",
                           command=promote_rated_employee_button)
promote_rated_btn.grid(column=5, row=9, columnspan=2, sticky=NSEW)

# DepartmentSalaryTree button
department_salary_tree_btn = \
    Button(main_window,
           text="Display Department Salary Tree",
           command=display_department_salary_tree_button)
department_salary_tree_btn.grid(column=5, row=10, columnspan=2,
                                sticky=NSEW)

# Load from file button
load_from_file_btn = Button(main_window,
                            text="Load organization from file",
                            command=load_from_file_button)
load_from_file_btn.grid(column=5, row=11, columnspan=2,
                        sticky=NSEW)


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-import-modules': ['client_code', 'tkinter',
    #                                'typing', 'python_ta'],
    #     'disable': ['E9997', 'R0914', 'W0401', 'C0103'],
    #     'max-args': 7
    # })

    main_window.mainloop()
