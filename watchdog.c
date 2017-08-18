#include <assert.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/inotify.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#define EVENT_SIZE sizeof(struct inotify_event)
#define EVENT_BUF_LEN ( 1024 * (EVENT_SIZE + NAME_MAX + 1) )

void timestamp()
{
  time_t ltime; /* calendar time */
  ltime=time(NULL); /* get current cal time */
  printf("%s",asctime( localtime(&ltime) ) );
}

/* Takes a list of filenames as command-line arguments, and
   prints out a message when any one of these files is deleted. */
int main(int argc, char **argv)
{
  int i, j, fd, wd, len, index;
  char buffer[EVENT_BUF_LEN];
  int* wd_list;

  /* Allocate buffers */
  if ( (wd_list = malloc((argc - 1) * sizeof(int))) == NULL ) {
    goto error;
  }

  /* Set up inotify system */
  if ( (fd = inotify_init()) == -1 ) {
    goto error;
  }

  /* Create watch descriptors for each argument */
  for (i = 1; i < argc; i++) {
    if ( (wd = inotify_add_watch(fd, argv[i], IN_DELETE | IN_DELETE_SELF)) == -1 ) {
      goto error;
    }
    wd_list[i-1] = wd;
  }

  /* Listen for inotify events */
  while (1) {
    if ( (len = read(fd, buffer, EVENT_BUF_LEN)) < 0 ) {
      goto error;
    }
    i = 0;
    while (i < len) {
      struct inotify_event* event = (struct inotify_event*)&buffer[i];

      /* Linear search to find which file was modified */
      index = -1;
      for (j = 0; j < argc - 1; j++) {
        if (event->wd == wd_list[j]) {
          index = j;
          break;
        }
      }
      if (index < 0) {
        fprintf(stderr, "Event does not correspond to watched files.\n");
      } else {
        char* event_type = NULL;
        if (event->mask & IN_DELETE) {
          event_type = "IN_DELETE";
        } else if (event->mask & IN_DELETE_SELF) {
          event_type = "IN_DELETE_SELF";
        } else {
          event_type = "other";
        }
        timestamp();
        printf(" Delete event (%s) for %s\n", event_type, argv[index+1]);
      }

      i += EVENT_SIZE + event->len;
    }
  }

  return 0;

 error:
  perror(NULL);
  return -1;
}
