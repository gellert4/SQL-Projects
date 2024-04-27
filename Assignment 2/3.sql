SELECT p.pnumber, p.dnum, d.mgrssn, e.lname, e.address, e.bdate
FROM project p
JOIN department d ON p.dnum = d.dnumber
JOIN employee e ON d.mgrssn = e.ssn
WHERE p.plocation = 'Houston';
