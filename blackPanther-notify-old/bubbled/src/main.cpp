/***************************************************************************
 *   Copyright (C) 2005 by Kov√°cs Tam√°s                                    *
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

#include <kuniqueapplication.h>
#include <kmainwindow.h>
#include <kaboutdata.h>
#include <kcmdlineargs.h>
#include <klocale.h>

#include "cbubbled.h"

static const char description[] = I18N_NOOP ("A KDE KPart Application");
static const char version[] = "0.1";
static KCmdLineOptions options[] =
{
 KCmdLineLastOption
};

int main (int argc, char **argv)
{
 KAboutData about ("bubbled", I18N_NOOP ("Bubbled"), version, description, KAboutData::License_GPL, "(C) %{YEAR} Kov·cs Tam·s", 0, 0, "kovacst@blackpanther.hu");
 about.addAuthor ("Kov·cs Tam·s", 0, "kovacst@blackpanther.hu");
 KCmdLineArgs::init (argc, argv, &about);
 KCmdLineArgs::addCmdLineOptions (options);
 KUniqueApplication app;
 CBubbled *mainWin = 0;

 if (app.isRestored())
 {
  int n = 1;

  while (KMainWindow::canBeRestored (n))
  {
   (new CBubbled)->restore (n, FALSE);
   n++;
  }
 }
 else
 {
  KCmdLineArgs *args = KCmdLineArgs::parsedArgs();
  mainWin = new CBubbled (0, "main_window", Qt::WType_TopLevel);
  mainWin->hide();

  args->clear();
 }

 return app.exec();
}
