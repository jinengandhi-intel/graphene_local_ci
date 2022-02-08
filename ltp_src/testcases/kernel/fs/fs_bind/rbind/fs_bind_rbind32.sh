#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) International Business Machines  Corp., 2005
# Copyright (c) 2021 Joerg Vehlow <joerg.vehlow@aox-tech.de>
# Author: Avantika Mathur (mathurav@us.ibm.com)

FS_BIND_TESTFUNC=test

. fs_bind_lib.sh

test()
{
	tst_res TINFO "rbind: shared subtree with uncloneable child to uncloneable subtree"

	fs_bind_makedir rshared parent1
	fs_bind_makedir runbindable parent2
	fs_bind_makedir rshared share1

	EXPECT_PASS mount --rbind share1 parent1

	fs_bind_makedir runbindable parent1/child1
	EXPECT_PASS mount --rbind "$FS_BIND_DISK1" parent1/child1
	EXPECT_PASS mount --rbind parent1 parent2

	fs_bind_check -n parent1/child1 share1/child1
	fs_bind_check -n parent1/child1 parent2/child1


	EXPECT_PASS umount parent1/child1
	EXPECT_PASS umount parent1/child1
	EXPECT_PASS umount parent2
	EXPECT_PASS umount parent2
	EXPECT_PASS umount parent1
	EXPECT_PASS umount share1
	EXPECT_PASS umount parent1
}

tst_run
