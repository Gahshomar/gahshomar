## Process this file with automake to produce Makefile.in

ACLOCAL_AMFLAGS = -I m4

MAINTAINERCLEANFILES = \
	$(srcdir)/aclocal.m4 \
	$(srcdir)/autoscan.log \
	$(srcdir)/compile \
	$(srcdir)/config.guess \
	$(srcdir)/config.h.in \
	$(srcdir)/config.sub \
	$(srcdir)/configure.scan \
	$(srcdir)/depcomp \
	$(srcdir)/install-sh \
	$(srcdir)/ltmain.sh \
	$(srcdir)/missing \
	$(srcdir)/mkinstalldirs \
	$(srcdir)/py-compile \
	$(srcdir)/plugins/main/__pycache__/
	$(srcdir)/src/python/gahshomar/__pycache__/
	$(srcdir)/src/python/gahshomar/khayyam/__pycache__/


GITIGNOREFILES = m4/ 
distdir = gahshomar-$(VERSION)

SUBDIRS = \
	src/c \
	src/python/gahshomar \
	po \
	data \
	frontend/applet/gnome-shell \
	help \
	plugins/main \
	plugins/appindicator \
	plugins/statusicon

dist_doc_DATA = \
	README \
	COPYING \
	AUTHORS \
	ChangeLog \
	INSTALL \
	NEWS


# INTLTOOL_FILES = intltool-extract.in
# 	intltool-merge.in
# 	intltool-update.in

# DEBIAN_FILES =
# 	debian/changelog
# 	debian/compat
# 	debian/control
# 	debian/copyright
# 	debian/rules
# 	debian/docs
# 	debian/source/format 


# EXTRA_DIST = 
# 	$(DEBIAN_FILES)
# 	$(INTLTOOL_FILES)

DISTCLEANFILES = intltool-extract \
	intltool-merge \
	intltool-update \
	po/.intltool-merge-cache


# Remove doc directory on uninstall
uninstall-local:
	-rm -r $(docdir)

-include $(top_srcdir)/git.mk
