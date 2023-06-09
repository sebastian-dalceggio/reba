USE ipc_database;
GO

IF OBJECT_ID('interanual', 'P') IS NOT NULL
    DROP PROCEDURE interanual;
GO

CREATE PROCEDURE interanual
	@Region nvarchar(50)
AS

	SELECT TOP 5
		i1.date,
		i1.category,
		i1.value,
		i1.value*100/i2.value - 100 AS interanual_value
	FROM 
		indice_aperturas i1
	LEFT JOIN
	(
		SELECT
			date,
			category,
			value
		FROM indice_aperturas
		WHERE region = @Region
	) i2 ON i1.date = DATEADD(year, 1, i2.date) AND i1.category = i2.category AND i2.value IS NOT NULL
	WHERE
    		i1.date = (SELECT MAX(date) FROM indice_aperturas) AND i1.region = @Region
	ORDER BY interanual_value DESC
GO