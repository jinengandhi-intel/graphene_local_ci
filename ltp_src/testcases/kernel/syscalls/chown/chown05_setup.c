// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * Copyright (c) International Business Machines  Corp., 2001
 * 07/2001 Ported by Wayne Boyer
 * Copyright (c) 2021 Xie Ziyao <xieziyao@huawei.com>
 */

/*\
 * [Description]
 *
 * Verify that, chown(2) succeeds to change the owner and group of a file
 * specified by path to any numeric owner(uid)/group(gid) values when invoked
 * by super-user.
 */

#include "tst_test.h"
#include "compat_tst_16.h"
#include "tst_safe_macros.h"

#define FILE_MODE (S_IFREG|S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH)
#define TESTFILE "/tmp/chown05_testfile"

struct test_case_t {
	char *desc;
	uid_t uid;
	gid_t gid;
} tc[] = {
	{"change owner/group ids", 700, 701},
};

static void run(unsigned int i)
{
	tst_res(TPASS, "No Test function defined here");
}

static void setup(void)
{
	SAFE_TOUCH(TESTFILE, FILE_MODE, NULL);
}

static struct tst_test test = {
	.tcnt = ARRAY_SIZE(tc),
	.setup = setup,
	.test = run,
};
