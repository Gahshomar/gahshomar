pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'gahshomar')
gnome = import('gnome')
python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('URL', 'https://gahshomar.github.io/gahshomar/')

configure_file(
  input: 'gahshomar.in',
  output: 'gahshomar',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

about_dialog = configure_file(
  input: 'about-dialog.ui.in',
  output: 'about-dialog.ui',
  configuration: conf,
)

gnome.compile_resources('gahshomar',
  'gahshomar.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: about_dialog
)

gahshomar_sources = [
  '__init__.py',
  'api.py',
  'appindicator.py',
  'applet.py',
  'calendar.py',
  'date.py',
  'gi_composites.py',
  'main.py',
  'preferences.py',
  'statusicon.py',
  'widgets.py',
  'window.py',
]

install_data(gahshomar_sources, install_dir: moduledir)

khayyamdir = join_paths(moduledir, 'khayyam')
khayyam_sources = [
  'khayyam/__init__.py',
  'khayyam/algorithms.py',
  'khayyam/compat.py',
  'khayyam/constants.py',
  'khayyam/helpers.py',
  'khayyam/jalali_date.py',
  'khayyam/jalali_datetime.py',
  'khayyam/tehran_timezone.py',
]

install_data(khayyam_sources, install_dir: khayyamdir)
