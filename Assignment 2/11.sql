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
