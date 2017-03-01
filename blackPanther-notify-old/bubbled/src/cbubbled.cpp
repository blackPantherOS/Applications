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

#include <kdialog.h>
#include <kpassivepopup.h>
#include <kpopupmenu.h>
#include <kiconloader.h>
#include <kmessagebox.h>

#include <qspinbox.h>
#include <qcheckbox.h>

#include "cbubbled.h"
#include "cbase.h"

////////// class CMsgView //////////

CMsgView::CMsgView (QWidget* parent, const char* name, WFlags f)
{
 vbox = new QVBox (parent, "vbox");
 vbox->setSpacing (KDialog::spacingHint());
 hbox = new QHBox (vbox, "hbox");
 hbox->setMargin (0);
 hbox->setSpacing (KDialog::spacingHint());
 icon = new QLabel (hbox, "labIcon");
 icon->setAlignment (AlignLeft);
 icon->setMaximumWidth (128);
 icon->setMaximumHeight (128);
 title = new QLabel (hbox, "labTitle");
 title->setTextFormat (Qt::RichText);
 font = title->font();
 font.setBold (true);
 title->setFont (font);
 title->setAlignment (Qt::AlignHCenter);
 title->setMinimumWidth (200);
 title->setMaximumWidth (350);
 hbox->setStretchFactor (title, 10); // enforce centering
 message = new QLabel (vbox, "labMessage");
 message->setAlignment (AlignLeft);
 message->setTextFormat (Qt::RichText);
 message->setMinimumWidth (200);
 message->setMaximumWidth (350);
 setFrameStyle (QFrame::PopupPanel | QFrame::Plain);
 setLineWidth (2);
 resize (sizeHint());
} // CMsgView constructor

CMsgView::~CMsgView()
{
} // CMsgView destructor


void CMsgView::fill (QString tit, QString msg, QPixmap ico)
{
 title->setText (tit);
 message->setText (msg);
 icon->setPixmap (ico);
 arrange();
} // fill()

QVBox* CMsgView::getBox()
{
 if (vbox != NULL) return vbox;
 else return 0;
} // getBox()

void CMsgView::arrange()
{
 title->adjustSize();
 message->adjustSize();
 icon->adjustSize();
 hbox->adjustSize();
 vbox->adjustSize();
 updateGeometry();
 resize (sizeHint());
} // arrange()

////////// class CBubbled //////////

CBubbled::CBubbled (QWidget* parent, const char* name, WFlags fl) : Bubbled (parent, name, fl)
{
 init();
} // CBubbled constructor

CBubbled::~CBubbled()
{
 util->deleteFile (LOCKFILE);
 util->deleteFile (FORTUNESFILE);
 util->deleteFile (PIPE);
 if (log) delete log;
 if (util) delete util;
 if (pipe) delete pipe;
 //if (sound) delete sound;
} // CBubbled destructor

bool CBubbled::restore (int number, bool show)
{
 if (show) this->show();

 return false;
} // restore()

void CBubbled::init()
{
 QString strRet;

 conf = NULL;
 tray = NULL;
 popup = NULL;
 popView = NULL;
 pipe = NULL;
 log = NULL;
 util = NULL;
 timer = NULL;
 tFortune = NULL;
 conf = new KConfig ("bubbledrc");
 tray = new KSystemTray (this);
 tray->setPixmap (tray->loadIcon ("ktip"));
 tray->show();
 log = new CLog();
 util = new CFile();
 util->makeLockFile();
 //// Sound part ////
 //sound = new CSound();
 //sound->load ((char*) "/home/tomi/Prog/kdevelop/bubbled/src/sounds/msgsent.wav");

 log->openLog();
 if (conf->hasGroup ("Main"))
  conf->setGroup (QString ("Main"));
 else
 {
  conf->setGroup (QString ("Main"));
  log->writeLog ((char*) "<Main> csoport nem található! Lérehozva..");
 }
 strRet = conf->readEntry ("PopupTimeout");
 if (strRet == QString::null)
 {
  conf->writeEntry ("PopupTimeout", 5000);
  cPopupTimeout = 5000;
  log->writeLog ((char*) "<Main/PopupTimeout> bejegyzés nem található! Lérehozva..");
 }
 else
 {
  cPopupTimeout = strRet.toInt();
 }
 chkShow[INSTALL] = conf->readBoolEntry ("ShowInstall", TRUE);
 if (!conf->hasKey ("ShowInstall"))
 {
  conf->writeEntry ("ShowInstall", TRUE);
  log->writeLog ((char*) "<Main/ShowInstall> bejegyzés nem található! Lérehozva..");
 }
 chkShow[UPGRADE] = conf->readBoolEntry ("ShowUpgrade", TRUE);
 if (!conf->hasKey ("ShowUpgrade"))
 {
  conf->writeEntry ("ShowUpgrade", TRUE);
  log->writeLog ((char*) "<Main/ShowUpgrade> bejegyzés nem található! Lérehozva..");
 }
 chkShow[UNINSTALL] = conf->readBoolEntry ("ShowUninstall", TRUE);
 if (!conf->hasKey ("ShowUninstall"))
 {
  conf->writeEntry ("ShowUninstall", TRUE);
  log->writeLog ((char*) "<Main/ShowUninstall> bejegyzés nem található! Lérehozva..");
 }
 chkShow[ERROR] = conf->readBoolEntry ("ShowError", TRUE);
 if (!conf->hasKey ("ShowError"))
 {
  conf->writeEntry ("ShowError", TRUE);
  log->writeLog ((char*) "<Main/ShowError> bejegyzés nem található! Lérehozva..");
 }
 chkShow[UPDATE] = conf->readBoolEntry ("ShowUpdate", TRUE);
 if (!conf->hasKey ("ShowUpdate"))
 {
  conf->writeEntry ("ShowUpdate", TRUE);
  log->writeLog ((char*) "<Main/ShowUpdate> bejegyzés nem található! Lérehozva..");
 }
 chkShow[CLUB] = conf->readBoolEntry ("ShowClub", TRUE);
 if (!conf->hasKey ("ShowClub"))
 {
  conf->writeEntry ("ShowClub", TRUE);
  log->writeLog ((char*) "<Main/ShowClub> bejegyzés nem található! Lérehozva..");
 }
 chkShow[USERMSG] = conf->readBoolEntry ("ShowUserMsg", TRUE);
 if (!conf->hasKey ("ShowUserMsg"))
 {
  conf->writeEntry ("ShowUserMsg", TRUE);
  log->writeLog ((char*) "<Main/ShowUserMsg> bejegyzés nem található! Lérehozva..");
 }
 chkShow[OTHER] = conf->readBoolEntry ("ShowOther", TRUE);
 if (!conf->hasKey ("ShowOther"))
 {
  conf->writeEntry ("ShowOther", TRUE);
  log->writeLog ((char*) "<Main/ShowOther> bejegyzés nem található! Lérehozva..");
 }
 if (conf->hasGroup ("Fortunes"))
  conf->setGroup (QString ("Fortunes"));
 else
 {
  conf->setGroup (QString ("Fortunes"));
  log->writeLog ((char*) "<Fortunes> csoport nem található! Lérehozva..");
 }
 chkShow[FORTUNES] = conf->readBoolEntry ("ShowFortunes", TRUE);
 if (!conf->hasKey ("ShowFortunes"))
 {
  conf->writeEntry ("ShowFortunes", TRUE);
  log->writeLog ((char*) "<Fortunes/ShowFortunes> bejegyzés nem található! Lérehozva..");
 }
 chkShow[FORTSTART] = conf->readBoolEntry ("AtStart", TRUE);
 if (!conf->hasKey ("AtStart"))
 {
  conf->writeEntry ("AtStart", TRUE);
  log->writeLog ((char*) "<Fortunes/AtStart> bejegyzés nem található! Lérehozva..");
 }
 chkShow[FORTSPEC] = conf->readBoolEntry ("Specified", TRUE);
 if (!conf->hasKey ("Specified"))
 {
  conf->writeEntry ("Specified", TRUE);
  log->writeLog ((char*) "<Fortunes/Specified> bejegyzés nem található! Lérehozva..");
 }
 strRet = conf->readEntry ("ShowInterval");
 if (strRet == QString::null)
 {
  conf->writeEntry ("ShowInterval", 60);
  cFortuneInterval = 60;
  log->writeLog ((char*) "<Fortunes/ShowInterval> bejegyzés nem található! Lérehozva..");
 }
 else
 {
  cFortuneInterval = strRet.toInt();
 }
 conf->sync();
 log->closeLog();

 pipe->setConfig (chkShow);

 spinShowTime->setValue (cPopupTimeout / 1000);
 chkShowInstall->setChecked (chkShow[INSTALL]);
 chkShowUpgrade->setChecked (chkShow[UPGRADE]);
 chkShowUninstall->setChecked (chkShow[UNINSTALL]);
 chkShowError->setChecked (chkShow[ERROR]);
 chkShowUpdate->setChecked (chkShow[UPDATE]);
 chkShowClub->setChecked (chkShow[CLUB]);
 chkShowUserMsg->setChecked (chkShow[USERMSG]);
 chkShowOther->setChecked (chkShow[OTHER]);
 chkFortunes->setChecked (chkShow[FORTUNES]);
 chkFortStart->setChecked (chkShow[FORTSTART]);
 chkFortSpec->setChecked (chkShow[FORTSPEC]);
 if (!chkShow[FORTUNES])
 {
  chkFortStart->setDisabled(TRUE);
  chkFortSpec->setDisabled(TRUE);
  spinFortMinute->setDisabled(TRUE);
  labFortMinute->setDisabled(TRUE);
 }
 else if (!chkShow[FORTSPEC])
 {
  spinFortMinute->setDisabled(TRUE);
  labFortMinute->setDisabled(TRUE);
 }
 
 menu = tray->contextMenu();
 menu->setCheckable (TRUE);
 popup = new KPassivePopup (tray, "popitem", Qt::WStyle_Customize | Qt::WDestructiveClose | Qt::WX11BypassWM | Qt::WStyle_StaysOnTop | Qt::WStyle_Tool | Qt::WStyle_NoBorder);
 popup->setTimeout (cPopupTimeout);
 popView = new CMsgView (popup, "popview");
 popup->setView (popView->getBox());
 
 if (chkShow[FORTSTART] and chkShow[FORTUNES]) slotShowFortune();
 if (chkShow[FORTUNES]) startFortunes();

 pipe = new CComm();
 pipe->link();

 timer = new QTimer (this);
 connect (timer, SIGNAL (timeout()), this, SLOT (slotTimerDone()));
 timer->start (250);

 menu->clear();
 action[TOGGLE] = (KToggleAction*) new KAction ("Rejt/&mutat", tray->loadIcon ("window_list"), 0, tray, SLOT (toggleActive()), this, "std_showhide");
 action[QUIT] = (KToggleAction*) new KAction ("&Kilépés", tray->loadIcon ("exit"), 0, this, SLOT (slotClose()), this, "std_quit");
 menu->insertTitle ("Bubbled");
 action[TOGGLE]->plug (menu);
 menu->insertSeparator();
 action[QUIT]->plug (menu);
} // init()

void CBubbled::applySettings()
{
 cPopupTimeout = spinShowTime->text().toInt() * 1000;
 cFortuneInterval = spinFortMinute->text().toInt();
 chkShow[INSTALL] = chkShowInstall->isChecked();
 chkShow[UPGRADE] = chkShowUpgrade->isChecked();
 chkShow[UNINSTALL] = chkShowUninstall->isChecked();
 chkShow[ERROR] = chkShowError->isChecked();
 chkShow[UPDATE] = chkShowUpdate->isChecked();
 chkShow[CLUB] = chkShowClub->isChecked();
 chkShow[USERMSG] = chkShowUserMsg->isChecked();
 chkShow[OTHER] = chkShowOther->isChecked();
 chkShow[FORTUNES] = chkFortunes->isChecked();
 chkShow[FORTSTART] = chkFortStart->isChecked();
 chkShow[FORTSPEC] = chkFortSpec->isChecked();

 popup->setTimeout (cPopupTimeout);
 pipe->setConfig (chkShow);
 if (!chkShow[FORTUNES])
 {
  chkFortStart->setDisabled (TRUE);
  chkFortSpec->setDisabled (TRUE);
  spinFortMinute->setDisabled (TRUE);
  labFortMinute->setDisabled (TRUE);
 }
 else if (!chkShow[FORTSPEC])
 {
  spinFortMinute->setDisabled (TRUE);
  labFortMinute->setDisabled (TRUE);
 }
 if (chkShow[FORTUNES]) startFortunes();

 conf->setGroup (QString ("Main"));
 conf->writeEntry ("PopupTimeout", cPopupTimeout);
 conf->writeEntry ("ShowInstall", chkShow[INSTALL]);
 conf->writeEntry ("ShowUpgrade", chkShow[UPGRADE]);
 conf->writeEntry ("ShowUninstall", chkShow[UNINSTALL]);
 conf->writeEntry ("ShowError", chkShow[ERROR]);
 conf->writeEntry ("ShowUpdate", chkShow[UPDATE]);
 conf->writeEntry ("ShowClub", chkShow[CLUB]);
 conf->writeEntry ("ShowUserMsg", chkShow[USERMSG]);
 conf->writeEntry ("ShowOther", chkShow[OTHER]);
 conf->setGroup (QString ("Fortunes"));
 conf->writeEntry ("ShowFortunes", chkShow[FORTUNES]);
 conf->writeEntry ("AtStart", chkShow[FORTSTART]);
 conf->writeEntry ("Specified", chkShow[FORTSPEC]);
 conf->writeEntry ("ShowInterval", cFortuneInterval);
 conf->sync();
} // applySettings()

void CBubbled::startFortunes()
{
 if (chkShow[FORTUNES] and chkShow[FORTSPEC])
 {
  if (tFortune == NULL)
  {
   tFortune = new QTimer (this);
   connect (tFortune, SIGNAL (timeout()), this, SLOT (slotShowFortune()));
  }
  if (tFortune->isActive()) tFortune->changeInterval (cFortuneInterval * 60 * 1000);
  else tFortune->start (cFortuneInterval * 60 * 1000, FALSE);
 }
} // startFortunes()

void CBubbled::stopFortunes()
{
 if (tFortune != NULL)
 {
  if (tFortune->isActive()) tFortune->stop();
  delete tFortune;
  tFortune = NULL;
 }
} // stopFortunes()

QString CBubbled::sayFortune()
{
 CFile strFortune;
 char *path;

 path = (char*) malloc (10 + strlen (FORTUNESFILE) + 1);
 sprintf (path, "fortune > ", 10);
 path +=10;
 sprintf (path, FORTUNESFILE, strlen (FORTUNESFILE));
 path -= 10;
 path[10 + strlen (FORTUNESFILE)] = '\0';
 system (path);
 delete path;
 
 return QString (strFortune.getContent (FORTUNESFILE));
} // sayFortune()

void CBubbled::slotTimerDone()
{
 pipe->listen();

 if (!pipe->empty)
 {
  switch (pipe->typenum)
  {
   case INSTALL:
    if (pipe->comm != NULL)
    {
     popView->fill ("Rendszerüzenet", QString ("A(z) <b>%1</b> program és az esetleges függõségek telepítése sikeresen befejezõdött<br><br>%2").arg (QString::fromLocal8Bit (pipe->name)).arg (QString::fromLocal8Bit (pipe->comm)), SmallIcon ("hint"));
    }
    else
    {
     popView->fill ("Rendszerüzenet", QString ("A(z) <b>%1</b> program és az esetleges függõségek telepítése sikeresen befejezõdött").arg (QString::fromLocal8Bit (pipe->name)), SmallIcon ("hint"));
    }
    break;
   case UPGRADE:
    if (pipe->comm != NULL)
    {
     popView->fill ("Rendszerüzenet", QString ("A(z) <b>%1</b> program frissítése sikeresen befejezõdött<br><br>%2").arg (QString::fromLocal8Bit (pipe->name)).arg (QString::fromLocal8Bit (pipe->comm)), SmallIcon ("hint"));
    }
    else
    {
     popView->fill ("Rendszerüzenet", QString ("A(z) <b>%1</b> program frissítése sikeresen befejezõdött").arg (QString::fromLocal8Bit (pipe->name)), SmallIcon ("hint"));
    }
    break;
   case UNINSTALL:
    if (pipe->comm != NULL)
    {
     popView->fill ("Rendszerüzenet", QString ("A(z) <b>%1</b> program eltávolítása sikeresen befejezõdött<br><br>%2").arg (QString::fromLocal8Bit (pipe->name)).arg (QString::fromLocal8Bit (pipe->comm)), SmallIcon ("hint"));
    }
    else
    {
     popView->fill ("Rendszerüzenet", QString ("A(z) <b>%1</b> program eltávolítása sikeresen befejezõdött").arg (QString::fromLocal8Bit (pipe->name)), SmallIcon ("hint"));
    }
    break;
   case ERROR:
    if (pipe->comm != NULL)
    {
     popView->fill ("Hiba", QString ("Hiba történt a(z) <b>%1</b> programban<br><br>%2").arg (QString::fromLocal8Bit (pipe->name)).arg (QString::fromLocal8Bit (pipe->comm)), SmallIcon ("error"));
    }
    else
    {
     popView->fill ("Hiba", QString ("Hiba történt a(z) <b>%1</b> programban").arg (QString::fromLocal8Bit (pipe->name)), SmallIcon ("error"));
    }
    break;
   case UPDATE:
    if (pipe->comm != NULL)
    {
     popView->fill ("Rendszerüzenet", QString ("A(z) <b>%1</b> programhoz frissítés telepíthetõ<br><br>%2").arg (QString::fromLocal8Bit (pipe->name)).arg (QString::fromLocal8Bit (pipe->comm)), SmallIcon ("error"));
    }
    else
    {
     popView->fill ("Rendszerüzenet", QString ("A(z) <b>%1</b> programhoz frissítés telepíthetõ").arg (QString::fromLocal8Bit (pipe->name)), SmallIcon ("error"));
    }
    break;
   case CLUB:
    if (pipe->comm != NULL)
    {
     popView->fill ("Fan Club", QString ("Újdonság a Clubban: <b>%1</b><br><br>%2").arg (QString::fromLocal8Bit (pipe->name)).arg (QString::fromLocal8Bit (pipe->comm)), SmallIcon ("error"));
    }
    else
    {
     popView->fill ("FanClub", QString ("Újdonság a Clubban: <b>%1</b>").arg (QString::fromLocal8Bit (pipe->name)), SmallIcon ("error"));
    }
    break;
   case USERMSG:
    if (pipe->comm != NULL)
    {
     popView->fill (QString ("<b>%1</b> üzeni:").arg (QString::fromLocal8Bit (pipe->name)), QString::fromLocal8Bit (pipe->comm), SmallIcon ("error"));
    }
    else
    {
     popView->fill (QString ("<b>%1</b> üzeni:").arg (QString::fromLocal8Bit (pipe->name)), QString::fromLocal8Bit (pipe->comm), SmallIcon ("error"));
    }
    break;
   case OTHER:
    if (pipe->comm != NULL)
    {
     popView->fill (QString::fromLocal8Bit (pipe->name), QString::fromLocal8Bit (pipe->comm), SmallIcon ("hint"));
    }
    else
     popView->fill (QString::fromLocal8Bit (pipe->name), QString (""), SmallIcon ("hint"));
    break;
   default:
    break;
  }
  if (pipe->typenum > 0)
  {
   popup->show();
   QTimer::singleShot (100, this, SLOT (slotPlaySound()));
   pipe->typenum = 0;
  }
 }
 pipe->empty = true;
} // slotTimerDone()

void CBubbled::slotSave()
{
 applySettings();
 hide();
} // slotSave()

void CBubbled::slotApply()
{
 applySettings();
} // slotApply()

void CBubbled::slotCancel()
{
 hide();
 spinShowTime->setValue (cPopupTimeout / 1000);
 chkShowInstall->setChecked (chkShow[INSTALL]);
 chkShowUpgrade->setChecked (chkShow[UPGRADE]);
 chkShowUninstall->setChecked (chkShow[UNINSTALL]);
 chkShowError->setChecked (chkShow[ERROR]);
 chkShowUpdate->setChecked (chkShow[UPDATE]);
 chkShowClub->setChecked (chkShow[CLUB]);
 chkShowUserMsg->setChecked (chkShow[USERMSG]);
 chkShowOther->setChecked (chkShow[OTHER]);
} // slotCancel()

void CBubbled::slotClose()
{
 delete this;
 exit (0);
} // slotClose()

void CBubbled::slotShowFortune()
{
 popView->fill (QString ("Fortunes"), sayFortune(), SmallIcon ("hint"));
 popup->show();
} // slotShowFortune()

void CBubbled::slotPlaySound()
{
 //sound->play();
} // slotPlaySound()

#include "cbubbled.moc"
