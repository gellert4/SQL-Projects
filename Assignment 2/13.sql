SELECT d.dependent_name, d.relationship
FROM dependent d
JOIN employee e ON d.essn = e.ssn
WHERE e.superssn = '333445555'
ORDER BY d.dependent_name;
