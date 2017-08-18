#ifndef RARE_MODE_H
#define RARE_MODE_H

#ifdef __cplusplus
extern "C" {
#endif    

struct termios* rare_mode_start(int);
void rare_mode_stop(struct termios*);
char rare_mode_read_one();
    

#ifdef __cplusplus
}
#endif
    
#endif /* RARE_MODE_H */
