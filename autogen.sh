#!/bin/sh

set -e

test -n "$srcdir" || srcdir=`dirname "$0"`
test -n "$srcdir" || srcdir=.

olddir=`pwd`
cd "$srcdir"

# This will run autoconf, automake, etc. for us
autoreconf --force --install

cd "$olddir"

if test -z "$NOCONFIGURE"; then
  "$srcdir"/configure "$@"
fi
# #!/bin/bash
# # Run this to generate all the initial makefiles, etc.

# srcdir=`dirname $0`
# test -z "$srcdir" && srcdir=.

# PKG_NAME="gahshomar"

# test -f $srcdir/configure.ac || {
#     echo -n "**Error**: Directory "\`$srcdir\'" does not look like the"
#     echo " top-level gahshomar directory"
#     exit 1
# }

# which gnome-autogen.sh || {
#     echo "You need to install gnome-common from GNOME Git (or from"
#     echo "your OS vendor's package manager)."
#     exit 1
# }

# (cd "$srcdir" ;
# test -d m4 || mkdir m4/ ;
# git submodule update --init --recursive ;
# )
# touch AUTHORS
# . gnome-autogen.sh
