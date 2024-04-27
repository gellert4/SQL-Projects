SELECT d.dname, AVG(e.salary) AS average_salary
FROM department d
JOIN employee e ON d.dnumber = e.dno
GROUP BY d.dname;
