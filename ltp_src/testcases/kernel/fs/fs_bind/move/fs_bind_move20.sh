#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) International Business Machines  Corp., 2005
# Copyright (c) 2021 Joerg Vehlow <joerg.vehlow@aox-tech.de>
# Author: Avantika Mathur (mathurav@us.ibm.com)

FS_BIND_TESTFUNC=test

. fs_bind_lib.sh

test()
{
	tst_res TINFO "move: private to private - with unclonable children"

	fs_bind_makedir private parent1
	fs_bind_makedir private parent2
	fs_bind_makedir runbindable parent1/child1

	EXPECT_PASS mount --bind "$FS_BIND_DISK1" parent1/child1

	EXPECT_PASS mount --move parent1 parent2

	fs_bind_check "$FS_BIND_DISK1" parent2/child1

	EXPECT_PASS umount parent2/child1
	EXPECT_PASS umount parent2/child1
	EXPECT_PASS umount parent2
	EXPECT_PASS umount parent2
}

tst_run
