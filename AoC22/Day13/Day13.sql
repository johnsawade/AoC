-- AoC Day 13 - JohnS
CREATE OR ALTER FUNCTION comp_string (@array NVARCHAR(MAX))
RETURNS TABLE
AS RETURN (
    WITH PARSER AS (
        
		-- Generate series of numbers from 1 to the length of the input array        
		SELECT LVL = SUM(IIF(CHR = N'[', 1, IIF(CHR = N']', -1, 0))) OVER(ORDER BY [value])
            ,CHR
        FROM GENERATE_SERIES(1, CAST(LEN(@array) AS INT)) series

        -- Split the input array into individual characters
        CROSS APPLY (VALUES(SUBSTRING(REPLACE(@array, '10', 'A'), series.[value], 1))) X(CHR)
    )

    -- Produce the output table
    SELECT [value] = ISNULL(STRING_AGG(IIF(chr = ',', CHAR(33 + lvl), IIF(CHR in ('[',']'), '', CHR)), ''), '')
    FROM PARSER
    WHERE CHR NOT IN ('[',']')
);
GO

-- Declare variable to store input file
DECLARE @contents VARCHAR(MAX) = (SELECT BULKCOLUMN FROM OPENROWSET(BULK 'c:/code/AoC22/day13/input.txt', SINGLE_CLOB) D);

-- Declare variables to store input as a JSON array
DECLARE @c1 VARCHAR(MAX) = '[[' + REPLACE(REPLACE(TRIM(CHAR(10) FROM @contents), CHAR(10) + CHAR(10), '],['), CHAR(10), ',') + ']]';
DECLARE @c2 VARCHAR(MAX) = '[' + REPLACE(REPLACE(TRIM(CHAR(10) FROM @contents), CHAR(10) + CHAR(10), ','), CHAR(10), ',') + ',[[2]],[[6]]]';

-- Compute the sum of Part 1
SELECT [Part 1] = SUM(j.[key] + 1)
FROM OPENJSON(@c1) j
CROSS APPLY comp_string(json_query(j.[value], '$[0]')) [left]
CROSS APPLY comp_string(json_query(j.[value], '$[1]')) [right]
WHERE [left].[value] <= [right].[value];

-- Compute the Part 2 using exponential function
SELECT [Part 2] = EXP(SUM(LOG(j)))
FROM (
    SELECT j = ROW_NUMBER() OVER(ORDER BY y.[value]), j.[value]
    FROM OPENJSON(@c2) j
    CROSS APPLY comp_string([value]) y
) x
WHERE [value] in ('[[2]]','[[6]]');