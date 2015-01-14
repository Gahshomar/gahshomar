#include <gtk/gtk.h>
#include <libpeas/peas.h>

#include "gahshomar.h"

#include <glib.h>
#include <glib/gi18n.h>

/* Command line argument variables*/
gboolean verbose = FALSE;
gboolean minimized = FALSE;

static GOptionEntry entries[] =
{
  { "verbose", 'v', 0, G_OPTION_ARG_NONE, &verbose, N_("Be verbose"), NULL },
  { "minimized", 'm', 0, G_OPTION_ARG_NONE, &minimized, N_("Start minimized"), NULL },
};


int
main (int argc, char *argv[])
{

  GError *error = NULL;
  GOptionContext *context;

  PeasEngine *engine;
  gchar *plugin_dir;

#ifdef ENABLE_NLS
    bindtextdomain (GETTEXT_PACKAGE, PACKAGE_LOCALE_DIR);
    bind_textdomain_codeset (GETTEXT_PACKAGE, "UTF-8");
    textdomain (GETTEXT_PACKAGE);
#endif


  context = g_option_context_new (_("- Gahshomar, an Iranian Calendar"));
  g_option_context_add_main_entries (context, entries, GETTEXT_PACKAGE);
  g_option_context_add_group (context, gtk_get_option_group (TRUE));
  if (!g_option_context_parse (context, &argc, &argv, &error))
  {
    g_print ("option parsing failed: %s\n", error->message);
    return 1;
  }

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
