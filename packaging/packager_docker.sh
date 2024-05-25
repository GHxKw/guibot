#!/bin/bash

readonly install_variant="${INSTALL_VARIANT:-pip}"
readonly packager=$(echo $install_variant | cut -d '.' -f 1)
readonly distro=$(echo $install_variant | cut -d '.' -f 2)
readonly version=$(echo $install_variant | cut -d '.' -f 3)

# Ensure the project directory is set correctly
project_dir=$(pwd)/..

# Create a virtual environment in the project directory
python3 -m venv $project_dir/venv

# Install necessary dependencies in the virtual environment
source $project_dir/venv/bin/activate
pip install --upgrade pip

# Run the Docker container with the virtual environment
if [ "$packager" == "rpm" ]; then
    sudo docker run \
        -e DISTRO="$distro" -e VERSION="$version" -e ROOT="/" \
        -v $project_dir:/guibot:rw $distro:$version \
        /bin/bash -c "
            source /guibot/venv/bin/activate && \
            /bin/bash /guibot/packaging/packager_rpm.sh
        "
elif [ "$packager" == "deb" ]; then
    sudo docker run \
        -e DISTRO="$distro" -e VERSION="$version" -e ROOT="/" \
        -v $project_dir:/guibot:rw $distro:$version \
        /bin/bash -c "
            source /guibot/venv/bin/activate && \
            /bin/bash /guibot/packaging/packager_deb.sh
        "
fi
