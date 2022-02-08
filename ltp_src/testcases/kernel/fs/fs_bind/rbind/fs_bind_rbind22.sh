#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) International Business Machines  Corp., 2005
# Copyright (c) 2021 Joerg Vehlow <joerg.vehlow@aox-tech.de>
# Author: Avantika Mathur (mathurav@us.ibm.com)

FS_BIND_TESTFUNC=test

. fs_bind_lib.sh

test()
{
	tst_res TINFO "rbind: shared subtree with  private child to slave subtree"

	fs_bind_makedir rshared parent1
	fs_bind_makedir rshared parent2
	fs_bind_makedir rshared share2

	EXPECT_PASS mount --rbind share2 parent2
	EXPECT_PASS mount --make-rslave parent2
	fs_bind_makedir private parent1/child1
	EXPECT_PASS mount --rbind "$FS_BIND_DISK1" parent1/child1
	EXPECT_PASS mount --rbind parent1 parent2

	fs_bind_check parent1 parent2
	fs_bind_check parent1/child1/ parent2/child1
	fs_bind_check -n parent2 share2
	EXPECT_PASS mount --rbind "$FS_BIND_DISK2" parent1/child1/a

	fs_bind_check -n parent1/child1/a parent2/child1/a

	EXPECT_PASS mount --rbind "$FS_BIND_DISK3" parent2/child1/b

	fs_bind_check -n parent1/child1/b parent2/child1/b


	EXPECT_PASS umount parent1/child1/a
	EXPECT_PASS umount parent2/child1/b
	EXPECT_PASS umount parent2/child1
	EXPECT_PASS umount parent2/child1
	EXPECT_PASS umount parent1/child1
	EXPECT_PASS umount parent2
	EXPECT_PASS umount parent2
	EXPECT_PASS umount parent1
	EXPECT_PASS umount share2
	EXPECT_PASS umount parent2
}

tst_run
