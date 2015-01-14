#ifndef __GAHSHOMAR_H
#define __GAHSHOMAR_H

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <gtk/gtk.h>
#include <libpeas/peas.h>


#define GAH_SHOMAR_TYPE (gah_shomar_get_type ())
#define GAH_SHOMAR(obj) (G_TYPE_CHECK_INSTANCE_CAST ((obj), GAH_SHOMAR_TYPE, Gahshomar))


typedef struct _Gahshomar       Gahshomar;
typedef struct _GahshomarClass  GahshomarClass;


GType           gah_shomar_get_type    (void);
Gahshomar     *gah_shomar_new         (void);

/* Command line argument variables*/
extern gboolean verbose;
extern gboolean minimized;

#endif /* __GAHSHOMAR_H */
