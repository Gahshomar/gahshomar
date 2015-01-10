#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <gtk/gtk.h>

#include "gahshomar.h"
#include "gahshomarwin.h"
// #include "gahshomarprefs.h"
#include "gahshomarapi.h"

struct _Gahshomar
{
  GtkApplication parent;
  // PeasEngine *engine;
};

struct _GahshomarClass
{
  GtkApplicationClass parent_class;
};

G_DEFINE_TYPE(Gahshomar, gah_shomar, GTK_TYPE_APPLICATION);

// GDBus
static GDBusNodeInfo *introspection_data = NULL;

static void
handle_method_call (GDBusConnection       *connection,
                    const gchar           *sender,
                    const gchar           *object_path,
                    const gchar           *interface_name,
                    const gchar           *method_name,
                    GVariant              *parameters,
                    GDBusMethodInvocation *invocation,
                    gpointer               user_data)
{
  GahshomarApi *api = user_data;

  if (g_strcmp0 (method_name, "GetDay") == 0)
    {
      gchar day[250];
      // g_variant_get (parameters, "(s)", &day);

      gah_shomar_api_get_day (api, day);

      g_dbus_method_invocation_return_value (invocation, 
        g_variant_new ("(s)", day));
      // g_free(day);
    }
  if (g_strcmp0 (method_name, "GetDate") == 0)
    {
      gchar date[250];
      // g_variant_get (parameters, "(s)", &date);

      gah_shomar_api_get_date (api, date);

      g_dbus_method_invocation_return_value (invocation, g_variant_new ("(s)", date));
      // g_free(date);
    }
}

/* for now */
static const GDBusInterfaceVTable interface_vtable =
{
  handle_method_call,
};

static guint registration_id;


static gboolean
gah_shomar_dbus_register (GApplication              *application,
                          GDBusConnection           *connection,
                          const gchar               *object_path,
                          GError                   **error)
{
  static guint registration_id;
  GahshomarApi *api;
  // GDBusConnection *connection;

  introspection_data = g_dbus_node_info_new_for_xml (introspection_xml, NULL);
  g_assert (introspection_data != NULL);

  // connection = g_application_get_dbus_connection (application);
  api = g_object_new (gah_shomar_api_get_type (), NULL);
  registration_id = g_dbus_connection_register_object (connection,
                                                       object_path,
                                                       introspection_data->interfaces[0],
                                                       &interface_vtable,
                                                       api,
                                                       NULL,  /* user_data_free_func */
                                                       NULL); /* GError** */
  g_assert (registration_id > 0);

  return TRUE;
}

static void
gah_shomar_dbus_unregister (GApplication              *application,
                            GDBusConnection           *connection,
                            const gchar               *object_path)
{
  static guint registration_id;
  g_dbus_connection_unregister_object(connection, registration_id);
}

//GDBus

static void
on_extension_added (PeasExtensionSet *set,
                    PeasPluginInfo   *info,
                    PeasExtension    *exten,
                    GahshomarWindow       *win)
{
  peas_activatable_activate (PEAS_ACTIVATABLE (exten));
}

static void
on_extension_removed (PeasExtensionSet *set,
                      PeasPluginInfo   *info,
                      PeasExtension    *exten,
                      GahshomarWindow       *win)
{
  peas_activatable_deactivate (PEAS_ACTIVATABLE (exten));
}

static void
gah_shomar_init (Gahshomar *app)
{
  // DEBUG
  // GahshomarApi *api;
  // api = gah_shomar_api_new ();
  // DEBUG
}


static void
quit_activated (GSimpleAction *action,
                GVariant      *parameter,
                gpointer       app)
{
  GSettings *settings;
  settings = g_settings_new ("org.gahshomar.Gahshomar");
  g_settings_set_value(settings, "app-crashed", g_variant_new_boolean(FALSE));
  g_application_quit (G_APPLICATION (app));
}

static GActionEntry app_entries[] =
{
  // { "preferences", preferences_activated, NULL, NULL, NULL },
  { "quit", quit_activated, NULL, NULL, NULL }
};

static void
gah_shomar_startup (GApplication *app)
{
  GtkBuilder *builder;
  GMenuModel *app_menu;
  const gchar *quit_accels[2] = { "<Ctrl>Q", NULL };
  const gchar *today_accels[2] = { "<Ctrl>T", NULL };
  PeasExtensionSet *exten_set;

  G_APPLICATION_CLASS (gah_shomar_parent_class)->startup (app);

  GSettings *settings;
  settings = g_settings_new ("org.gahshomar.Gahshomar");

  g_action_map_add_action_entries (G_ACTION_MAP (app),
                                   app_entries, G_N_ELEMENTS (app_entries),
                                   app);
  gtk_application_set_accels_for_action (GTK_APPLICATION (app),
                                         "app.quit",
                                         quit_accels);

  gtk_application_set_accels_for_action (GTK_APPLICATION (app),
                                         "win.today",
                                         today_accels);

  builder = gtk_builder_new_from_resource ("/org/gahshomar/Gahshomar/app-menu.ui");
  app_menu = G_MENU_MODEL (gtk_builder_get_object (builder, "appmenu"));
  gtk_application_set_app_menu (GTK_APPLICATION (app), app_menu);
  g_object_unref (builder);

  // add the extensions point
  exten_set = peas_extension_set_new (peas_engine_get_default (),
                                          PEAS_TYPE_ACTIVATABLE,
                                          "object", app,
                                          NULL);

  peas_extension_set_foreach (exten_set,
                              (PeasExtensionSetForeachFunc) on_extension_added,
                              app);

  g_signal_connect (exten_set, "extension-added",
                    G_CALLBACK (on_extension_added), app);
  g_signal_connect (exten_set, "extension-removed",
                    G_CALLBACK (on_extension_removed), app);

  // activate the main plugin
  peas_engine_load_plugin (peas_engine_get_default (),
   peas_engine_get_plugin_info(peas_engine_get_default (), "main"));

  // g_settings_set_value(settings, "app-crashed", g_variant_new("b", "true"));
  // DEBUG
  // peas_engine_load_plugin (peas_engine_get_default (),
  //  peas_engine_get_plugin_info(peas_engine_get_default (), "noheaderbar"));

  // preferences_activated(NULL, NULL, app);
  // DEBUG

}

static void
gah_shomar_activate (GApplication *app)
{
  GtkWindow *win;

  win = gtk_application_get_active_window (GTK_APPLICATION (app));
  gtk_window_present (win);
}

static void
gah_shomar_class_init (GahshomarClass *class)
{
  G_APPLICATION_CLASS (class)->startup = gah_shomar_startup;
  G_APPLICATION_CLASS (class)->activate = gah_shomar_activate;
  G_APPLICATION_CLASS (class)->dbus_register = gah_shomar_dbus_register;
  G_APPLICATION_CLASS (class)->dbus_unregister = gah_shomar_dbus_unregister;
}

Gahshomar *
gah_shomar_new (void)
{
  return g_object_new (GAH_SHOMAR_TYPE,
                       "application-id", "org.gahshomar.Gahshomar",
                       "flags", G_APPLICATION_FLAGS_NONE,
                       NULL);
}
