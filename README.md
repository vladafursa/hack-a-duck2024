This is my Hack-a-Duch 2024 project that I implemented solo and was awarded with employer challenge reward. 

The task was to create something that can assign people to projects more efficiently. My idea was to allow filtering employees by skills, experience, location, type of work, temperament, security clearance and availability. Apart from filtering HR can choose a project from project list and see the best options of assigning employees: actual team, ideal team and preferred team. Actual team is a team, where all employees are already available for start; ideal team is a team, where you do not specify the availability date; preferred team is a team when you can wait for specified period for other employees. Also, there is AI siggestion of team function. I implemented a function that forms a team with the next logic:
There are specified skills in a project, function searches all employees with matched skills and finds an employee with the greates number of these matched skills, adds it to the team list; if there are several employees with the same number, it chooses the one with the grater experience. Then found in this employee skills are removed from a search list. All this process is done till all required for a project skills are found. The list of employees is presented to the user; different types of teams are reached by giving the function already filtered list of employees.

Login credentials for HR are as follows:  
username: admin  
password: P@ssw0rd1!  

Login page:
<img width="1427" height="810" alt="Screenshot 2026-01-12 at 20 19 11" src="https://github.com/user-attachments/assets/19390fe7-9394-4a4b-8f78-c6ac83a0976b" />


Activities page:
<img width="1418" height="791" alt="Screenshot 2026-01-12 at 20 19 47" src="https://github.com/user-attachments/assets/d3bc4636-456d-4e97-af0a-115d7317f534" />


Filter page:
<img width="1431" height="809" alt="Screenshot 2026-01-12 at 20 44 39" src="https://github.com/user-attachments/assets/4805a4c7-3fb8-4959-8ff7-30ef12d7625c" />

Projects page:
<img width="1315" height="654" alt="Screenshot 2026-01-12 at 20 45 05" src="https://github.com/user-attachments/assets/04261765-482f-43a6-83df-06125070f020" />

Chosen project page:
<img width="1224" height="516" alt="Screenshot 2026-01-12 at 20 46 30" src="https://github.com/user-attachments/assets/e9df3d9c-d92c-4bc5-a9a3-ad14a35acaa3" />

