SELECT fname, lname, pname
FROM employee
JOIN works_on ON ssn = essn
JOIN project ON pno = pnumber
WHERE pname IN ('Middleware', 'DatabaseSystems');

SELECT DISTINCT e.fname, e.lname
FROM employee e
JOIN works_on w ON e.ssn = w.essn
WHERE w.pno = (SELECT pnumber FROM project WHERE pname = 'DatabaseSystems')
AND w.hours > 40;

SELECT p.pnumber, p.dnum, d.mgrssn, e.lname, e.address, e.bdate
FROM project p
JOIN department d ON p.dnum = d.dnumber
JOIN employee e ON d.mgrssn = e.ssn
WHERE p.plocation = 'Houston';

SELECT e.fname AS employee_fname, e.lname AS employee_lname, 
       s.fname AS supervisor_fname, s.lname AS supervisor_lname
FROM employee e
LEFT JOIN employee s ON e.superssn = s.ssn;

SELECT *
FROM employee
WHERE sex = 'F' AND address LIKE '%Houston, TX%';

SELECT *
FROM employee
WHERE MONTH(bdate) = 6;

SELECT d.dname, AVG(e.salary) AS average_salary
FROM department d
JOIN employee e ON d.dnumber = e.dno
GROUP BY d.dname;

SELECT fname, lname
FROM employee
WHERE ssn NOT IN (SELECT DISTINCT essn FROM works_on);

SELECT e.fname, e.lname
FROM employee e
JOIN works_on w ON e.ssn = w.essn
JOIN project p ON w.pno = p.pnumber
WHERE e.dno = 7 
    AND e.salary > 50000 
    AND p.pname = 'DatabaseSystems';

SELECT e.fname, e.lname
FROM employee e
JOIN employee m ON e.superssn = m.ssn
WHERE e.address LIKE '%Houston, TX%' AND m.ssn = '333445555';

SELECT e.fname, e.lname
FROM employee e
WHERE e.dno = (
    SELECT d.dnumber
    FROM department d
    JOIN employee e ON d.dnumber = e.dno
    GROUP BY d.dnumber
    HAVING AVG(e.salary) = (
        SELECT MAX(avg_salary)
        FROM (
            SELECT AVG(salary) AS avg_salary
            FROM employee
            GROUP BY dno
        ) AS temp
    )
);

SELECT d.dnumber, d.dname, COUNT(e.ssn) AS num_employees
FROM department d
JOIN employee e ON d.dnumber = e.dno
GROUP BY d.dnumber, d.dname
HAVING AVG(e.salary) > 35000;

SELECT d.dependent_name, d.relationship
FROM dependent d
JOIN employee e ON d.essn = e.ssn
WHERE e.superssn = '333445555'
ORDER BY d.dependent_name;

SELECT p.pname, SUM(w.hours) AS total_hours, COUNT(DISTINCT w.essn) AS num_employees
FROM project p
JOIN works_on w ON p.pnumber = w.pno
GROUP BY p.pname;

SELECT d.dname, COUNT(DISTINCT p.pnumber) AS num_projects, COUNT(DISTINCT e.ssn) AS num_employees
FROM department d
LEFT JOIN project p ON d.dnumber = p.dnum
LEFT JOIN employee e ON d.dnumber = e.dno
GROUP BY d.dname;
