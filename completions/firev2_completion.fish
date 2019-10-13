complete -c v2 -x -a '(v2 list)' --condition '__fish_seen_subcommand_from start'
complete -c v2 -x -a start --condition '__fish_v2_no_subcommand'
complete -c v2 -x -a restart --condition '__fish_v2_no_subcommand'
complete -c v2 -x -a stop --condition '__fish_v2_no_subcommand'
complete -c v2 -x -a status --condition '__fish_v2_no_subcommand'
complete -c v2 -x -a list --condition '__fish_v2_no_subcommand'
complete -c v2 -x -a test --condition '__fish_v2_no_subcommand'

function __fish_v2_no_subcommand
    for i in (commandline -cop)
        if contains -- $i start status stop restart stat list ls test
            return 1
        end
    end
    return 0
end
