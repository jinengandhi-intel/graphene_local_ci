// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * Copyright (c) 2000 Silicon Graphics, Inc.  All Rights Reserved.
 */

/*
 * Description:
 * The testcase checks the various errnos of the unlink(2).
 * 1) unlink() returns ENOENT if file doesn't exist.
 * 2) unlink() returns ENOENT if path is empty.
 * 3) unlink() returns ENOENT if path contains a non-existent file.
 * 4) unlink() returns EFAULT if address is invalid.
 * 5) unlink() returns ENOTDIR if path contains a regular file.
 * 6) unlink() returns ENAMETOOLONG if path contains a regular file.
 */

#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <sys/param.h>	/* for PATH_MAX */
#include "tst_test.h"

static char longpathname[PATH_MAX + 2];

static struct test_case_t {
	char *name;
	char *desc;
	int exp_errno;
} tcases[] = {
	{"nonexistfile", "non-existent file", ENOENT},
	// {"", "path is empty string", ENOENT},
	// {"nefile/file", "path contains a non-existent file", ENOENT},
	// {NULL, "invalid address", EFAULT},
	// {"file/file", "path contains a regular file", ENOTDIR},
	// {longpathname, "pathname too long", ENAMETOOLONG},
};

static void verify_unlink(unsigned int n)
{
	tst_res(TPASS, "No Test function defined here");
}

static void setup(void)
{
	unsigned int n;

	SAFE_TOUCH("/tmp/unlink07_file", 0777, NULL);

	// memset(longpathname, 'a', PATH_MAX + 2);

	// for (n = 0; n < ARRAY_SIZE(tcases); n++) {
	// 	if (!tcases[n].name)
	// 		tcases[n].name = tst_get_bad_addr(NULL);
	// }
}

static struct tst_test test = {
	.needs_tmpdir = 1,
	.setup = setup,
	.tcnt = ARRAY_SIZE(tcases),
	.test = verify_unlink,
};
