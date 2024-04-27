SELECT e.fname, e.lname
FROM employee e
JOIN employee m ON e.superssn = m.ssn
WHERE e.address LIKE '%Houston, TX%' AND m.ssn = '333445555';
