#!/usr/bin/env bash

xgettext --files-from=po/POTFILES --directory=. --output=po/gahshomar.pot
msgmerge --update --no-fuzzy-matching --backup=off po/fa.po po/gahshomar.pot
