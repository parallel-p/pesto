### BEGIN ejudge auto-generated makefile ###
EJUDGE_PREFIX_DIR ?= /usr
EJUDGE_CONTESTS_HOME_DIR ?= /var/lib/ejudge
EJUDGE_LOCAL_DIR ?= /var/lib/ejudge/tmp
EJUDGE_SERVER_BIN_PATH ?= /usr/lib/ejudge/bin

EXECUTE = ${EJUDGE_PREFIX_DIR}/bin/ejudge-execute
EXECUTE_FLAGS =  --use-stdin --use-stdout --test-pattern=%03d.dat --corr-pattern=%03d.ans

NORMALIZE = ${EJUDGE_SERVER_BIN_PATH}/ej-normalize
NORMALIZE_FLAGS = --workdir=tests --test-pattern=%03d.dat --corr-pattern=%03d.ans

all :
check_settings : all normalize



normalize :
	${NORMALIZE} ${NORMALIZE_FLAGS} --all-tests

clean :
	-rm -f *.o *.class *.exe *~ *.bak

### END ejudge auto-generated makefile ###
