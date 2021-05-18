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
	{FNAME_RWX, X_OK, "X_OK", 0, 3},
	{FNAME_RWX, W_OK, "W_OK", 0, 3},
	{FNAME_RWX, R_OK, "R_OK", 0, 3},

	{FNAME_RWX, R_OK|W_OK, "R_OK|W_OK", 0, 3},
	{FNAME_RWX, R_OK|X_OK, "R_OK|X_OK", 0, 3},
	{FNAME_RWX, W_OK|X_OK, "W_OK|X_OK", 0, 3},
	{FNAME_RWX, R_OK|W_OK|X_OK, "R_OK|W_OK|X_OK", 0, 3},

	{FNAME_X, X_OK, "X_OK", 0, 3},
	{FNAME_W, W_OK, "W_OK", 0, 3},
	{FNAME_R, R_OK, "R_OK", 0, 3},

	{FNAME_R, X_OK, "X_OK", EACCES, 3},
	// {FNAME_R, W_OK, "W_OK", EACCES, 1},
	// {FNAME_W, R_OK, "R_OK", EACCES, 1},
	{FNAME_W, X_OK, "X_OK", EACCES, 3},
	// {FNAME_X, R_OK, "R_OK", EACCES, 1},
	// {FNAME_X, W_OK, "W_OK", EACCES, 1},

	{FNAME_R, W_OK|X_OK, "W_OK|X_OK", EACCES, 3},
	{FNAME_R, R_OK|X_OK, "R_OK|X_OK", EACCES, 3},
	// {FNAME_R, R_OK|W_OK, "R_OK|W_OK", EACCES, 1},
	{FNAME_R, R_OK|W_OK|X_OK, "R_OK|W_OK|X_OK", EACCES, 3},

	{FNAME_W, W_OK|X_OK, "W_OK|X_OK", EACCES, 3},
	{FNAME_W, R_OK|X_OK, "R_OK|X_OK", EACCES, 3},
	// {FNAME_W, R_OK|W_OK, "R_OK|W_OK", EACCES, 1},
	{FNAME_W, R_OK|W_OK|X_OK, "R_OK|W_OK|X_OK", EACCES, 3},

	// {FNAME_X, W_OK|X_OK, "W_OK|X_OK", EACCES, 1},
	// {FNAME_X, R_OK|X_OK, "R_OK|X_OK", EACCES, 1},
	// {FNAME_X, R_OK|W_OK, "R_OK|W_OK", EACCES, 1},
	// {FNAME_X, R_OK|W_OK|X_OK, "R_OK|W_OK|X_OK", EACCES, 1},

	// {FNAME_R, W_OK, "W_OK", 0, 2},
	// {FNAME_R, R_OK|W_OK, "R_OK|W_OK", 0, 2},

	// {FNAME_W, R_OK, "R_OK", 0, 2},
	// {FNAME_W, R_OK|W_OK, "R_OK|W_OK", 0, 2},

	// {FNAME_X, R_OK, "R_OK", 0, 2},
	// {FNAME_X, W_OK, "W_OK", 0, 2},
	// {FNAME_X, R_OK|W_OK, "R_OK|W_OK", 0, 2},

	// {DNAME_R"/"DFNAME_R, F_OK, "F_OK", 0, 2},
	// {DNAME_R"/"DFNAME_R, R_OK, "R_OK", 0, 2},
	// {DNAME_R"/"DFNAME_R, W_OK, "W_OK", 0, 2},

	// {DNAME_R"/"DFNAME_W, F_OK, "F_OK", 0, 2},
	// {DNAME_R"/"DFNAME_W, R_OK, "R_OK", 0, 2},
	// {DNAME_R"/"DFNAME_W, W_OK, "W_OK", 0, 2},

	// {DNAME_R"/"DFNAME_X, F_OK, "F_OK", 0, 2},
	// {DNAME_R"/"DFNAME_X, R_OK, "R_OK", 0, 2},
	// {DNAME_R"/"DFNAME_X, W_OK, "W_OK", 0, 2},
	// {DNAME_R"/"DFNAME_X, X_OK, "X_OK", 0, 2},

	// {DNAME_W"/"DFNAME_R, F_OK, "F_OK", 0, 2},
	// {DNAME_W"/"DFNAME_R, R_OK, "R_OK", 0, 2},
	// {DNAME_W"/"DFNAME_R, W_OK, "W_OK", 0, 2},

	// {DNAME_W"/"DFNAME_W, F_OK, "F_OK", 0, 2},
	// {DNAME_W"/"DFNAME_W, R_OK, "R_OK", 0, 2},
	// {DNAME_W"/"DFNAME_W, W_OK, "W_OK", 0, 2},

	// {DNAME_W"/"DFNAME_X, F_OK, "F_OK", 0, 2},
	// {DNAME_W"/"DFNAME_X, R_OK, "R_OK", 0, 2},
	// {DNAME_W"/"DFNAME_X, W_OK, "W_OK", 0, 2},
	// {DNAME_W"/"DFNAME_X, X_OK, "X_OK", 0, 2},

	{DNAME_X"/"DFNAME_R, F_OK, "F_OK", 0, 3},
	{DNAME_X"/"DFNAME_R, R_OK, "R_OK", 0, 3},
	// {DNAME_X"/"DFNAME_R, W_OK, "W_OK", 0, 2},

	{DNAME_X"/"DFNAME_W, F_OK, "F_OK", 0, 3},
	// {DNAME_X"/"DFNAME_W, R_OK, "R_OK", 0, 2},
	{DNAME_X"/"DFNAME_W, W_OK, "W_OK", 0, 3},

	{DNAME_X"/"DFNAME_X, F_OK, "F_OK", 0, 3},
	// {DNAME_X"/"DFNAME_X, R_OK, "R_OK", 0, 2},
	// {DNAME_X"/"DFNAME_X, W_OK, "W_OK", 0, 2},
	{DNAME_X"/"DFNAME_X, X_OK, "X_OK", 0, 3},

	// {DNAME_RW"/"DFNAME_R, F_OK, "F_OK", 0, 2},
	// {DNAME_RW"/"DFNAME_R, R_OK, "R_OK", 0, 2},
	// {DNAME_RW"/"DFNAME_R, W_OK, "W_OK", 0, 2},

	// {DNAME_RW"/"DFNAME_W, F_OK, "F_OK", 0, 2},
	// {DNAME_RW"/"DFNAME_W, R_OK, "R_OK", 0, 2},
	// {DNAME_RW"/"DFNAME_W, W_OK, "W_OK", 0, 2},

	// {DNAME_RW"/"DFNAME_X, F_OK, "F_OK", 0, 2},
	// {DNAME_RW"/"DFNAME_X, R_OK, "R_OK", 0, 2},
	// {DNAME_RW"/"DFNAME_X, W_OK, "W_OK", 0, 2},
	// {DNAME_RW"/"DFNAME_X, X_OK, "X_OK", 0, 2},

	{DNAME_RX"/"DFNAME_R, F_OK, "F_OK", 0, 3},
	{DNAME_RX"/"DFNAME_R, R_OK, "R_OK", 0, 3},
	// {DNAME_RX"/"DFNAME_R, W_OK, "W_OK", 0, 2},

	{DNAME_RX"/"DFNAME_W, F_OK, "F_OK", 0, 3},
	// {DNAME_RX"/"DFNAME_W, R_OK, "R_OK", 0, 2},
	{DNAME_RX"/"DFNAME_W, W_OK, "W_OK", 0, 3},

	{DNAME_RX"/"DFNAME_X, F_OK, "F_OK", 0, 3},
	// {DNAME_RX"/"DFNAME_X, R_OK, "R_OK", 0, 2},
	// {DNAME_RX"/"DFNAME_X, W_OK, "W_OK", 0, 2},
	{DNAME_RX"/"DFNAME_X, X_OK, "X_OK", 0, 3},

	{DNAME_WX"/"DFNAME_R, F_OK, "F_OK", 0, 3},
	{DNAME_WX"/"DFNAME_R, R_OK, "R_OK", 0, 3},
	// {DNAME_WX"/"DFNAME_R, W_OK, "W_OK", 0, 2},

	{DNAME_WX"/"DFNAME_W, F_OK, "F_OK", 0, 3},
	// {DNAME_WX"/"DFNAME_W, R_OK, "R_OK", 0, 2},
	{DNAME_WX"/"DFNAME_W, W_OK, "W_OK", 0, 3},

	{DNAME_WX"/"DFNAME_X, F_OK, "F_OK", 0, 3},
	// {DNAME_WX"/"DFNAME_X, R_OK, "R_OK", 0, 2},
	// {DNAME_WX"/"DFNAME_X, W_OK, "W_OK", 0, 2},
	{DNAME_WX"/"DFNAME_X, X_OK, "X_OK", 0, 3},

	// {DNAME_R"/"DFNAME_R, F_OK, "F_OK", EACCES, 1},
	// {DNAME_R"/"DFNAME_R, R_OK, "R_OK", EACCES, 1},
	// {DNAME_R"/"DFNAME_R, W_OK, "W_OK", EACCES, 1},
	{DNAME_R"/"DFNAME_R, X_OK, "X_OK", EACCES, 3},

	// {DNAME_R"/"DFNAME_W, F_OK, "F_OK", EACCES, 1},
	// {DNAME_R"/"DFNAME_W, R_OK, "R_OK", EACCES, 1},
	// {DNAME_R"/"DFNAME_W, W_OK, "W_OK", EACCES, 1},
	{DNAME_R"/"DFNAME_W, X_OK, "X_OK", EACCES, 3},

	// {DNAME_R"/"DFNAME_X, F_OK, "F_OK", EACCES, 1},
	// {DNAME_R"/"DFNAME_X, R_OK, "R_OK", EACCES, 1},
	// {DNAME_R"/"DFNAME_X, W_OK, "W_OK", EACCES, 1},
	// {DNAME_R"/"DFNAME_X, X_OK, "X_OK", EACCES, 1},

	// {DNAME_W"/"DFNAME_R, F_OK, "F_OK", EACCES, 1},
	// {DNAME_W"/"DFNAME_R, R_OK, "R_OK", EACCES, 1},
	// {DNAME_W"/"DFNAME_R, W_OK, "W_OK", EACCES, 1},
	{DNAME_W"/"DFNAME_R, X_OK, "X_OK", EACCES, 3},

	// {DNAME_W"/"DFNAME_W, F_OK, "F_OK", EACCES, 1},
	// {DNAME_W"/"DFNAME_W, R_OK, "R_OK", EACCES, 1},
	// {DNAME_W"/"DFNAME_W, W_OK, "W_OK", EACCES, 1},
	{DNAME_W"/"DFNAME_W, X_OK, "X_OK", EACCES, 3},

	// {DNAME_W"/"DFNAME_X, F_OK, "F_OK", EACCES, 1},
	// {DNAME_W"/"DFNAME_X, R_OK, "R_OK", EACCES, 1},
	// {DNAME_W"/"DFNAME_X, W_OK, "W_OK", EACCES, 1},
	// {DNAME_W"/"DFNAME_X, X_OK, "X_OK", EACCES, 1},

	// {DNAME_X"/"DFNAME_R, W_OK, "W_OK", EACCES, 1},
	{DNAME_X"/"DFNAME_R, X_OK, "X_OK", EACCES, 3},

	// {DNAME_X"/"DFNAME_W, R_OK, "R_OK", EACCES, 1},
	{DNAME_X"/"DFNAME_W, X_OK, "X_OK", EACCES, 3},

	// {DNAME_X"/"DFNAME_X, R_OK, "R_OK", EACCES, 1},
	// {DNAME_X"/"DFNAME_X, W_OK, "W_OK", EACCES, 1},

	// {DNAME_RW"/"DFNAME_R, F_OK, "F_OK", EACCES, 1},
	// {DNAME_RW"/"DFNAME_R, R_OK, "R_OK", EACCES, 1},
	// {DNAME_RW"/"DFNAME_R, W_OK, "W_OK", EACCES, 1},
	{DNAME_RW"/"DFNAME_R, X_OK, "X_OK", EACCES, 3},

	// {DNAME_RW"/"DFNAME_W, F_OK, "F_OK", EACCES, 1},
	// {DNAME_RW"/"DFNAME_W, R_OK, "R_OK", EACCES, 1},
	// {DNAME_RW"/"DFNAME_W, W_OK, "W_OK", EACCES, 1},
	{DNAME_RW"/"DFNAME_W, X_OK, "X_OK", EACCES, 3},

	// {DNAME_RW"/"DFNAME_X, F_OK, "F_OK", EACCES, 1},
	// {DNAME_RW"/"DFNAME_X, R_OK, "R_OK", EACCES, 1},
	// {DNAME_RW"/"DFNAME_X, W_OK, "W_OK", EACCES, 1},
	// {DNAME_RW"/"DFNAME_X, X_OK, "X_OK", EACCES, 1},

	// {DNAME_RX"/"DFNAME_R, W_OK, "W_OK", EACCES, 1},
	{DNAME_RX"/"DFNAME_R, X_OK, "X_OK", EACCES, 3},

	// {DNAME_RX"/"DFNAME_W, R_OK, "R_OK", EACCES, 1},
	{DNAME_RX"/"DFNAME_W, X_OK, "X_OK", EACCES, 3},

	// {DNAME_RX"/"DFNAME_X, R_OK, "R_OK", EACCES, 1},
	// {DNAME_RX"/"DFNAME_X, W_OK, "W_OK", EACCES, 1},

	// {DNAME_WX"/"DFNAME_R, W_OK, "W_OK", EACCES, 1},
	{DNAME_WX"/"DFNAME_R, X_OK, "X_OK", EACCES, 3},

	// {DNAME_WX"/"DFNAME_W, R_OK, "R_OK", EACCES, 1},
	{DNAME_WX"/"DFNAME_W, X_OK, "X_OK", EACCES, 3},

	// {DNAME_WX"/"DFNAME_X, R_OK, "R_OK", EACCES, 1},
	// {DNAME_WX"/"DFNAME_X, W_OK, "W_OK", EACCES, 1}
};

static void verify_success(struct tcase *tc, const char *user)
{
	if (TST_RET == -1) {
		tst_res(TFAIL | TTERRNO,
		        "access(%s, %s) as %s failed unexpectedly",
		        tc->fname, tc->name, user);
		return;
	}

	tst_res(TPASS, "access(%s, %s) as %s", tc->fname, tc->name, user);
}

static void verify_failure(struct tcase *tc, const char *user)
{
	if (TST_RET != -1) {
		tst_res(TFAIL, "access(%s, %s) as %s succeded unexpectedly",
		        tc->fname, tc->name, user);
		return;
	}

	if (TST_ERR != tc->exp_errno) {
		tst_res(TFAIL | TTERRNO,
		        "access(%s, %s) as %s should fail with %s",
		        tc->fname, tc->name, user,
		        tst_strerrno(tc->exp_errno));
		return;
	}

	tst_res(TPASS | TTERRNO, "access(%s, %s) as %s",
	        tc->fname, tc->name, user);
}

static void access_test(struct tcase *tc, const char *user)
{
	TEST(access(tc->fname, tc->mode));

	if (tc->exp_errno)
		verify_failure(tc, user);
	else
		verify_success(tc, user);
}

static void verify_access(unsigned int n)
{
	struct tcase *tc = tcases + n;
	pid_t pid;

	if (tc->exp_user & 0x02)
		access_test(tc, "root");

	if (tc->exp_user & 0x01) {
		pid = SAFE_FORK();
		if (pid) {
			SAFE_WAITPID(pid, NULL, 0);
		} else {
			SAFE_SETUID(uid);
			access_test(tc, "nobody");
		}
	}
}

static void setup(void)
{
	struct passwd *pw;

	umask(0022);

	pw = SAFE_GETPWNAM("nobody");

	uid = pw->pw_uid;
}

static struct tst_test test = {
	.needs_tmpdir = 1,
	.needs_root = 1,
	.forks_child = 1,
	.setup = setup,
	.test = verify_access,
	.tcnt = ARRAY_SIZE(tcases),
};
