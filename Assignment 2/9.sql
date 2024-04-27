SELECT e.fname, e.lname
FROM employee e
JOIN works_on w ON e.ssn = w.essn
JOIN project p ON w.pno = p.pnumber
WHERE e.dno = 7 
    AND e.salary > 50000 
    AND p.pname = 'DatabaseSystems';
