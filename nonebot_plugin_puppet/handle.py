from time import strftime, localtime
from argparse import Namespace as ArgNamespace

from .data import *


class Namespace(ArgNamespace):
    pass


def handle_link(args: Namespace) -> Namespace:

    user_id_a = args.user_a if hasattr(args, "user_a") else []
    group_id_a = args.group_a if hasattr(args, "group_a") else []
    if not user_id_a and not group_id_a:
        if args.user_id:
            user_id_a.append(args.user_id)
        if args.group_id:
            group_id_a.append(args.group_id)

    user_id_b = args.user_b if hasattr(args, "user_b") else []
    group_id_b = args.group_b if hasattr(args, "group_b") else []

    link_conv(user_id_a, group_id_a, user_id_b, group_id_b)

    args.message = "会话链接成功！"
    args.recv_args = [[args.user_id, args.group_id, args.message]]
    return args


def handle_unlink(args: Namespace) -> Namespace:

    user_id_a = args.user_a if hasattr(args, "user_a") else []
    group_id_a = args.group_a if hasattr(args, "group_a") else []
    if not user_id_a and not group_id_a:
        if args.user_id:
            user_id_a.append(args.user_id)
        if args.group_id:
            group_id_a.append(args.group_id)

    user_id_b = args.user_b if hasattr(args, "user_b") else []
    group_id_b = args.group_b if hasattr(args, "group_b") else []

    unlink_conv(user_id_a, group_id_a, user_id_b, group_id_b)

    args.message = "链接解除成功！"
    args.recv_args = [[args.user_id, args.group_id, args.message]]
    return args


def handle_clear(args: Namespace):
    pass


def handle_list(args: Namespace):

    user_id = args.user if args.user else []
    group_id = args.group if args.group else []

    if not user_id and not group_id:
        if args.user_id:
            user_id.append(args.user_id)
        if args.group_id:
            group_id.append(args.group_id)

    conv_mapping = get_conv_mapping(user_id, group_id)

    args.message = "本群链接列表如下："
    print(conv_mapping)
    for type_a in conv_mapping:
        for id_a in conv_mapping[type_a]:
            for type_b in conv_mapping[type_a][id_a]:
                args.message += f"\n {type_b}: "
                for id_b in conv_mapping[type_a][id_a][type_b]:
                    args.message += f"\n {id_b}"
    args.recv_args = [[args.user_id, args.group_id, args.message]]
    return args


def handle_send(args: Namespace) -> Namespace:

    conv_mapping = [["user", id] for id in args.user] + [
        ["group", id] for id in args.group
    ]

    for type, id in conv_mapping:
        args.recv_args.append(
            [
                id if type == "user" else None,
                id if type == "group" else None,
                f"{args.message}",
            ]
        )

    return args


def handle_transmit(args: Namespace) -> Namespace:
    conv_mapping = get_conv_mapping(args.user_id, args.group_id)

    args.recv_args = []

    args.sender = f"{args.name} {strftime('%Y-%m-%d %H:%M:%S',localtime(args.time))} \n"

    if not args.is_superuser:
        args.message = args.conv + args.sender + args.message

    for type in conv_mapping:
        for id in conv_mapping[type]:
            args.recv_args.append(
                [
                    id if type == "user" else None,
                    id if type == "group" else None,
                    f"{args.message}",
                ]
            )

    return args
