#! /bin/sh

#set -e

BASE_DIR="$PWD/`dirname $0`"

DEBUG=${DEBUG-0}
CONFIG_DIR="$BASE_DIR/nodes" # should be absolute
LINK_TARGET="$BASE_DIR/nodes/using.json"

errecho() {
    echo "$@" >&2
}

usage() {
    errecho "command:"
    errecho "    $0 start [NODE]"
    errecho "    $0 restart|stop|status(stat)|list(ls)|test"
    exit -1
}

checknode() {
    CONFIG=$CONFIG_DIR/$1.json
    test "$DEBUG" != "0" && echo $CONFIG
    if ! test -f $CONFIG
    then
        errecho "node [$1] not exists"
        exit -1
    fi
}

createlink() {
    # $1: node name
    linksrc=$CONFIG_DIR/$1.json
    rm $LINK_TARGET
    ln -s $linksrc $LINK_TARGET
}

linkinfo() {
    if ! test -e $LINK_TARGET
    then
        errecho "$LINK_TARGET not existed"
        exit -1
    fi
    if ! test -L $LINK_TARGET
    then
        errecho "$LINK_TARGET existed but not a symbiolic link"
        exit -1
    fi
    echo 'current: '`readlink $LINK_TARGET`
}

if test $# -lt 1
then
    usage $@
fi

case "$1" in
    start)
        if test $# -gt 2
        then
            usage $@
        fi

        checknode $2
        createlink $2
        systemctl restart myv2ray
        ;;
    stop)
        if test $# -gt 1
        then
            usage $@
        fi

        systemctl stop myv2ray
        ;;
    restart)
        if test $# -gt 1
        then
            usage $@
        fi

        systemctl restart myv2ray
        ;;
    stat|status)
        if test $# -gt 1
        then
            usage $@
        fi

        linkinfo
        echo '---systemctl status myv2ray---'
        systemctl status myv2ray
        ;;
    ls|list)
        ls $CONFIG_DIR | grep .json | sed -e 's/.json//'
        ;;
    test)
        linkinfo
        echo 'curl -x socks5h://localhost:1080 https://google.com'
        curl -x socks5h://localhost:1080 https://google.com
        ;;
    *)
        usage $@
        ;;
esac
