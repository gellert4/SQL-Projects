SELECT p.pname, SUM(w.hours) AS total_hours, COUNT(DISTINCT w.essn) AS num_employees
FROM project p
JOIN works_on w ON p.pnumber = w.pno
GROUP BY p.pname;
