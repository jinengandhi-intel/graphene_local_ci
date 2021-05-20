// SPDX-License-Identifier: GPL-2.0-or-later
/* Copyright (c) International Business Machines  Corp., 2001
 *	07/2001 John George
 *		-Ported
 *
 * check stat() with various error conditions that should produce
 * EACCES, EFAULT, ENAMETOOLONG,  ENOENT, ENOTDIR, ELOOP
 */

#include <fcntl.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <pwd.h>
#include "tst_test.h"

#define TST_EACCES_DIR   "/tmp/tst_eaccesdir"
#define TST_EACCES_FILE  "/tmp/tst_eaccesdir/tst"
#define TST_ENOENT       "/tmp/tst_enoent/tst"
#define TST_ENOTDIR_DIR  "/tmp/tst_enotdir/tst"
#define TST_ENOTDIR_FILE "/tmp/tst_enotdir"

#define MODE_RW	        0666
#define DIR_MODE        0755

struct passwd *ltpuser;

static char long_dir[PATH_MAX + 2] = {[0 ... PATH_MAX + 1] = 'a'};
static char loop_dir[PATH_MAX] = ".";

static struct tcase{
	char *pathname;
	int exp_errno;
} TC[] = {
	{TST_EACCES_FILE, EACCES}
};

static void verify_stat(unsigned int n)
{
    tst_res(TPASS, "No Test function defined");
}

static void setup(void)
{
	unsigned int i;

	ltpuser = SAFE_GETPWNAM("nobody");
	SAFE_SETUID(ltpuser->pw_uid);

	SAFE_MKDIR(TST_EACCES_DIR, DIR_MODE);
	SAFE_TOUCH(TST_EACCES_FILE, DIR_MODE, NULL);
	SAFE_CHMOD(TST_EACCES_DIR, MODE_RW);

	SAFE_TOUCH(TST_ENOTDIR_FILE, DIR_MODE, NULL);

	SAFE_MKDIR("/tmp/test_eloop", DIR_MODE);
	SAFE_SYMLINK("/tmp/test_eloop/test_eloop", "/tmp/test_eloop/test_eloop");
}

static struct tst_test test = {
	.tcnt = ARRAY_SIZE(TC),
	.needs_tmpdir = 1,
	.setup = setup,
	.test = verify_stat,
};
