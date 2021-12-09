#!/bin/bash

echo "Setting up"
echo "===================="
echo ""
echo "Creating VirtualEnv"
echo "--------------------"
echo ""

virtualenv ENV &&
source ENV/bin/activate

echo ""
echo "Installing required dependencies"
echo "--------------------"
echo ""

pip3 install -r dependencies.txt
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ""
echo "=================="
echo "Setup completed"
echo "=================="
echo ""
echo "Run the following command"
echo "export PATH=\"$DIR:\$PATH\""
echo "=================="
echo ""
