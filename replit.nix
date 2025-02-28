{pkgs}: {
  deps = [
    pkgs.xorg.libXrender
    pkgs.xorg.libX11
    pkgs.tk
    pkgs.tcl
    pkgs.qhull
    pkgs.gtk3
    pkgs.gobject-introspection
    pkgs.ghostscript
    pkgs.freetype
    pkgs.ffmpeg-full
    pkgs.cairo
    pkgs.xsimd
    pkgs.pkg-config
    pkgs.libxcrypt
  ];
}
