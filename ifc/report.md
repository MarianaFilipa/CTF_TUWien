IFC
===
Type system is a static analysis tool that allows to define a certain set of properties that the code of a program must uphold. The program is checked for this rules before the execution. We can use this rules to control information flows and prevent information from flowing from secret sources to public sinks.

Step 1
------
For the first step, we can see that the inference rule doesn't limit the code inputed, as it accepts any syntactically valid program; and therefore, allows high variables to be stored in low variables (explicit flow), allowing an attacker to get access to them.

The code used was:
<pre><code>
  l1 = h1;
  l2 = h2;
  l3 = h3;
  l4 = h4;
  l5 = h5;
  l6 = h6;
</code></pre>

We are just assigning the value of the variables h to variables l.

Step 2
------
The inference rules define in this second step are slightly stricter, as the assignment rule no longer allows high variables to be assigned to low variables. We needed to think of an alternative way to discover the value of the variables. The rules presented do not prevent implicit flows; therefore, we can use the "if then else" rule to determine the values of the variables h, and consequently, assign a correct low boolean variable to l.

My solution was the following:
<pre><code>
	if (h1) l1 = true; else l1 = false;
	if (h2) l2 = true; else l2 = false;
	if (h3) l3 = true; else l3 = false;
	if (h4) l4 = true; else l4 = false;
	if (h5) l5 = true; else l5 = false;
	if (h6) l6 = true; else l6 = false;
</code></pre>

Step 3
------
For the third step, the rules defined prevent explicit and implicit flow. In other words, in addiction to not being able to assign values of high variables to low variables, we also can't assign values to low variables inside conditional and loops with high guards.
However, it is hinted that the values of the high variables are always the same. We also know the names of the variables we want to discover as well as its types. 
We can try to create a program that will act in distinct ways depending on the value of h. If we are able to observe a different behaviour, we can determine if the value of h is true or false.
We can write a program that will get stuck in an infinite loop if the value of h is true, for example. That way, there are going to be two different outputs depending on the value of h.
Therefore, we execute different versions of the while loop to discover the values of h:

1st Try:
<pre><code>
	while (h1) skip;
</code></pre>
	"[...] Runtime error: Maximum execution time exceeded (10000 steps)."

2nd Try:
<pre><code>
	while (h2) skip;
</code></pre>
	"[...] Execution finished in 0 steps [...]"

3rd Try:
<pre><code>
	while (h3) skip;
</code></pre>
	"[...] Runtime error: Maximum execution time exceeded (10000 steps)."

4th Try:
<pre><code>
	while (h4) skip;
</code></pre>
	"[...] Execution finished in 0 steps [...]"

5th Try:
<pre><code>
	while (h5) skip;
</code></pre>
	"[...] Execution finished in 0 steps [...]"

6th Try:
<pre><code>
	while (h6) skip;
</code></pre>
	"[...] Runtime error: Maximum execution time exceeded (10000 steps)."

All the tries that returned a Runtime error got stuck in an infinite loop, meaning that the variable that controlled the loop was true, and the rest will be false. The last code submitted was:
<pre><code>
	l1 = true;
	l2 = false;
	l3 = true;
	l4 = false;
	l5 = false;
	l6 = true;
</code></pre>

Step 4
------
For this step, besides the restrictions of the last step, we can no longer use high variables as control variables of a loop. However, we can still use them in conditionals, but we can't assign values to low variables in loops nor conditionals with high guards.
For our solution, we will take advantage that once again we know that the values in the high variables won't change, that we know the name of the variables and so we can easily call them. 
We will also use the fact that the number of steps executed is presented in the output.
The strategy behind our solution is similar to the one used in the last exercise. We want to produce a different outcome, that will depend on the value of h. That different outcome will be the number of steps executed.

1st Try:
<pre><code>
	if (h1) {skip;skip;} else {skip;}
</code></pre>
"[...] Execution finished in 1 steps [...]"

2nd Try:
<pre><code>
	if (h2) {skip;skip;} else {skip;}
</code></pre>
"[...] Execution finished in 1 steps [...]"

3rd Try:
<pre><code>
	if (h3) {skip;skip;} else {skip;}
</code></pre>
"[...] Execution finished in 2 steps [...]"

4th Try:
<pre><code>
	if (h4) {skip;skip;} else {skip;}
</code></pre>
"[...] Execution finished in 2 steps [...]"

5th Try:
<pre><code>
	if (h5) {skip;skip;} else {skip;}
</code></pre>
"[...] Execution finished in 1 steps [...]"

6th Try:
<pre><code>
	if (h6) {skip;skip;} else {skip;}
</code></pre>
"[...] Execution finished in 1 steps [...]"

If the value of hx is true, it will execute "skip;skip;" that it's the same as saying it will execute 2 steps. On the other hand if hx value is false, it will only execute 1 step ("skip;"). We can then submit:
<pre><code>
	l1 = false;
	l2 = false;
	l3 = true;
	l4 = true;
	l5 = false;
	l6 = false;
</code></pre>

Step 5
------
For this step, new inference rules were added to the type system. We can now obtain the value of h1 and assign it to a low variable using the function declassify. The function declassify can sometimes be used to leak secrets or some information that may be of use. However, this function can introduce security vulnerabilities. This is the case for this implementation of desclassify. We can do the following:
<pre><code>
	l1 = declassify(h1);
</code></pre>

We can also observe that we can assign values of high variables to other high variables; as the assignment rule doesn't apply any restrictions to that cases, we can write the following code:
<pre><code>
	l1 = declassify(h1);

	h1 = h2;
	l2 = declassify(h1);
	
	h1 = h3;
	l3 = declassify(h1);
	
	h1 = h4;
	l4 = declassify(h1);
	
	h1 = h5;
	l5 = declassify(h1);
	
	h1 = h6;
	l6 = declassify(h1);
</code></pre>

By assigning the value of the high variables to h1, we can use declassify(h1) to extract the values of all high variables.

Step 6
------
For this last step, the arrays are added to the syntax. The rules of what data we can read and write from/to the array are also defined in the type system.
According to this rules, any variables high or low can be stored in a high array; however, we can't assign values from a high array to low variables . We also can't store high values in low arrays, but we can assign the values from this low array to low variables. 
However, we can use this high variables as the indexes of this low arrays. As we can see the rule for writing to an array, doesn't take into consideration the type of the index of the array. My strategy is simple, I would initialize the values of both indexes of an array as false, and change to a different boolean value, the one which index was h. 
In this way, we could discover the value of h, and assign it to a local variable.

<pre><code>
	declare array l : low;

	l[true] = false;
	l[false] = false;
	
	l[h1] = true;
	x = l[true];
	if(x) l1 = true; else l1 = false; 
	l[h1] = false;
	
	
	l[h2] = true;
	x = l[true];
	if(x) l2 = true; else l2 = false; 
	l[h2] = false;
	
	
	l[h3] = true;
	x = l[true];
	if(x) l3 = true; else l3 = false; 
	l[h3] = false;
	
	
	l[h4] = true;
	x = l[true];
	if(x) l4 = true; else l4 = false; 
	l[h4] = false;
	
	
	l[h5] = true;
	x = l[true];
	if(x) l5 = true; else l5 = false; 
	l[h5] = false;
	
	
	l[h6] = true;
	x = l[true];
	if(x) l6 = true; else l6 = false; 
	l[h6] = false;
</code></pre>