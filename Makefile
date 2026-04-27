.PHONY: all
all:
	@$(MAKE) debian-base
	@$(MAKE) -j2 debian claude

.PHONY: debian-base
debian-base:
	@cd ./debian/forky && ./build.sh

.PHONY: debian-all
debian-all:
	@$(MAKE) debian-base
	@$(MAKE) debian

.PHONY: debian
debian:
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
