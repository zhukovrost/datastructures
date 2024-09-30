.PHONY: build/docs
build/docs:
	make -C docs html

.PHONY: build/diagram
build/diagram:
	pydeps datastructures --noshow
