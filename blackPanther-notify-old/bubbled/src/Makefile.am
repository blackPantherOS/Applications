# set the include path for X, qt and KDE
INCLUDES = $(all_includes)

# these are the headers for your project


# let automoc handle all of the meta source files (moc)
METASOURCES = AUTO

messages: rc.cpp
	$(XGETTEXT) *.cpp -o $(podir)/bubbled.pot

KDE_ICON = bubbled

#########################################################################
# APPLICATION SECTION
#########################################################################
# this is the program that gets installed.  it's name is used for all
# of the other Makefile.am variables
bin_PROGRAMS = bubbled

# the application source, library search path, and link libraries
bubbled_SOURCES = main.cpp cbase.cpp bubbled.ui cbubbled.cpp
bubbled_LDFLAGS = $(KDE_RPATH) $(all_libraries)
bubbled_LDADD = $(LIB_KDEUI)

# this is where the desktop file will go 
shelldesktopdir   = $(kde_appsdir)/Utilities
shelldesktop_DATA = bubbled.desktop

# this is where the shell's XML-GUI resource file goes
shellrcdir   = $(kde_datadir)/bubbled


noinst_HEADERS = cbase.h cbubbled.h
