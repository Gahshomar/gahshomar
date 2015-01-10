#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "gahshomarapi.h"
#include <stdio.h>


struct _GahshomarApi
{
  GObject parent;
};

struct _GahshomarApiClass
{
  GObjectClass parent_class;
};

G_DEFINE_TYPE(GahshomarApi, gah_shomar_api, G_TYPE_OBJECT);


extern void
gah_shomar_api_get_date(GahshomarApi *api, gchar *s)
{
  size_t size;
  char buf[250];
  struct jtm j;
  time_t ts;
  gchar _la[100];
  gchar _lb[100];
  gchar wday[100];
  gchar mon[100];

  time(&ts);
  jlocaltime_r(&ts, &j);
  jmktime(&j);
  size = jstrftime(wday, 100, "%G", &j);
  size = jstrftime(mon, 100, "%V", &j);
  jalali_to_farsi(_la, 100, 2, "۰", (&j)->tm_mday);
  jalali_to_farsi(_lb, 100, 0, " ", (&j)->tm_year);
  snprintf(buf, 250, "%s %s %s %s", wday, _la, mon, _lb);
  // s = g_strdup (buf);
  g_stpcpy(s, buf);
  // The returned string should be freed with g_free() when no longer needed.
}

extern void
gah_shomar_api_get_day(GahshomarApi *api, gchar *s)
{

  struct jtm j;
  time_t ts;
  gchar _la[100];

  time(&ts);
  jlocaltime_r(&ts, &j);
  jmktime(&j);
  jalali_to_farsi(_la, 100, 2, "۰", (&j)->tm_mday);
  // s = g_strdup (_la);
  g_stpcpy(s, _la);
  // The returned string should be freed with g_free() when no longer needed.

}



static void
gah_shomar_api_init (GahshomarApi *api)
{
}

static void
gah_shomar_api_class_init (GahshomarApiClass *class)
{
}

GahshomarApi *
gah_shomar_api_new (void)
{
  return g_object_new (GAH_SHOMAR_API_TYPE,
                       NULL);
}
