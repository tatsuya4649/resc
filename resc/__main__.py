import sys
import os
sys.path.append(os.path.dirname(__file__))

from resc import Resc, RescLog, RescLogAnalyze, \
    start_server, RescLogPathError, RescLogUnMatchError, RescJSON
import argparse
import re
import subprocess


def main():
    parser = argparse.ArgumentParser(description="Resouce Checker.")
    parser.add_argument(
        "-c",
        "--cpu_t",
        help="CPU threshold value",
        type=float
    )
    parser.add_argument(
        "--cpu_mode",
        help="CPU mode",
        type=str
    )
    parser.add_argument(
        "-i",
        "--cpu_interval",
        help="Time to confirm CPU threshold",
        type=int
    )
    parser.add_argument(
        "-m",
        "--mem_t",
        help="Memory threshold value",
        type=float
    )
    parser.add_argument(
        "--mem_mode",
        help="Memory mode",
        type=str
    )
    parser.add_argument(
        "-d",
        "--disk_t",
        help="Disk threshold value",
        type=float
    )
    parser.add_argument(
        "-p",
        "--disk_path",
        help="Disk path",
        type=str
    )
    parser.add_argument(
        "--disk_mode",
        help="Disk mode",
        type=str
    )
    parser.add_argument(
        "-n",
        "--net",
        help="Network Connections threshold",
        type=int,
    )
    parser.add_argument(
        "--net_kind",
        help="type of Network Connections",
        type=str,
    )
    parser.add_argument(
        "-s",
        "--ps",
        help="Process threshold value",
        type=float,
    )
    parser.add_argument(
        "--ps_mode",
        help="Process mode.(percent or number)",
        type=str,
    )
    parser.add_argument(
        "--ps_limits",
        help="Process Limits.(soft limits or hard limits.)",
        type=str,
    )
    parser.add_argument(
        "-f",
        "--file",
        help="File threshold value.",
        type=float,
    )
    parser.add_argument(
        "--file_mode",
        help="File mode value.",
        type=str,
    )
    parser.add_argument(
        "--log",
        help="Analize log file.receive path.",
        type=str
    )
    parser.add_argument(
        "--log_server",
        help="Analize log file on GUI.(Flag)",
        action="store_true"
    )
    parser.add_argument(
        "-q",
        help="Quiet output(Flag)",
        action="store_true"
    )
    parser.add_argument(
        "--all",
        help="All resouce exceeded mode(Flag)",
        action="store_true"
    )
    parser.add_argument(
        "--not_found",
        help="for crontab. If not found script, write to log",
        type=str,
    )
    parser.add_argument(
        "-r",
        "--registered",
        help="display list of now registered in Resc",
        action="store_true",
    )

    args = parser.parse_args()

    if args.log is not None:
        try:
            analyzer = RescLogAnalyze(path=args.log)
            log = analyzer.getlog()
            anares = analyzer.analyze(log)
            for ana in anares:
                print(ana)
            sys.exit(0)
        except RescLogPathError as e:
            print(e)
        except RescLogUnMatchError as e:
            print(e)
        except Exception as e:
            print(e)
        sys.exit(1)
    elif args.log_server:
        start_server()
        sys.exit(0)
    elif args.not_found is not None:
        RescLog._not_found(args.not_found)
        sys.exit(0)
    elif args.registered:
        RescJSON.display(Resc._RESCJSONPATH)
        sys.exit(0)

    cpu = dict()
    memory = dict()
    disk = dict()
    net = dict()
    ps = dict()
    file = dict()
    if args.cpu_t is not None:
        cpu["threshold"] = args.cpu_t
        if args.cpu_mode is not None:
            cpu["mode"] = args.cpu_mode
        if args.cpu_interval is not None:
            cpu["interval"] = args.cpu_interval
    else:
        cpu = None
    if args.mem_t is not None:
        memory["threshold"] = args.mem_t
        if args.mem_mode is not None:
            memory["mode"] = args.mem_mode
    else:
        memory = None
    if args.disk_t is not None and args.disk_path is not None:
        disk["threshold"] = args.disk_t
        disk["path"] = args.disk_path
        if args.disk_mode is not None:
            disk["mode"] = args.disk_mode
    else:
        disk = None
    if args.net is not None:
        net["threshold"] = args.net
        if args.net_kind is not None:
            net["kind"] = args.net_kind
    else:
        net = None
    if args.ps is not None:
        ps["threshold"] = args.ps
        if args.ps_mode is not None:
            ps["mode"] = args.ps_mode
        if args.ps_limits is not None:
            ps["limits"] = args.ps_limits
    else:
        ps = None
    if args.file is not None:
        file["threshold"] = args.file
        if args.file_mode is not None:
            file["mode"] = args.file_mode
    else:
        file = None

    if cpu is None and memory is None \
            and disk is None and net is None and ps is None \
            and file is None:
        print(
            "Resource must be not empty.",
            file=sys.stderr
        )
        parser.print_help()
        sys.exit(1)
    try:
        resc = Resc(
            cpu=cpu,
            memory=memory,
            disk=disk,
            net=net,
            ps=ps,
            file=file,
        )
        if args.all:
            resc.all = True
        else:
            resc.all = False
    except Exception as e:
        print(e)
        parser.print_help()
        sys.exit(1)
    if resc.over_one:
        if not args.q:
            print("exceed threshold.")
        sys.exit(255)
    else:
        if not args.q:
            print("no exceed threshold.")
        sys.exit(0)


if __name__ == "__main__":
    main()
