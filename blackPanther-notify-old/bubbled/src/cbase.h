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

#ifndef CBASE_H
#define CBASE_H

#define PIPE "/tmp/bubblepipe"
#define LOCKFILE "/tmp/bubbled.lock"
#define FORTUNESFILE "/tmp/bubbled.fortune"

#define TOGGLE 1
#define QUIT 2

#define INSTALL 1
#define UPGRADE 2
#define UNINSTALL 3
#define ERROR 4
#define UPDATE 5
#define CLUB 6
#define USERMSG 7
#define OTHER 8
#define FORTUNES 9
#define FORTSTART 10
#define FORTSPEC 11

class CComm
{
 public:
  bool empty;
  char *name, *comm;
  int typenum;

  CComm();
  ~CComm();

  bool link();
  void listen();
  void setConfig (bool *config);

 private:
  int pipe;
  bool opened;

}; // class CComm

class CSound
{
 public:
  CSound();
  ~CSound();

  bool load (char *file);
  void play();
 
 private:
  char *sound1;
  int size1;

}; // class CSound

class CLog
{
 public:
  CLog();
  ~CLog();

  void openLog();
  void writeLog (char *err);
  void closeLog();
 
 private:

}; // class CLog

class CFile
{
 public:
  CFile();
  ~CFile();

  char *getContent (const char* fname);
  void makeLockFile();
  int deleteFile (char* fname);

 private:
  int file;

}; // class CFile

#endif
