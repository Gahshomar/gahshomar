# Maintainer: Amir Mohammadi <183.amir@gmail.com>
pkgname=gahshomar
pkgver=4.4.0
pkgrel=1
pkgdesc="A Persian (Jalali/Farsi) calendar"
arch=(i686 x86_64)
url="https://gahshomar.github.io/gahshomar/"
license=('GPL3')
replaces=('persian-calendar')
conflicts=('persian-calendar')
depends=('python-gobject' 'jcal' 'libpeas')
makedepends=('intltool' 'yelp-tools' 'gnome-common' 'gobject-introspection')
optdepends=('libappindicator-gtk3: for the app indicator plugin'
			'gnome-shell: for the gnome-shell extension')
install=gahshomar.install
source=($pkgname-$pkgver.tar.gz::https://github.com/Gahshomar/gahshomar/releases/download/v$pkgver/gahshomar-$pkgver.tar.gz)
md5sums=('de24df8aabd349d407745be3ecb0a38b')

build() {
	cd $srcdir/$pkgname-$pkgver
	./configure --prefix=/usr --disable-schemas-compile
	make
}

package() {
	cd $srcdir/$pkgname-$pkgver
	make DESTDIR="${pkgdir}" install
}
