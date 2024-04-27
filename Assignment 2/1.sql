SELECT fname, lname, pname
FROM employee
JOIN works_on ON ssn = essn
JOIN project ON pno = pnumber
WHERE pname IN ('Middleware', 'DatabaseSystems');