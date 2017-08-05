#Install chocolate Doom
#git clone https://github.com/chocolate-doom/chocpkg
#cd chocpkg/chocpk/
#./chocpkg install native:autotools
#./chocpkg install chocolate-doom
#cd ../../
brew install sdl2

FOLDER="restful-doom"

if [ ! -d "$FOLDER" ] ; then
  git clone https://github.com/jeff-1amstudios/restful-doom "$FOLDER"
fi

cd $FOLDER
./configure-and-build.sh
cd ./chocpkg/chocpkg/
./chocpkg install native:autotools
cd ../../
./configure-and-build.sh
make