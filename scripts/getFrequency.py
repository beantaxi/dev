import argparse

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('arg')
	args = ap.parse_args()
	print(args.arg)
	# Get the latest report for this arg
	# Analyze the timestamps and figure something out
