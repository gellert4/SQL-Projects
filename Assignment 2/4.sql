SELECT e.fname AS employee_fname, e.lname AS employee_lname, 
       s.fname AS supervisor_fname, s.lname AS supervisor_lname
FROM employee e
LEFT JOIN employee s ON e.superssn = s.ssn;
