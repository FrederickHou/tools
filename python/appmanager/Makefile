VERSION = 1.0
BUILLD_DATE=`date "+%Y-%m-%d %H:%M:%S"`

INTSALL_NAME = appmanager
INTSALL_DIR =  appmanager
TEMP_DIR = release/opt/${INTSALL_DIR}

all:
	make package
	make rpm
package:
	sed -i "s#__BUILD_DATE__#${BUILLD_DATE}#g" src/main.py
	sed -i "s#__BUILD_VERSION__#${VERSION}#g" src/main.py
	# cxfreeze ./src/main.py --target-dir="./src/build" \
	#                        --target-name=${INTSALL_NAME} \
	#                        --include-modules=flask,subprocess,sys,os
	pyinstaller -F ./src/main.py -n ${INTSALL_NAME}
	if [ ! -d "${TEMP_DIR}" ]; then \
		mkdir -p ${TEMP_DIR}; \
	fi
	mv ./dist/${INTSALL_NAME} ${TEMP_DIR}
	# mv ./src/build/* ${TEMP_DIR}
	cp -rf script ${TEMP_DIR}

rpm:
	fpm -s dir -t rpm -v ${VERSION} -n ${INTSALL_NAME} --vendor "guest" --description "guest" --pre-install ${TEMP_DIR}/script/pre_install_centos.sh --post-install ${TEMP_DIR}/script/install_centos.sh --before-remove ${TEMP_DIR}/script/pre_uninstall_centos.sh -C ./release
	rm -rf ./release

deb:
	fpm -s dir -t deb -v ${VERSION} -n ${INTSALL_NAME} --vendor "guest" --description "guest" --pre-install ${TEMP_DIR}/script/pre_install_centos.sh --post-install ${TEMP_DIR}/script/install_centos.sh --before-remove ${TEMP_DIR}/script/pre_uninstall_centos.sh -C ./release
	rm -rf ./release

clean:
	sed -i "s#__BUILD_DATE__#${BUILLD_DATE}#g" src/main.py
	sed -i "s#__BUILD_VERSION__#${VERSION}#g" src/main.py
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./src/build
	rm ./src/*.pyc





