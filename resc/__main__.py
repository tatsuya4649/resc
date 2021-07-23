from resc import Resc
import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description="Resouce Checker.")
	parser.add_argument("-c","--cpu_t",help="CPU threshold value",type=float)
	parser.add_argument("--cpu_mode",help="CPU mode",type=str)
	parser.add_argument("-i","--cpu_interval",help="Time to confirm CPU threshold",type=int)
	parser.add_argument("-m","--mem_t",help="Memory threshold value",type=float)
	parser.add_argument("--mem_mode",help="Memory mode",type=str)
	parser.add_argument("-d","--disk_t",help="Disk threshold value",type=float)
	parser.add_argument("-p","--disk_path",help="Disk path",type=str)
	parser.add_argument("--disk_mode",help="Disk mode",type=str)

	args = parser.parse_args()
	cpu = dict()
	memory = dict()
	disk = dict()
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
	if args.disk_t is not None and args.disk_path:
		disk["threshold"] = args.disk_t
		disk["path"] = args.disk_path
		if args.disk_mode is not None:
			disk["mode"] = args.disk_mode
	else:
		disk = None

	if cpu is None and memory is None and disk is None:
		print("CPU or Memory or Disk must be not empty.",file=sys.stderr)
		parser.print_help()
		sys.exit(1)
	resc = Resc(
		cpu=cpu,
		memory=memory,
		disk=disk,
	)
	print(resc._resc_arg)
	print(f"PATH=\"$PATH:~/.local/bin\" resc {resc._resc_arg}")
	if resc.over_one:
		print("over threshold.")
		sys.exit(255)
	else:
		print("no resource over threshold.")
		sys.exit(0)


if __name__ == "__main__":
	main()
