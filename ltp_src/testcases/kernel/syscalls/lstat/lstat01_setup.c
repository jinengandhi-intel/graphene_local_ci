// SPDX-License-Identifier: GPL-2.0
/*
 * Copyright (c) 2000 Silicon Graphics, Inc.  All Rights Reserved.
 *  Authors:	William Roske, Dave Fenner
 *
 *  06/2019 Ported to new library:
 *		Christian Amann <camann@suse.com>
 */
/*
 * Basic test for lstat():
 *
 * Tests if lstat() writes correct information about a symlink
 * into the stat structure.
 */

#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include "tst_test.h"

#define TESTFILE        "/tmp/tst_file"
#define TESTSYML        "/tmp/tst_syml"

static uid_t user_id;
static gid_t group_id;

static void run(void)
{
	tst_res(TPASS, "No test function defined here");
}

static void setup(void)
{
	user_id  = getuid();
	group_id = getgid();

	SAFE_TOUCH(TESTFILE, 0644, NULL);
	SAFE_SYMLINK(TESTFILE, TESTSYML);
}

static void cleanup(void)
{}

static struct tst_test test = {
	.test_all = run,
	.setup = setup,
	.needs_tmpdir = 1,
};
