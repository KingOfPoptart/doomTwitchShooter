#brew install sdl2

./cltools.sh

FOLDER="restful-doom"

if [ ! -d "$FOLDER" ] ; then
  git clone https://github.com/jeff-1amstudios/restful-doom "$FOLDER"
fi

cd $FOLDER
./configure-and-build.sh
make