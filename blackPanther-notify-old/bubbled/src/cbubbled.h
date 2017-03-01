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

#ifndef CBUBBLED_H
#define CBUBBLED_H

#include <kconfig.h>
#include <ksystemtray.h>
#include <kpassivepopup.h>
#include <kaction.h>
#include <kactionclasses.h>

#include <qtimer.h>
#include <qframe.h>
#include <qstring.h>
#include <qpixmap.h>
#include <qlabel.h>
#include <qvbox.h>
#include <qfont.h>

#include "bubbled.h"
#include "cbase.h"

class CMsgView : public QFrame
{
 Q_OBJECT

 public:
  CMsgView (QWidget* parent = 0, const char* name = 0, WFlags f = 0);
  ~CMsgView();
  void fill (QString tit, QString msg, QPixmap ico);
  QVBox *getBox();

 private:
  QVBox *vbox;
  QHBox *hbox;
  QFont font;
  QLabel *icon, *title, *message;

  void arrange();

}; // class CMsgView

class CBubbled : public Bubbled
{
 Q_OBJECT

 public:
  CBubbled (QWidget* parent = 0, const char* name = 0, WFlags fl = 0);
  ~CBubbled();
  bool restore (int number, bool show = TRUE);

 protected:
  KConfig *conf;
  KSystemTray *tray;
  KPopupMenu *menu;
  KToggleAction *action[8];
  KPassivePopup *popup;

  QTimer *timer, *tFortune;

  CComm *pipe;
  CLog *log;
  CMsgView *popView;
  CFile *util;
  CSound *sound;
  
  int cPopupTimeout, cFortuneInterval;
  bool chkShow[11]; // install, upgrade, uninstall, error, update, club, usermsg, other, fortunes, fort-start/stop

  void init();
  void applySettings();
  void startFortunes();
  void stopFortunes();
  QString sayFortune();

 public slots:

 protected slots:
  void slotTimerDone();
  void slotSave();
  void slotApply();
  void slotCancel();
  void slotClose();
  void slotShowFortune();
  void slotPlaySound();

}; // class CBubbled

#endif
