#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) International Business Machines  Corp., 2005
# Copyright (c) 2021 Joerg Vehlow <joerg.vehlow@aox-tech.de>
# Author: Avantika Mathur (mathurav@us.ibm.com)

FS_BIND_TESTFUNC=test

. fs_bind_lib.sh

test()
{
	tst_res TINFO "bind: private child to shared parent"

	fs_bind_makedir rshared parent1
	fs_bind_makedir rshared parent2
	fs_bind_makedir rshared share1
	fs_bind_makedir rshared share2
	fs_bind_makedir private parent1/child1

	EXPECT_PASS mount --bind parent1 share1
	EXPECT_PASS mount --bind "$FS_BIND_DISK1" parent1/child1
	EXPECT_PASS mount --bind parent2 share2

	fs_bind_check -n parent1/child1 share1/child1

	mkdir parent2/child2

	EXPECT_PASS mount --bind parent1/child1 parent2/child2
	fs_bind_check parent1/child1 parent2/child2 share2/child2

	EXPECT_PASS mount --bind "$FS_BIND_DISK2" parent1/child1/a
	fs_bind_check -n parent1/child1/a parent2/child2/a

	EXPECT_PASS mount --bind "$FS_BIND_DISK3" parent2/child2/b
	fs_bind_check -n parent1/child1/b parent2/child2/b
	fs_bind_check parent2/child2/b share2/child2/b

	EXPECT_PASS mount --bind "$FS_BIND_DISK4" share2/child2/c
	fs_bind_check -n parent1/child1/b parent2/child2/b
	fs_bind_check parent2/child2/c share2/child2/c

	EXPECT_PASS umount parent1/child1/a
	EXPECT_PASS umount parent2/child2/b
	EXPECT_PASS umount share2/child2/c
	EXPECT_PASS umount parent2/child2
	EXPECT_PASS umount parent1/child1
	EXPECT_PASS umount parent1/child1
	EXPECT_PASS umount share1
	EXPECT_PASS umount share1
	EXPECT_PASS umount share2
	EXPECT_PASS umount share2
	EXPECT_PASS umount parent2
	EXPECT_PASS umount parent1
}

tst_run
