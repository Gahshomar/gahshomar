#include <gtk/gtk.h>
#include <libpeas/peas.h>

#include "gahshomar.h"

#include <glib/gi18n.h>

int
main (int argc, char *argv[])
{

  PeasEngine *engine;
  gchar *plugin_dir;

#ifdef ENABLE_NLS
    bindtextdomain (GETTEXT_PACKAGE, PACKAGE_LOCALE_DIR);
    bind_textdomain_codeset (GETTEXT_PACKAGE, "UTF-8");
    textdomain (GETTEXT_PACKAGE);
#endif

  // DEBUG
  /* Since this example is running uninstalled,
   * we have to help it find its schema. This
   * is *not* necessary in properly installed
   * application.
   */
  // g_setenv ("GSETTINGS_SCHEMA_DIR", "src", FALSE);
  // DEBUG

  engine = peas_engine_get_default ();
  // /home/amir/.local/share/gahshomar/plugins
  plugin_dir = g_build_filename (g_get_user_data_dir (),
    "gahshomar/plugins", NULL);
  // DEBUG
  // printf("%s\n", plugin_dir);
  // DEBUG
  peas_engine_add_search_path (engine, plugin_dir, plugin_dir);
  g_free (plugin_dir);

  /* We don't care about leaking memory */
  // g_setenv ("PEAS_ALLOW_ALL_LOADERS", "1", TRUE);
  peas_engine_enable_loader (engine, "python3");
  // /usr/lib
  // /usr
  peas_engine_add_search_path (engine,
    g_build_filename(PEAS_LIBDIR, "gahshomar/plugins/", NULL),
    g_build_filename(PEAS_PREFIX, "share/gahshomar/plugins/", NULL));

  g_irepository_require (g_irepository_get_default (),
                       "Peas", "1.0", 0, NULL);
  // DEBUG
  // printf("%s\n%s\n", PEAS_LIBDIR, PEAS_PREFIX);
  // DEBUG

  return g_application_run (G_APPLICATION (gah_shomar_new ()), argc, argv);

  g_object_unref (engine);
}
