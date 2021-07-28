# Makefile for system configuration variables.

# Version info.
PY = 3

# Operating system.
OS = $(shell uname -o)

# OS and drive variables.
ifeq (${OS}, GNU/Linux)
PYTHON = python$(PY)
OSNAME = linux
LINUX = true
endif

ifeq (${OS}, Msys)
PYTHON = py -$(PY)
OSNAME = windows
WINDOWS = true
endif
