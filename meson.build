project('gahshomar',
  version: '5.0.2',
  meson_version: '>= 0.50.0',
)
i18n = import('i18n')

subdir('data')
subdir('src')
subdir('po')
meson.add_install_script('build-aux/meson/postinstall.py')
