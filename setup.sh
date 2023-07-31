#!/bin/bash

set -a
[ -f .env ] && . .env

# Setup .env file
cp .env.example .env
