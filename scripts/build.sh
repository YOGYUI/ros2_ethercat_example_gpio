#! /usr/sh
wd=${PWD}

if [[ "$OSTYPE" == "darwin"* ]]; then
    script_path=$(dirname $(realpath $0))
else
    script_path=$(dirname $(realpath $BASH_SOURCE))
fi
package_name=$(basename $(dirname $(script_path)))
ws_path=$(dirname $(dirname $(dirname $(script_path))))

cd ${ws_path}
colcon build --packages-select ${package_name} --symlink-install

cd ${wd}