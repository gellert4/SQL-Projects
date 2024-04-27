SELECT fname, lname
FROM employee
WHERE ssn NOT IN (SELECT DISTINCT essn FROM works_on);
