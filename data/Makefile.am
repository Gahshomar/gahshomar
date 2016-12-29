# resource_files = $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --sourcedir=$(builddir) --generate-dependencies $(builddir)/gahshomar.gresource.xml) 
# gahshomar.gresource: gahshomar.gresource.xml $(resource_files)
# 	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) --sourcedir=$(builddir) $<

# resourcedir = $(pkgdatadir)
# resource_DATA = gahshomar.gresource

appsdir = $(datadir)/applications
apps_DATA = gahshomar.desktop

@INTLTOOL_DESKTOP_RULE@

appdatadir = $(datadir)/appdata
appdata_DATA = $(appdata_in_files:.xml.in=.xml)
appdata_in_files = gahshomar.appdata.xml.in

@INTLTOOL_XML_RULE@

man1_MANS = gahshomar.1

# hicolor icons
hicolor_icon16dir = $(datadir)/icons/hicolor/16x16/apps
hicolor_icon16_DATA = icons/hicolor/16x16/apps/gahshomar.png
hicolor_icon22dir = $(datadir)/icons/hicolor/22x22/apps
hicolor_icon22_DATA = icons/hicolor/22x22/apps/gahshomar.png
hicolor_icon24dir = $(datadir)/icons/hicolor/24x24/apps
hicolor_icon24_DATA = icons/hicolor/24x24/apps/gahshomar.png
hicolor_icon32dir = $(datadir)/icons/hicolor/32x32/apps
hicolor_icon32_DATA = icons/hicolor/32x32/apps/gahshomar.png
hicolor_icon48dir = $(datadir)/icons/hicolor/48x48/apps
hicolor_icon48_DATA = icons/hicolor/48x48/apps/gahshomar.png \
	icons/hicolor/48x48/apps/org.gahshomar.Gahshomar-no-icon.png
hicolor_icon64dir = $(datadir)/icons/hicolor/64x64/apps
hicolor_icon64_DATA = icons/hicolor/64x64/apps/gahshomar.png
hicolor_icon96dir = $(datadir)/icons/hicolor/96x96/apps
hicolor_icon96_DATA = icons/hicolor/96x96/apps/gahshomar.png
hicolor_icon256dir = $(datadir)/icons/hicolor/256x256/apps
hicolor_icon256_DATA = icons/hicolor/256x256/apps/gahshomar.png
hicolor_iconscalable256dir = $(datadir)/icons/hicolor/scalable/apps
hicolor_iconscalable256_DATA = icons/hicolor/scalable/apps/gahshomar.svg
hicolor_icon_files = \
	$(hicolor_icon16_DATA) \
	$(hicolor_icon22_DATA) \
	$(hicolor_icon24_DATA) \
	$(hicolor_icon32_DATA) \
	$(hicolor_icon48_DATA) \
	$(hicolor_icon64_DATA) \
	$(hicolor_icon96_DATA) \
	$(hicolor_icon256_DATA) \
	$(hicolor_iconscalable256_DATA) \
	icons/hicolor/gahshomar.svg

hicontrast_icon16dir = $(datadir)/icons/HighContrast/16x16/apps
hicontrast_icon16_DATA = icons/HighContrast/16x16/apps/gahshomar.png
hicontrast_icon22dir = $(datadir)/icons/HighContrast/22x22/apps
hicontrast_icon22_DATA = icons/HighContrast/22x22/apps/gahshomar.png
hicontrast_icon24dir = $(datadir)/icons/HighContrast/24x24/apps
hicontrast_icon24_DATA = icons/HighContrast/24x24/apps/gahshomar.png
hicontrast_icon32dir = $(datadir)/icons/HighContrast/32x32/apps
hicontrast_icon32_DATA = icons/HighContrast/32x32/apps/gahshomar.png
hicontrast_icon48dir = $(datadir)/icons/HighContrast/48x48/apps
hicontrast_icon48_DATA = icons/HighContrast/48x48/apps/gahshomar.png
hicontrast_icon64dir = $(datadir)/icons/HighContrast/64x64/apps
hicontrast_icon64_DATA = icons/HighContrast/64x64/apps/gahshomar.png
hicontrast_icon96dir = $(datadir)/icons/HighContrast/96x96/apps
hicontrast_icon96_DATA = icons/HighContrast/96x96/apps/gahshomar.png
hicontrast_icon256dir = $(datadir)/icons/HighContrast/256x256/apps
hicontrast_icon256_DATA = icons/HighContrast/256x256/apps/gahshomar.png
hicontrast_iconscalable256dir = $(datadir)/icons/HighContrast/scalable/apps
hicontrast_iconscalable256_DATA = icons/HighContrast/scalable/apps/gahshomar.svg
hicontrast_icon_files = \
	$(hicontrast_icon16_DATA) \
	$(hicontrast_icon22_DATA) \
	$(hicontrast_icon24_DATA) \
	$(hicontrast_icon32_DATA) \
	$(hicontrast_icon48_DATA) \
	$(hicontrast_icon64_DATA) \
	$(hicontrast_icon96_DATA) \
	$(hicontrast_icon256_DATA) \
	$(hicontrast_iconscalable256_DATA) \
	icons/HighContrast/gahshomar.svg

gtk_update_hicolor_icon_cache = gtk-update-icon-cache -f -t $(datadir)/icons/hicolor
gtk_update_hicontrast_icon_cache = gtk-update-icon-cache -f -t $(datadir)/icons/HighContrast

install-data-hook: update-icon-cache
uninstall-hook: update-icon-cache
update-icon-cache:
	@-if test -z "$(DESTDIR)"; then \
		echo "Updating Gtk hicolor icon cache."; \
		$(gtk_update_hicolor_icon_cache); \
		echo "Updating Gtk highcontrast icon cache."; \
		$(gtk_update_hicontrast_icon_cache); \
	else \
		echo "*** Icon cache not updated.  After (un)install, run this:"; \
		echo "***   $(gtk_update_hicolor_icon_cache)"; \
		echo "***   $(gtk_update_hicontrast_icon_cache)"; \
	fi


gsettings_SCHEMAS = org.gahshomar.Gahshomar.gschema.xml

# For uninstalled use
gschemas.compiled: $(gsettings_SCHEMAS) Makefile
	$(AM_V_GEN) $(GLIB_COMPILE_SCHEMAS) $(builddir)

@GSETTINGS_RULES@

EXTRA_DIST = \
	$(hicolor_icon_files) \
	$(hicontrast_icon_files) \
	$(resource_files) \
	gahshomar.appdata.xml.in \
	gahshomar.desktop.in \
	gahshomar.gresource.xml \
	org.gahshomar.Gahshomar.gschema.xml \
	$(man1_MANS) \
	$(NULL)

CLEANFILES = \
	gahshomar.gresource \
	gahshomar.appdata.xml \
	$(apps_DATA) \
	*.valid \
	gschemas.compiled \
	$(NULL)

all-local: gschemas.compiled

-include $(top_srcdir)/git.mk
