#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) International Business Machines  Corp., 2005
# Copyright (c) 2021 Joerg Vehlow <joerg.vehlow@aox-tech.de>
# Author: Avantika Mathur (mathurav@us.ibm.com)

FS_BIND_TESTFUNC=test

. fs_bind_lib.sh

test()
{
	tst_res TINFO "bind: uncloneable child to private parent"

	fs_bind_makedir rshared parent1
	fs_bind_makedir private parent2
	fs_bind_makedir rshared share1
	fs_bind_makedir runbindable parent1/child1
	mkdir parent1/child1/x

	EXPECT_PASS mount --bind parent1 share1
	EXPECT_PASS mount --bind "$FS_BIND_DISK1" parent1/child1/x
	mkdir parent2/child2
	EXPECT_FAIL mount --bind parent1/child1 parent2/child2

	EXPECT_PASS umount parent1/child1/x
	EXPECT_PASS umount parent1/child1
	EXPECT_PASS umount share1
	EXPECT_PASS umount share1
	EXPECT_PASS umount parent2
	EXPECT_PASS umount parent1
}

tst_run
