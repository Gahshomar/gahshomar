#ifndef __GAHSHOMARAPI_H
#define __GAHSHOMARAPI_H

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <time.h>
#include <jalali/jtime.h>
#include <jalali/jalali.h>
#include <glib-object.h>
#include <gio/gio.h>


#define GAH_SHOMAR_API_TYPE (gah_shomar_api_get_type ())
#define GAH_SHOMAR_API(obj) (G_TYPE_CHECK_INSTANCE_CAST ((obj), GAH_SHOMAR_API_TYPE, GahshomarApi))


typedef struct _GahshomarApi       GahshomarApi;
typedef struct _GahshomarApiClass  GahshomarApiClass;


GType           gah_shomar_api_get_type    (void);
GahshomarApi     *gah_shomar_api_new         (void);
extern int jalali_to_farsi(char* buf, size_t n, int padding, char* pad, int d);
extern void gah_shomar_api_get_date(GahshomarApi *api, gchar *s);
extern void gah_shomar_api_get_day(GahshomarApi *api, gchar *s);

/* Introspection data for the service we are exporting */
static const gchar introspection_xml[] =
  "<node>"
  "  <interface name='org.gahshomar.Api'>"
  "    <method name='GetDay'>"
  "      <arg type='s' name='day' direction='out'/>"
  "    </method>"
  "    <method name='GetDate'>"
  "      <arg type='s' name='date' direction='out'/>"
  "    </method>"
  "  </interface>"
  "</node>";


#endif /* __GAHSHOMARAPI_H */
