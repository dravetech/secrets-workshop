HUGO=docker run -p 1313:1313 --rm -v $(PWD):/site hugo:0.61.0
HUGO_OPTS=--source /site/src --destination /site/html
HUGO_TEST_OPTS=-D -E -F

ifneq ($(BIND), )
HUGO_OPTS:=$(HUGO_OPTS) --bind $(BIND)
endif

.PHONY: init
init:
	$(HUGO) new site /site/src

.PHONY: serve
serve:
	$(HUGO) serve \
		$(HUGO_TEST_OPTS) \
		$(HUGO_OPTS)

.PHONY: gen
gen:
	$(HUGO) \
		$(HUGO_OPTS)
