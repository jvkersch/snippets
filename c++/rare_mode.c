#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>

struct termios* rare_mode_start(int echo) {
    struct termios *p_old, new = {0};

    if ((p_old = malloc(sizeof(struct termios))) == NULL) {
        perror("malloc");
    }
    
    if (tcgetattr(0, p_old) < 0) {
        perror("tcsetattr");
    }

    memcpy(&new, p_old, sizeof(struct termios));

    if (echo == 0) {
        new.c_lflag &= ~ECHO;
    }
    new.c_lflag &= ~ICANON;
    new.c_cc[VMIN] = 1;
    new.c_cc[VTIME] = 0;

    if (tcsetattr(0, TCSANOW, &new) < 0)
        perror("tcsetattr");

    return p_old;
}

void rare_mode_stop(struct termios* p_old) 
{
    if (tcsetattr(0, TCSADRAIN, p_old) < 0)
        perror ("tcsetattr");
    free(p_old);
}

char rare_mode_read_one() 
{
    char buf = 0;
    if (read(0, &buf, 1) < 0)
        perror ("read()");
    return buf;
}
