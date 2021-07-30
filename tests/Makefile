# Makefile for tests.

# TODO: add unit tests with pytest

include ../conf/Makefile.conf

FIRST    = test-original
SECOND   = test-modified
DIFF     = $(PYTHON) -m xldiff
SUFFIXES = xlsx xls

all: test

test:
	@ for ext in $(SUFFIXES); do					\
	    echo Testing $$ext;  					\
	    exp=expected-$$ext.diff;					\
	    res=result-$$ext.diff;					\
	    $(DIFF) $(FIRST).$$ext $(SECOND).$$ext -o $$res;		\
	    diff $$exp $$res;	   		      			\
	done

clean:
	rm -f result-*.diff
