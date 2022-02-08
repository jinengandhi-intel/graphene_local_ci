#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) International Business Machines  Corp., 2005
# Copyright (c) 2021 Joerg Vehlow <joerg.vehlow@aox-tech.de>
# Author: Avantika Mathur (mathurav@us.ibm.com)

FS_BIND_TESTFUNC=test

. fs_bind_lib.sh

test()
{
	tst_res TINFO "move: uncloneable subtree to private parent"

	fs_bind_makedir runbindable dir
	fs_bind_makedir private parent2
	fs_bind_makedir rshared share2

	mkdir dir/grandchild
	mkdir parent2/child2
	EXPECT_PASS mount --move dir parent2/child2

	EXPECT_PASS mount --bind parent2 share2
	fs_bind_check  -n parent2/child2/ share2/child2/

	EXPECT_PASS umount share2
	EXPECT_PASS umount parent2/child2
	EXPECT_PASS umount share2
	EXPECT_PASS umount parent2
}

tst_run
