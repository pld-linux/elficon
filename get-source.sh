#!/bin/sh
package=elfres
version=0.6.0

dir=$package-$version
archive=$package-$version-bzr.tar.xz

set -e

if [ ! -d $dir ]; then
	install -d $dir
	cd $dir
	bzr branch lp:~ehoover/elfres/libr
	bzr branch lp:~ehoover/elfres/elfres
	bzr branch lp:~ehoover/elfres/gnome-elf-thumbnailer
	cd ..
else
	cd $dir/libr
	bzr pull
	cd ../elfres
	bzr pull
	cd ../gnome-elf-thumbnailer
	bzr pull
	cd ../..
fi

tar -cJf $archive --exclude-vcs $dir
