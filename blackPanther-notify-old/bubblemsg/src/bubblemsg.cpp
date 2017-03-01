/***************************************************************************
 *   Copyright (C) 2005 by Kovács Tamás                                    *
 *   kovacst@blackpanther.hu                                               *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

#define HEADER 25 // size of header
#define PIPE "/tmp/bubblepipe" // pipe file

int main (int argc, char *argv[])
{
 int pipe;
 long msglen, namestart, commstart, typelen, namelen, commlen;
 char *buff;

 if (argc < 3)
 {
  printf ("HIBA! Túl kevés paraméter!\n");
  printf ("\tHasználat: bubblemsg install | upgrade | uninstall <name> [<comment>]\n");
  printf ("\tHasználat: bubblemsg error <name> [<comment>]\n");
  printf ("\tHasználat: bubblemsg other <title> <message>\n");
  return 1;
 }

 if ((pipe = open (PIPE, O_TRUNC | O_WRONLY | O_NONBLOCK)) < 0)
 {
  printf ("HIBA! Nem hozhatá létre a kapcsolat!\n");
  return 1;
 }

 if ((strlen (argv[1])) > 99999)
 {
  printf ("HIBA! A <type> paraméter túl hosszú!\n");
  return 1;
 }
 if ((strlen (argv[2])) > 99999)
 {
  printf ("HIBA! Az elsõ paraméter túl hosszú!\n");
  return 1;
 }
 if (argc > 3) if ((strlen (argv[1])) > 99999)
 {
  printf ("HIBA! A második paraméter túl hosszú!\n");
  return 1;
 }
 typelen = strlen (argv[1]);
 namestart = HEADER + typelen;
 namelen = strlen (argv[2]);
 msglen = HEADER + strlen (argv[1]) + strlen (argv[2]);
 if (argc > 3)
 {
  msglen += strlen (argv[3]);
  commstart = namestart + namelen;
  commlen = strlen (argv[3]);
  buff = (char*) malloc (msglen);
  bzero (buff, msglen);
  sprintf (buff, "%5.0ld%5.0ld%5.0ld%5.0ld%5.0ld%s%s%s", typelen, namestart, namelen, commstart, commlen, argv[1], argv[2], argv[3]);
 }
 else
 {
  commstart = 0;
  commlen = 0;
  buff = (char*) malloc (msglen);
  bzero (buff, msglen);
  sprintf (buff, "%5.0ld%5.0ld%5.0ld%5.0ld%5.0ld%s%s", typelen, namestart, namelen, commstart, commlen, argv[1], argv[2]);
 }

 printf ("%s\n", buff);
 write (pipe, buff, msglen);

 return 0;
}
