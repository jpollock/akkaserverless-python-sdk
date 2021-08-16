# Make Akka Serverless Python documentation

module   := python
upstream := akkaserverlessio/python-support
branch   := docs/current
sources  := src build/src/managed

akkaserverless_antora_download := https://github.com/akkaserverlessio/akkaserverless-antora/raw/master/akkaserverless-antora
akkaserverless_antora := .cache/bin/akkaserverless-antora
descriptor := build/site.yml
src_managed := build/src/managed
managed_partials := ${src_managed}/modules/python/partials

.SILENT:

build: clean managed validate html

${akkaserverless_antora}:
	mkdir -p $$(dirname ${akkaserverless_antora})
	curl -Lo ${akkaserverless_antora} ${akkaserverless_antora_download}
	chmod +x ${akkaserverless_antora}

clean-cache:
	rm -rf .cache

update: clean-cache ${akkaserverless_antora}

clean: ${akkaserverless_antora}
	${akkaserverless_antora} clean

managed: attributes
	mkdir -p "${src_managed}"
	cp src/antora.yml "${src_managed}/antora.yml"

attributes: ${akkaserverless_antora}
	mkdir -p "${managed_partials}"
	${akkaserverless_antora} version | xargs -0  printf ":akkaserverless-python-version: %s" \
		> "${managed_partials}/attributes.adoc"

${descriptor}: ${akkaserverless_antora}
	mkdir -p $$(dirname ${descriptor})
	${akkaserverless_antora} source --preview --upstream ${upstream} ${sources} > build/source.yml
	${akkaserverless_antora} site --preview --exclude ${module} build/source.yml > ${descriptor}

validate: ${descriptor}
	${akkaserverless_antora} validate ${descriptor}

html: ${descriptor}
	${akkaserverless_antora} build ${descriptor}

validate-links: ${akkaserverless_antora}
	${akkaserverless_antora} validate --no-xrefs --links

deploy: clean managed
	${akkaserverless_antora} deploy --module ${module} --upstream ${upstream} --branch ${branch} ${sources}
