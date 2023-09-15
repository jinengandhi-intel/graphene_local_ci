// SPDX-License-Identifier: GPL-2.0-or-later
/*
 *   Copyright (c) International Business Machines  Corp., 2001
 *		07/2001 Ported by Wayne Boyer
 *   Copyright (c) 2022 SUSE LLC Avinesh Kumar <avinesh.kumar@suse.com>
 */

/*\
 * [Description]
 *
 * Verify that rename() does nothing and returns a success status when
 * oldpath and newpath are existing hard links referring to the same file.
 */

#include <stdio.h>
#include "tst_test.h"

#define TEMP_FILE1 "/tmp/tmpfile1"
#define TEMP_FILE2 "/tmp/tmpfile2"
static struct stat buf1, buf2;

static void setup(void)
{
	SAFE_TOUCH(TEMP_FILE1, 0700, NULL);
}

static void run(void)
{
	
}

static struct tst_test test = {
	.setup = setup,
	.test_all = run,
	.needs_root = 1,
	.all_filesystems = 1,
	.skip_filesystems = (const char *const[]){
		"exfat",
		"vfat",
		NULL
	},
};
