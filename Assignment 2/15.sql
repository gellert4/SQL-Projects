SELECT d.dname, COUNT(DISTINCT p.pnumber) AS num_projects, COUNT(DISTINCT e.ssn) AS num_employees
FROM department d
LEFT JOIN project p ON d.dnumber = p.dnum
LEFT JOIN employee e ON d.dnumber = e.dno
GROUP BY d.dname;
