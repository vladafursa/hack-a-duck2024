This is my Hack-a-Duch 2024 project that I implemented solo and was awarded with employer challenge reward. 

The task was to create something that can assign people to projects more efficiently. My idea was to allow filtering employees by skills, experience, location, type of work, temperament, security clearance and availability. Apart from filtering HR can choose a project from project list and see the best options of assigning employees: actual team, ideal team and preferred team. Actual team is a team, where all employees are already available for start; ideal team is a team, where you do not specify the availability date; preferred team is a team when you can wait for specified period for other employees. Also, there is AI siggestion of team function. I implemented a function that forms a team with the next logic:
There are specified skills in a project, function searches all employees with matched skills and finds an employee with the greates number of these matched skills, adds it to the team list; if there are several employees with the same number, it chooses the one with the grater experience. Then found in this employee skills are removed from a search list. All this process is done till all required for a project skills are found. The list of employees is presented to the user; different types of teams are reached by giving the function already filtered list of employees.

Login credentials for HR are as follows:  
username: admin  
password: P@ssw0rd1!  

*ask AI function does not work, because Open API key is not allowed to be pushed to Git*
