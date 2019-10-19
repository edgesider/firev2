#! /usr/bin/env python3
import sys
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument(
            '--config', help='specify configuration file')
    subparsers = parser.add_subparsers(
            required=True, dest='command')

    sub_subscript = subparsers.add_parser(
            'subscript', help='get a subscription')
    sub_subscript.add_argument(
            'type', help='subscription type')
    sub_subscript.add_argument(
            'url', help='subscription url')
    sub_subscript.add_argument(
            '--template', help='select a template (default: proxy_multi.json)',
            default='proxy_multi.json')

    sub_start = subparsers.add_parser(
            'start', help='start a node')
    sub_start.add_argument(
            '-i', '--interactive',
            action='store_true',
            help='select node interactively')
    sub_start.add_argument(
            'node', nargs='?', help='node name')

    sub_stop = subparsers.add_parser(
            'stop', help='stop using node')
    sub_restart = subparsers.add_parser(
            'restart', help='restart using node')
    sub_list = subparsers.add_parser(
            'list', help='list all nodes')
    sub_status = subparsers.add_parser(
            'status', help='check current status')

    args = parser.parse_args(sys.argv[1:])

    import config

    if args.config is not None:
        config.load_from_file(args.config)
    else:
        config.auto_load()

    import subscript
    import node_mgr

    command = args.command
    if command == 'subscript':
        subscript.process(args.type, args.url, args.template)
    elif command == 'start':
        node_mgr.process_start(args.node, args.interactive)
    elif command == 'stop':
        node_mgr.process_stop()
    elif command == 'restart':
        node_mgr.process_restart()
    elif command == 'status':
        node_mgr.process_status()
    elif command == 'list':
        node_mgr.process_list()
