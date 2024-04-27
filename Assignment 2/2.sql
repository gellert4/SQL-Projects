SELECT DISTINCT e.fname, e.lname
FROM employee e
JOIN works_on w ON e.ssn = w.essn
WHERE w.pno = (SELECT pnumber FROM project WHERE pname = 'DatabaseSystems')
AND w.hours > 40;
