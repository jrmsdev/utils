.PHONY: all
all:
	cd ./claude && ./build.sh

.PHONY: check
check:
	@find . -type f -name '*.sh' | xargs shellcheck
	@python3 -m py_compile upgrade.py && rm -rf __pycache__
