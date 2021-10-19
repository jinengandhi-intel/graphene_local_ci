#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2008 FUJITSU LIMITED
# Copyright (c) 2021 Joerg Vehlow <joerg.vehlow@aox-tech.de>
# Copyright (c) 2021 Petr Vorel <pvorel@suse.cz>
#
# Author: Li Zefan <lizf@cn.fujitsu.com>
#
# Process event connector is a netlink connector that reports process events
# to userspace. It sends events such as fork, exec, id change and exit.

TST_OPTS="n:"
TST_SETUP=setup
TST_TESTFUNC=test
TST_PARSE_ARGS=parse_args
TST_USAGE=usage
TST_NEEDS_ROOT=1
TST_NEEDS_TMPDIR=1
TST_NEEDS_CHECKPOINTS=1
TST_TEST_DATA="fork exec exit uid gid"

. tst_test.sh

num_events=10

LISTENER_ID=0
GENERATOR_ID=1

usage()
{
	cat << EOF
usage: $0 [-n <nevents>]

OPTIONS
-n      The number of evetns to generate per test (default 10)
EOF
}

parse_args()
{
	case $1 in
	n) num_events=$2;;
	esac
}

# Find a free file handle
free_fd()
{
	local fd

	for fd in $(seq 200); do
		# Sapwn a new sh, because redirecting to a non existing file handle
		# will trigger a syntax error.
		sh -c ": 2>/dev/null >&$fd || : 2>/dev/null <&$fd" 2>/dev/null
		if [ $? -ne 0 ]; then
			echo $fd
			return
		fi
	done
}

setup()
{
	if ! grep -q cn_proc /proc/net/connector; then
		tst_brk TCONF "Process Event Connector is not supported or kernel < 2.6.26"
	fi

	tst_res TINFO "Test process events connector"
}

test()
{
	local event=$2
	local gen_pid list_pid gen_rc lis_rc
	local expected_events fd_act failed act_nevents exp act

	tst_res TINFO "Testing $2 event (nevents=$num_events)"

	event_generator -n $num_events -e $event -c $GENERATOR_ID >gen.log &
	gen_pid=$!

	pec_listener -p $gen_pid -c $LISTENER_ID >lis.log &
	lis_pid=$!

	TST_CHECKPOINT_WAIT $LISTENER_ID
	TST_CHECKPOINT_WAKE $GENERATOR_ID

	wait $gen_pid
	gen_rc=$?
	wait $lis_pid
	lis_rc=$?

	if [ $gen_rc -ne 0 ]; then
		tst_brk TBROK "failed to execute event_generator"
	fi

	if [ $lis_rc -ne 0 ]; then
		tst_brk TBROK "failed to execute pec_listener"
	fi

	# The listener writes the same messages as the generator, but it can
	# also see more events (e.g. for testing exit, a fork is generated).
	# So: The events generated by the generator have to be in the same order
	# as the events printed by the listener, but my interleaved with other
	# messages. To correctly compare them, we have to open both logs
	# and iterate over both of them at the same time, skipping messages
	# in the listener log, that are not of interest.
	# Because some messages may be multiple times in the listener log,
	# we have to open it only once!
	# This however does not check, if the listener sees more messages,
	# than expected.

	fd_act=$(free_fd)
	[ -z "$fd_act" ] && tst_brk TBROK "No free filehandle found"
	eval "exec ${fd_act}<lis.log"

	failed=0
	act_nevents=0
	while read -r exp; do
		local found=0
		act_nevents=$((act_nevents + 1))
		while read -r act; do
			if [ "$exp" = "$act" ]; then
				found=1
				break
			fi
		done <&${fd_act}
		if [ $found -ne 1 ]; then
			failed=1
			tst_res TFAIL "Event was not detected by the event listener: $exp"
			break
		fi
	done <gen.log

	eval "exec ${fd_act}<&-"

	if [ $failed -eq 0 ]; then
		if [ $act_nevents -ne $num_events ]; then
			tst_res TBROK "Expected $num_events, but $act_nevents generated"
		else
			tst_res TPASS "All events detected"
		fi
	else
		# TFAIL message is already printed in the loop above
		cat lis.log
	fi
}

tst_run
