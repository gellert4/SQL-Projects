SELECT d.dnumber, d.dname, COUNT(e.ssn) AS num_employees
FROM department d
JOIN employee e ON d.dnumber = e.dno
GROUP BY d.dnumber, d.dname
HAVING AVG(e.salary) > 35000;
