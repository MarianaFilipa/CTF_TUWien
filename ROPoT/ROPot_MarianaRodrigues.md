ROPoT              
=====
 
Overview                   
--------
This program lets the user make the decisions that a robot sitting on a planet next to its crashed spaceship should take. After introducing its serial number, the user is introduced to the current situation of the robot, and asked to choose the next action of this robot. The execution of the program will end when the robot chooses to go into standby, or after a certain number of iterations.
 
 
Vulnerability                   
-------------
When analyzing the assembly code, we can see that there is a function "subroutine_init", that is responsible for reading the serial number of the "robot". By only study the assembly code, we can determine that it has a behavior similar to:
 
<pre><code>
void subroutine_init(){
   char serialnumber[8];
   printf("We wake up slightly outside of a crashed spaceship. Our systems ask for a serial number before resuming operation.\n[!] ENTER SN:");
   fflush(stdout);
   scanf("%s",serialnumber);
   printf("After parsing the serial number '%s', our systems continue to boot.", serialnumber);
   return;
}
</code></pre>
 
 
In the function above, we can observe that the function *scanf* is causing a vulnerability, as it doesn't establish bounds for the input given by the user and doesn't verify if it can be saved in the variable *serialnumber*.
 
Additionally, it is possible to determine the address of the functions in *libc*, such as system calls, as the program was statically linked. We can easily take control of the flow of the execution. This is facilitated by the lack of protection of the return address.
 
Exploitation                   
------------
As I stated previously, we (Cláudia Silva e12135542 and myself) started by testing how the program reacts when receiving a big input.
Our goal when overflowing the program was to reach the return address to the calling function, so we could control the flow of the program.
As we saw in the assembly code of the function previously mentioned, we had a guess that a segmentation fault would happen in that function when we wrote a string of size 24, as the program allocated 16 bytes for the array, and as between it and the saved eip it's the saved base pointer, which is written on 8 bytes of the stack. We tried it, and some other different sizes and used gdb to verify where the input would be written. Our initial guess ended up revealing itself true.
 
<pre><code>
           padding = b'A'*24
 
</code></pre>
 
We knew that the executable *mars* open the file flag and that the program is defined on a sandbox, which means we couldn't open a bash and execute the program mars. Therefore, we decided to use, as suggested, the system call *execve*.
In order to do so, we used the command ROPgadgets to find the pieces we needed.
As we wanted to use *execve*, we needed to prepare the registers that this function receives as input (%rdx,%rax,%rdi,%rsi) and use the gadgets to do the pop of these. We also needed the ROPgadget for the function syscall in order to call the function *execve*.
 
<pre><code>
           popRdi = p64(0x4018ea)
           popRsi = p64(0x40f6be)
           popRdx = p64(0x4017ef)
           ...
           popRax = p64(0x459e97)
           ...
           syscallGadget = p64(0x4012e3)
</code></pre>
 
 
When this last function is call, the registers needed to have the following values: %rax need to have the hexadecimal value equal to 59 as this is the value of the function we desired to use and the %rdi need to have a pointer for a address in memory that kept the string "./mars". Both %rsi and %rdx would be equal to *NULL*.
 
<pre><code>
           payload += popRax
           payload += p64(0x3b)
           payload += popRdi
           payload += p64(0x4e1bc0) #address for writable memory
           payload += popRsi
           payload += p64(0)
           payload += popRdx
           payload += p64(0)
</code></pre>
 
In order to add the string "./mars" to an address in memory, we need another ROPgadget, similar to "mov qword ptr [\_], \_ ; ret", and we need to do the pop of the registers that would be used in this gadget. Besides this, we also need to find a place in memory to write the string; we used the command "objdump -x" to do so and use the address “0x4e1bc0”.
 
<pre><code>
           writeGadget = p64(0x428838)
           ...
           payload += popRax
           payload += b'./mars\x00\x00'
           payload += popRdx
           payload += p64(0x4e1bc0) #address for writable memory
           payload += writeGadget
</code></pre>
 
With all of these parts we build the final payload, that is presented in the file "script_soluction.py" that it's submitted with this writeup.
  
 
Solution
--------
We can easily notice that few modifications are obvious, such as adding bounds to *scanf*. We could also have enabled canaries as an extra layer of protection, when compiling. Even though there was a mechanism in place that tried to ensure that control transfers were into a trusted approved code, we were still able to overwrite it.
We could also have used *ASLR: Address Space Layout Randomization"*, as a run-time protection mechanism. This would prevent the attacker from knowing which addresses are binary codes loaded into, making it harder to invoke different programs or functions defined in libc.