--  creates a function SafeDiv that divides (and returns).
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
DECLARE result FLOAT;
IF b = 0
THEN
SET result = 0;
ElSE
SET result = a / b;
END IF;
RETURN result;
END$$
