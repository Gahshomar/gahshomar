# GTK_CFLAGS =			 		\
# 	-I$(top_srcdir)				\
# 	$(GTK_DEP_CFLAGS)

# GTK_LIBS = 					\
#         $(top_builddir)/gtk/libgtk-3.la 	\
#         $(top_builddir)/gdk/libgdk-3.la 	\
#         $(GTK_DEP_LIBS)

AM_CPPFLAGS = \
	-DPACKAGE_LOCALE_DIR=\""$(localedir)"\" \
	-DPACKAGE_SRC_DIR=\""$(srcdir)"\" \
	-DPACKAGE_DATA_DIR=\""$(pkgdatadir)"\" \
	$(GAHSHOMAR_CFLAGS)

AM_CFLAGS =\
	 -Wall\
	 -g

bin_PROGRAMS = gahshomar

# noinst_PROGRAMS = gahshomar

# gahshomar_CFLAGS = $(GTK_CFLAGS)
gahshomar_CFLAGS = \
	-DPEAS_LIBDIR="\"$(libdir)\"" \
	-DPEAS_PREFIX="\"$(prefix)\""

# gahshomar_LDADD = $(GAHSHOMAR_LIBS) /usr/lib/libjalali.la
gahshomar_LDADD = $(GAHSHOMAR_LIBS) -ljalali
# libjalali_LIBADD = libjalali.la
gahshomar_SOURCES = 				\
	main.c 					\
	gahshomar.c gahshomar.h 		\
	gahshomarapi.c gahshomarapi.h 	\
	resources.c

# gahshomar_LDFLAGS =  -ljalali 
gahshomar_LDFLAGS = 
# gahshomar_LDFLAGS = -I/usr/include/jalali/ -L/usr/lib/ -ljalali


if PLATFORM_WIN32
gahshomar_LDFLAGS += -Wl,--export-all-symbols
else
gahshomar_LDFLAGS += -Wl,--export-dynamic
endif

if NATIVE_WIN32
gahshomar_LDFLAGS += -mwindows
endif

BUILT_SOURCES = 				\
	resources.c 				\
	gschemas.compiled

resources.c: ../../data/gahshomar.gresource.xml $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=../../data --generate-dependencies ../../data/gahshomar.gresource.xml)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) ../../data/gahshomar.gresource.xml \
		--target=$@ --sourcedir=../../data --generate-source

gsettings_SCHEMAS = 				\
	../../data/org.gahshomar.Gahshomar.gschema.xml

@GSETTINGS_RULES@

gschemas.compiled: ../../data/org.gahshomar.Gahshomar.gschema.xml
	$(GLIB_COMPILE_SCHEMAS) .

EXTRA_DIST = \
    ../../data/app-menu.ui \
    ../../data/prefs.ui \
    ../../data/day-widget.ui \
    ../../data/months-widget.ui \
    ../../data/calendar-widget.ui \
    ../../data/AboutDialog.ui \
	../../data/gahshomar.gresource.xml 		\
	../../data/org.gahshomar.Gahshomar.gschema.xml

CLEANFILES = 					\
	gschemas.compiled

-include $(top_srcdir)/git.mk

