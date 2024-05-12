-- creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
DECLARE s_averge FLOAT;
SELECT AVG(score) INTO s_averge FROM corrections
WHERE corrections.user_id = user_id;
UPDATE users
SET average_score = s_averge
WHERE id = user_id;
END$$
