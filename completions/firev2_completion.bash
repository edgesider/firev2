__firev2_completion()
{
    if [[ "${COMP_CWORD}" -eq "1" ]]
    then
        curr=${COMP_WORDS[1]}
        if [[ "$curr" == -* ]]
        then
            COMPREPLY=($(compgen -W "-h --help --config" -- $curr))
        else
            COMPREPLY=($(compgen -W "subscript start restart stop status list" -- $curr))
        fi
    elif [[ "${COMP_CWORD}" -eq "2" ]]
    then
        cmd=${COMP_WORDS[1]}
        curr=${COMP_WORDS[2]}
        case "$cmd" in
            subscript)
                if [[ "$curr" == -* ]]
                then
                    COMPREPLY=($(compgen -W "-h --help --template" -- $curr))
                else
                    COMPREPLY=($(compgen -W "vmess_str vmess_url" -- $curr))
                fi
                ;;
            start)
                if [[ "$curr" == -* ]]
                then
                    COMPREPLY=($(compgen -W "-h --help" -- $curr))
                else
                    IFS_BK=$IFS
                    IFS=$'\n'
                    COMPREPLY=($(compgen -W "`firev2 list`" -- $curr))
                    IFS=$IFS_BK
                fi
                ;;
            restart)
                ;;
            stop)
                ;;
            status)
                ;;
            list)
                ;;
        esac
    fi
}

complete -F __firev2_completion firev2
