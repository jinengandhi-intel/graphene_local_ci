#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) International Business Machines  Corp., 2005
# Copyright (c) 2021 Joerg Vehlow <joerg.vehlow@aox-tech.de>
# Author: Avantika Mathur (mathurav@us.ibm.com)

FS_BIND_TESTFUNC=test

. fs_bind_lib.sh

test()
{
	tst_res TINFO "rbind: rbind within same tree - root to child, child is private "

	fs_bind_makedir rshared parent
	fs_bind_makedir private parent/child1
	fs_bind_makedir rshared parent/child2

	EXPECT_PASS mount --rbind "$FS_BIND_DISK3" parent/child1

	EXPECT_PASS mount --rbind parent parent/child2/
	fs_bind_check parent parent/child2/
	fs_bind_check parent/child1 parent/child2/child1

	EXPECT_PASS umount parent/child2/child1
	#added -n
	fs_bind_check -n parent/child1 parent/child2/child1

	EXPECT_PASS umount parent/child1
	fs_bind_check parent/child1 parent/child2/child1

	EXPECT_PASS mount --rbind "$FS_BIND_DISK4" parent/child2/child1
	fs_bind_check -n parent/child1 parent/child2/child1

	EXPECT_PASS umount parent/child2/child1
	fs_bind_check parent/child1 parent/child2/child1


	EXPECT_PASS umount parent/child2/child2
	EXPECT_PASS umount parent/child2/child1
	EXPECT_PASS umount parent/child2
	EXPECT_PASS umount parent/child2
	EXPECT_PASS umount parent
}

tst_run
