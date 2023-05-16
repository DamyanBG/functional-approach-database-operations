# Functional approach of common API problem - handling HTTP request followed by database operation

Here I implemented 4 ways of functional programming. You can find them in ./order/__init__.py . There is the main logic behind the idea. The database higher order functions are in ./common/database.py .

The first approach includes coupled functions.

The second approach uses decoupled functions and using lamda functions.

The third approach is implemented with the currying technique.

The last approachs is using higher order decoupled functions.