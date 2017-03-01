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

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

#include "cbase.h"

int logfile;
bool bShow[8];

////////// class CComm //////////

CComm::CComm()
{
 opened = false;
 empty = true;
 name = NULL;
 comm = NULL;
 typenum = 0;
 pipe = -1;
} // CComm constructor

CComm::~CComm()
{
} // CComm destructor

bool CComm::link()
{
 int mode = 0644;

 mode |= S_IFIFO;
 mknod (PIPE, mode, makedev (0, 0));
 if ((pipe = open (PIPE, O_TRUNC | O_RDONLY | O_NONBLOCK)) < 0)
 {
  printf ("HIBA! Nem hozható létre a kapcsolat!\n");
  return false;
 }
 opened = true;
 empty = true;

 return true;
} // link()

void CComm::listen()
{
 int datalen;
 char buff[32768], header[5], *type;
 int tlen, nstart, nlen, cstart, clen;
 
 if (opened)
 {
  bzero (buff, 32768);
  datalen = read (pipe, buff, 32767);
  if (datalen > 0)
  {
   empty = false;
   free (name);
   name = NULL;
   typenum = 0;
   if (comm != NULL)
   {
    free (comm);
    comm = NULL;
   }

   strncpy (header, buff, 5);
   tlen = atoi (header);
   strncpy (header, &buff[5], 5);
   nstart = atoi (header);
   strncpy (header, &buff[10], 5);
   nlen = atoi (header);
   strncpy (header, &buff[15], 5);
   cstart = atoi (header);
   strncpy (header, &buff[20], 5);
   clen = atoi (header);
   type = (char*) malloc (tlen + 1);
   name = (char*) malloc (nlen + 1);
   comm = (char*) malloc (clen + 1);
   bzero (type, tlen + 1);
   bzero (name, nlen + 1);
   bzero (comm, clen + 1);
   strncpy (type, &buff[25], tlen);
   type[tlen] = 0;
   strncpy (name, &buff[nstart], nlen);
   name[nlen] = 0;
   if (cstart > 0)
   {
    strncpy (comm, &buff[cstart], clen);
    comm[clen] = 0;
   }

   typenum = 0;
   if ((strcmp (type, "install") == 0) and bShow[INSTALL]) typenum = INSTALL;
   else if ((strcmp (type, "upgrade") == 0) and bShow[UPGRADE]) typenum = UPGRADE;
   else if ((strcmp (type, "uninstall") == 0) and bShow[UNINSTALL]) typenum = UNINSTALL;
   else if ((strcmp (type, "error") == 0) and bShow[ERROR]) typenum = ERROR;
   else if ((strcmp (type, "update") == 0) and bShow[UPDATE]) typenum = UPDATE;
   else if ((strcmp (type, "club") == 0) and bShow[CLUB]) typenum = CLUB;
   else if ((strcmp (type, "usermsg") == 0) and bShow[USERMSG]) typenum = USERMSG;
   else if ((strcmp (type, "other") == 0) and bShow[OTHER]) typenum = OTHER;

   if (clen == 0) comm = NULL;
   free (type);
   type = NULL;
  }
  if (typenum == 0) empty = true;
 }
 else empty = true;
} // listen()

void CComm::setConfig (bool *config)
{
 int i;

 for (i = 0; i < 8; i++)
 {
  bShow[i] = *config++;
 }
} // setConfig();

////////// class CSound //////////

CSound::CSound()
{
 sound1 = NULL;
} // CSound constructor

CSound::~CSound()
{
 if (sound1 != NULL) free (sound1);
} // CSound destructor

bool CSound::load (char *file)
{
 int wav;
 struct stat finfo;
 
 if ((wav = open (file, O_RDONLY)) < 0)
 {
  printf ("HIBA! A hangfájl nem nyitható meg.\n");
  return false;
 }

 if (!stat (file, &finfo))
 {
  sound1 = (char*) malloc (finfo.st_size);
  size1 = finfo.st_size;
  if ((read (wav, sound1, finfo.st_size)) == finfo.st_size)
  {
   close (wav);
   return true;
  }
  else
  {
   close (wav);
   return false;
  }
 }
 else return false;
} // load()

void CSound::play()
{
 int dsp;
 
 if ((dsp = open ("/dev/dsp", O_WRONLY | O_NONBLOCK)) < 0)
 {
  printf ("HIBA! A hangeszköz nem nyitható meg.\n");
  return;
 }
 printf ("Hang lejataszasa\n");
 write (dsp, sound1, size1);
 close (dsp);
} // play()

////////// class CLog //////////

CLog::CLog()
{
} // CLog constructor

CLog::~CLog()
{
} // CLog destructor

void CLog::openLog()
{
 int mode = 0644;

 if ((logfile = open ("/home/tomi/bubbled.log", O_CREAT | O_APPEND | O_WRONLY, mode)) < 0)
 {
  printf ("HIBA! A logfájl nem hozható létre!\n");
  logfile = -1;
 }
} // openLog()

void CLog::writeLog (char *err)
{
 if (logfile >= 0)
 {
  write (logfile, err, strlen (err));
  write (logfile, "\n", 1);
 }
} // writeLog()

void CLog::closeLog()
{
 if (logfile>= 0) close (logfile);
} // closeLog()

////////// class CFile //////////

CFile::CFile()
{
} // CFile constructor

CFile::~CFile()
{
} // CFile destructor

char *CFile::getContent (const char* fname)
{
 struct stat finfo;
 char *buff;

 if ((file = open (fname, O_RDONLY)) < 0)
 {
  printf ("HIBA! A fájl nem olvasható!\n");
  file = -1;
  return NULL;
 }

 if (!stat (fname, &finfo))
 {
  buff = (char*) malloc (finfo.st_size + 1);
  if ((read (file, buff, finfo.st_size)) == finfo.st_size)
  {
   close (file);
   buff[finfo.st_size] = '\0';
   return buff;
  }
  else
  {
   close (file);
   return NULL;
  }
 }
 else
 {
  close (file);
  return NULL;
 }
} // getContent()

void CFile::makeLockFile()
{
 int lock, mode = 0644;

 if ((lock = open (LOCKFILE, O_CREAT | O_TRUNC | O_WRONLY, mode)) < 0)
 {
  printf ("HIBA! A lockfájl nem hozható létre!\n");
 }
 else close (lock);
} // makeLockFile()

int CFile::deleteFile (char* fname)
{
 return unlink (fname);
} // deleteFile()
