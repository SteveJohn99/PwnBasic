#include <string.h>
#include <stdio.h>

char * r(char *s)
{
  char *i; // [sp+Ch] [bp-Ch]@2

      printf("%s",s);
  if ( s )
  {
    for ( i = &s[strlen(s) - 1]; s < i; --i )
    {
      *s ^= *i;
      //*i ^= *s;
      //*s ^= *i;
      printf("%c",*i);
      ++s;
    }
  }
	return i;
}
int main()
{
	char tt[32];
	strncpy(tt,"573rc353r4pm0c07pmcr7535u7n0d",32);
	printf("%s\n", tt);
	r(tt);
	printf("%s\n", tt);
	return 0;
}
