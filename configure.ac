dnl Process this file with autoconf to produce a configure script.

AC_INIT(gahshomar, 4.0)

AC_CONFIG_SRCDIR([Makefile.am])
AC_CONFIG_HEADERS([config.h])

AM_INIT_AUTOMAKE([1.11])

AM_SILENT_RULES([yes])

AC_PROG_CC
AM_PROG_LIBTOOL
AC_PROG_CPP
AC_PROG_CXX

AC_CONFIG_MACRO_DIRS([m4])

dnl ***************************************************************************
dnl Internationalization
dnl ***************************************************************************
IT_PROG_INTLTOOL([0.35.0])

GETTEXT_PACKAGE=gahshomar
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE",
                   [The prefix for our gettext translation domains.])
dnl IT_PROG_INTLTOOL(0.26)

YELP_HELP_INIT

AM_GLIB_GNU_GETTEXT



dnl ***************************************************************************
dnl Check for Windows
dnl ***************************************************************************
AC_CANONICAL_HOST

case $host_os in
  *mingw*)
    platform_win32=yes
    native_win32=yes
    ;;
  pw32* | *cygwin*)
    platform_win32=yes
    native_win32=no
    ;;
  *)
    platform_win32=no
    native_win32=no
    ;;
esac
AM_CONDITIONAL(PLATFORM_WIN32, test x"$platform_win32" = "xyes")
AM_CONDITIONAL(NATIVE_WIN32, test x"$native_win32" = "xyes")


LT_INIT([win32-dll])


PKG_CHECK_MODULES(GAHSHOMAR, [gtk+-3.0 >= 3.12.0, glib-2.0, libpeas-1.0, libpeas-gtk-1.0])

dnl ***************************************************************************
dnl GLIB_GSETTINGS and GLIB_COMPILE_RESOURCES
dnl ***************************************************************************

GOBJECT_INTROSPECTION_CHECK([0.9.3])

GLIB_GSETTINGS

GLIB_COMPILE_RESOURCES=`$PKG_CONFIG --variable glib_compile_resources gio-2.0`
AC_SUBST(GLIB_COMPILE_RESOURCES)

AM_PATH_PYTHON([3.3])

dnl GTK_DOC_CHECK([1.0])

dnl ***************************************************************************
dnl check for libjalali
dnl ***************************************************************************
AC_CHECK_LIB([jalali], [jstrftime], [],
  [ echo "*** ERROR: libjalali is not functional"; exit -1])


AC_CONFIG_FILES([
Makefile
src/c/Makefile
src/python/gahshomar/Makefile
src/python/gahshomar/khayyam/Makefile
data/Makefile
data/AboutDialog.ui
help/Makefile
po/Makefile.in
frontend/applet/gnome-shell/Makefile
plugins/main/Makefile
plugins/appindicator/Makefile
])

AC_OUTPUT
