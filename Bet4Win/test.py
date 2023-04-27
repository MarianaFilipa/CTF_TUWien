import random
import string
import hashlib

#def get_random_string(void):
    # choose from all lowercase letter
    #letters = string.ascii_lowercase
    #while(true)
    #    result_str = ''.join(random.choice(letters) for i in range(28))
    #    m = hashlib.sha1()
    #    m.update(result_str)
    #    hashvalue = m.hexdigest()
    
    #    length = len(hashvalue)
    #    while(int i = length-1; i > length - 7; i--)

# GERAR STRING: import string;import random; letters = string.ascii_lowercase;result_str = ''.join(random.choice(letters) for i in range(28)); print(result_str) 
# GERAR HASH e PEGA ULTIMOS CHARS: 

#import string; import random; import hashlib; letters = string.ascii_lowercase; result_str = ''.join(random.choice(letters) for i in range(28)); s1 = hashlib.sha1(result_str.encode("utf-8")).hexdigest(); s2 = s1[-6:]; if(s2 == "00c791") print(s2) else print("F")

def main(void):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(28))
    print(result_str)


#print(result_str); print(s1); print(s2)

import string; import random; import hashlib; letters = string.ascii_lowercase; result_str = ''.join(random.choice(letters) for i in range(28)); s1 = hashlib.sha1(result_str.encode("utf-8")).hexdigest(); s2 = s1[-6:]; if (s2 == "00c791"):    print(s2); else:    print("F")



import string; import random; import hashlib; letters = string.ascii_lowercase; result_str = ''.join(random.choice(letters) for i in range(28)); s1 = hashlib.sha1(result_str.encode("utf-8")).hexdigest(); s2 = s1[-6:]; obj = "00c791";print("V") if s2 == obj else print("F")


import string; import random; import hashlib; letters = string.ascii_lowercase; flag = True
while flag: result_str = ''.join(random.choice(letters) for i in range(28)); s1 = hashlib.sha1(result_str.encode("utf-8")).hexdigest(); s2 = s1[-6:]; obj = "00c791"; flag = False if s2 == obj else flag = True



Cod:
import string; import random; import hashlib; letters = string.ascii_lowercase; flag = True
while flag: result_str = ''.join(random.choice(letters) for i in range(27)); s1 = hashlib.sha1(result_str.encode("utf-8")).hexdigest(); s2 = s1[-6:]; obj = "00c791"; flag = False if s2 == obj else True

Sol: yajltoodhsknfbnauslrcrjeydzd
hash: \xea\x0a\xa8\x3c\x38\x8c\xc2\xcb\xd5\xcc\x05\x39\x64\x41\xe2\xb5\x76 00c791

ou: tbbxnooccvomrsirwcfbayhjtwab
hash: 93 6d c3 18 08 ea 3e 9b 79 bc 03 13 45 1f 51 b1 02 \x00\xc7\x91

NOVA:
Salt: voivrqoz
Pass: fmdyeschqiekiwzdvxy
sol: fmdyeschqiekiwzdvxyvoivrqoz

\x66\x6d\x64\x79\x65\x73\x63\x68\x71\x69\x65\x6b\x69\x77\x7a\x64\x76\x78\x79\x76\x6f\x69\x76\x72\x71\x6f\x7a
\x4e\x86\x16\x1a\x15\x18\xa8\xcb\x00\xff\xc2\xb8\xd9\x5f\x61\xd7\x83           00 c7 91


$(python3 -c 'import sys; sys.stdout.buffer.write(b"\x66\x6d\x64\x79\x65\x73\x63\x68\x71\x69\x65\x6b\x69\x77\x7a\x64\x76\x78\x79\x00\x76\x6f\x69\x76\x72\x71\x6f\x7a\x4e\x86\x16\x1a\x15\x18\xa8\xcb\x00\xff\xc2\xb8\xd9\x5f\x61\xd7\x83")')