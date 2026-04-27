.PHONY: all
all:
	@$(MAKE) debian
	@$(MAKE) claude

.PHONY: debian
debian:
	@cd ./debian/forky && ./build.sh
	@cd ./debian/devel && ./build.sh

.PHONY: claude
claude:
	@cd ./claude && ./build.sh

.PHONY: check
check:
	@git ls-files | grep -F .sh | xargs shellcheck
	@python3 -m py_compile upgrade.py bin/claude.py \
		&& rm -rf __pycache__ bin/__pycache__

.PHONY: clean
clean:
	@rm -rf __pycache__ bin/__pycache__

.PHONY: prune
prune: clean
	@docker system prune --force
