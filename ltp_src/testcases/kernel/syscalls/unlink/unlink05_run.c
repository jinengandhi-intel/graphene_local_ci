// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * Copyright (c) 2000 Silicon Graphics, Inc.  All Rights Reserved.
 */

/*
 * Description:
 * The testcase checks the basic functionality of the unlink(2).
 * 1) unlink() can delete regular file successfully.
 * 2) unlink() can delete fifo file successfully.
 */

#include <errno.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include "tst_test.h"

static void file_create(char *);
static void fifo_create(char *);

#define C_FILE "/tmp/unlink05_file"
#define C_FIFO "/tmp/unlink05_fifo"

static struct test_case_t {
	void (*setupfunc)(char *);
	char *desc;
} tcases[] = {
	{file_create, C_FILE},
	{fifo_create, C_FIFO},
};

static void file_create(char *name)
{
	SAFE_TOUCH(name, 0777, NULL);
}

static void fifo_create(char *name)
{
	SAFE_MKFIFO(name, 0777);
}

static void verify_unlink(unsigned int n)
{
	struct test_case_t *tc = &tcases[n];

	TEST(unlink(tc->desc));
	if (TST_RET == -1) {
		tst_res(TFAIL | TTERRNO, "unlink(%s) failed", tc->desc);
		return;
	}

	if (!access(tc->desc, F_OK)) {
		tst_res(TFAIL, "unlink(%s) succeeded, but %s still existed",
			tc->desc, tc->desc);
		return;
	}

	tst_res(TPASS, "unlink(%s) succeeded", tc->desc);
}

static struct tst_test test = {
	.needs_tmpdir = 1,
	.tcnt = ARRAY_SIZE(tcases),
	.test = verify_unlink,
};
