// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * Copyright (c) 2000 Silicon Graphics, Inc.  All Rights Reserved.
 *   AUTHOR		: William Roske
 */
/*
 * Basic test for access(2) using F_OK, R_OK, W_OK and X_OK
 */
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>
#include "tst_test.h"

#define FNAME_RWX "/tmp/accessfile_rwx"
#define FNAME_R   "/tmp/accessfile_r"
#define FNAME_W   "/tmp/accessfile_w"
#define FNAME_X   "/tmp/accessfile_x"

#define DFNAME_RWX "accessfile_rwx"
#define DFNAME_R   "accessfile_r"
#define DFNAME_W   "accessfile_w"
#define DFNAME_X   "accessfile_x"

#define DNAME_R   "/tmp/accessdir_r"
#define DNAME_W   "/tmp/accessdir_w"
#define DNAME_X   "/tmp/accessdir_x"
#define DNAME_RW  "/tmp/accessdir_rw"
#define DNAME_RX  "/tmp/accessdir_rx"
#define DNAME_WX  "/tmp/accessdir_wx"

static uid_t uid;

static struct tcase {
	const char *fname;
	int mode;
	char *name;
	int exp_errno;
	/* 1: nobody expected  2: root expected 3: both */
	int exp_user;
} tcases[] = {
	{FNAME_RWX, F_OK, "F_OK", 0, 3},
};

static void verify_access(unsigned int n)
{
    tst_res(TPASS, "No test function defined");
}

static void setup(void)
{
	struct passwd *pw;

	umask(0022);

	pw = SAFE_GETPWNAM("nobody");

	uid = pw->pw_uid;

	SAFE_TOUCH(FNAME_RWX, 0777, NULL);
	SAFE_TOUCH(FNAME_R, 0444, NULL);
	SAFE_TOUCH(FNAME_W, 0222, NULL);
	SAFE_TOUCH(FNAME_X, 0111, NULL);

	SAFE_MKDIR(DNAME_R, 0444);
	SAFE_MKDIR(DNAME_W, 0222);
	SAFE_MKDIR(DNAME_X, 0111);
	SAFE_MKDIR(DNAME_RW, 0666);
	SAFE_MKDIR(DNAME_RX, 0555);
	SAFE_MKDIR(DNAME_WX, 0333);

	SAFE_TOUCH(DNAME_R"/"DFNAME_R, 0444, NULL);
	SAFE_TOUCH(DNAME_R"/"DFNAME_W, 0222, NULL);
	SAFE_TOUCH(DNAME_R"/"DFNAME_X, 0111, NULL);

	SAFE_TOUCH(DNAME_W"/"DFNAME_R, 0444, NULL);
	SAFE_TOUCH(DNAME_W"/"DFNAME_W, 0222, NULL);
	SAFE_TOUCH(DNAME_W"/"DFNAME_X, 0111, NULL);

	SAFE_TOUCH(DNAME_X"/"DFNAME_R, 0444, NULL);
	SAFE_TOUCH(DNAME_X"/"DFNAME_W, 0222, NULL);
	SAFE_TOUCH(DNAME_X"/"DFNAME_X, 0111, NULL);

	SAFE_TOUCH(DNAME_RW"/"DFNAME_R, 0444, NULL);
	SAFE_TOUCH(DNAME_RW"/"DFNAME_W, 0222, NULL);
	SAFE_TOUCH(DNAME_RW"/"DFNAME_X, 0111, NULL);

	SAFE_TOUCH(DNAME_RX"/"DFNAME_R, 0444, NULL);
	SAFE_TOUCH(DNAME_RX"/"DFNAME_W, 0222, NULL);
	SAFE_TOUCH(DNAME_RX"/"DFNAME_X, 0111, NULL);

	SAFE_TOUCH(DNAME_WX"/"DFNAME_R, 0444, NULL);
	SAFE_TOUCH(DNAME_WX"/"DFNAME_W, 0222, NULL);
	SAFE_TOUCH(DNAME_WX"/"DFNAME_X, 0111, NULL);
}

static struct tst_test test = {
	.needs_tmpdir = 1,
	.needs_root = 1,
	.forks_child = 1,
	.setup = setup,
	.test = verify_access,
	.tcnt = ARRAY_SIZE(tcases),
};