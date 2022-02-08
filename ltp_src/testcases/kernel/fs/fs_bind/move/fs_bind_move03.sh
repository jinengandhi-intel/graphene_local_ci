#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) International Business Machines  Corp., 2005
# Copyright (c) 2021 Joerg Vehlow <joerg.vehlow@aox-tech.de>
# Author: Avantika Mathur (mathurav@us.ibm.com)

FS_BIND_TESTFUNC=test

. fs_bind_lib.sh

test()
{
	tst_res TINFO "move: shared subtree to slave parent"

	fs_bind_makedir rshared dir
	fs_bind_makedir rshared parent2
	fs_bind_makedir rshared share1
	fs_bind_makedir rshared share2

	EXPECT_PASS mount --bind dir share1
	EXPECT_PASS mount --bind share2 parent2
	mkdir dir/grandchild
	mkdir parent2/child2
	EXPECT_PASS mount --make-rslave parent2

	EXPECT_PASS mount --move dir parent2/child2

	EXPECT_PASS mount --bind "$FS_BIND_DISK1" parent2/child2/grandchild
	fs_bind_check parent2/child2/grandchild share1/grandchild
	fs_bind_check -n dir/grandchild parent2/child2/grandchild
	fs_bind_check -n share2/child2 parent2/child2

	EXPECT_PASS mount --bind "$FS_BIND_DISK2" share1/grandchild/a

	fs_bind_check parent2/child2/grandchild/a share1/grandchild/a

	EXPECT_PASS umount share1/grandchild/a
	EXPECT_PASS umount parent2/child2/grandchild
	EXPECT_PASS umount parent2/child2
	EXPECT_PASS umount parent2
	EXPECT_PASS umount share1
	EXPECT_PASS umount share2
	EXPECT_PASS umount share1
	EXPECT_PASS umount parent2
}

tst_run
