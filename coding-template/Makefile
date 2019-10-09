VERSION = 1.0
BUILLD_DATE=`date "+%Y-%m-%d %H:%M:%S"`

INTSALL_NAME = coding-template
INTSALL_DIR =  coding_template
TEMP_DIR = release/opt/test/${INTSALL_DIR}

all:
	make package
	make rpm
package:
	sed -i "s#__BUILD_DATE__#${BUILLD_DATE}#g" src/main.py
	sed -i "s#__BUILD_VERSION__#${VERSION}#g" src/main.py
	cxfreeze ./src/main.py --target-dir="./src/build" \
	                       --target-name=${INTSALL_NAME} \
	                       --include-modules=os,logging,sys,json,time,argparse,requests,base64,datetime
	if [ ! -d "${TEMP_DIR}" ]; then \
		mkdir -p ${TEMP_DIR}; \
	fi
	mv ./src/build/* ${TEMP_DIR}
	# cp ./src/*.py ${TEMP_DIR}
	cp -rf conf/* ${TEMP_DIR}
	cp -rf script ${TEMP_DIR}

rpm:
	fpm -s dir -t rpm -v ${VERSION} -n ${INTSALL_NAME} --vendor "test" --description "test" --pre-install ${TEMP_DIR}/script/pre_install_centos.sh --post-install ${TEMP_DIR}/script/install_centos.sh --before-remove ${TEMP_DIR}/script/pre_uninstall_centos.sh -C ./release
	rm -rf ./release

deb:
	fpm -s dir -t deb -v ${VERSION} -n ${INTSALL_NAME} --vendor "test" --description "test" --pre-install ${TEMP_DIR}/script/pre_install_centos.sh --post-install ${TEMP_DIR}/script/install_centos.sh --before-remove ${TEMP_DIR}/script/pre_uninstall_centos.sh -C ./release
	rm -rf ./release

clean:
	sed -i "s#__BUILD_DATE__#${BUILLD_DATE}#g" src/main.py
	sed -i "s#__BUILD_VERSION__#${VERSION}#g" src/main.py
	rm -rf ./src/log
	rm -rf ./release
	rm -rf ./src/build
	rm ./src/*.pyc




