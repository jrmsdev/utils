.PHONY: all
all:
	cd ./claude && ./build.sh

.PHONY: check
check:
	@find . -type f -name '*.sh' | xargs shellcheck
