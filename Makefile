.PHONY: default
default:

.PHONY: check
check:
	@find . -type f -name '*.sh' | xargs shellcheck
