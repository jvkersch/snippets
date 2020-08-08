/* compile with
emcc echo.c -o echo.js -s WASM=1 -s EXPORTED_FUNCTIONS='["_do_one"]' -s EXTRA_EXPORTED_RUNTIME_METHODS='["cwrap"]'
 */

#include <stdio.h>
#include <stdlib.h>

int do_one();

int main() 
{
    /* Read from stdin, echo to stdout/stderr. */
    while (1) {
        if (do_one() == 0) {
            break;
        }
        
    }

    return 0;
}


/* int do_one() */
/* { */
/*     fprintf(stderr, "starting\n"); */

    
/*     int ch = getchar(); */
/*     if (ch == EOF) { */
/*         return 0; */
/*     } */
/*     fprintf(stderr, "got a char: %d\n", ch); */
    
/*     putchar(ch); */
/*     fflush(stdout); */
    
/*     fprintf(stderr, "done posting char\n"); */
    
/*     return 1; */
/* } */

int do_one()
{
    char *buffer = NULL;
    size_t bufsize = 0;
    
    getline(&buffer, &bufsize, stdin);

    fprintf(stdout, "stdout: %s", buffer);
    fprintf(stderr, "stderr: %s", buffer);

    fflush(stdout);
    
    free(buffer);

    return 1;
}
