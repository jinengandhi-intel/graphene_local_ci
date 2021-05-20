// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * Copyright (C) 2013 Red Hat, Inc.
 *
 * Basic tests for open(2) and make sure open(2) works and handles error
 * conditions correctly.
 *
 * There are 28 test cases:
 * 1. Open regular file O_RDONLY
 * 2. Open regular file O_WRONLY
 * 3. Open regular file O_RDWR
 * 4. Open regular file O_RDWR | O_SYNC
 * 5. Open regular file O_RDWR | O_TRUNC
 * 6. Open dir O_RDONLY
 * 7. Open dir O_RDWR, expect EISDIR
 * 8. Open regular file O_DIRECTORY, expect ENOTDIR
 * 9. Open hard link file O_RDONLY
 * 10. Open hard link file O_WRONLY
 * 11. Open hard link file O_RDWR
 * 12. Open sym link file O_RDONLY
 * 13. Open sym link file O_WRONLY
 * 14. Open sym link file O_RDWR
 * 15. Open sym link dir O_RDONLY
 * 16. Open sym link dir O_WRONLY, expect EISDIR
 * 17. Open sym link dir O_RDWR, expect EISDIR
 * 18. Open device special file O_RDONLY
 * 19. Open device special file O_WRONLY
 * 20. Open device special file O_RDWR
 * 21. Open non-existing regular file in existing dir
 * 22. Open link file O_RDONLY | O_CREAT
 * 23. Open symlink file O_RDONLY | O_CREAT
 * 24. Open regular file O_RDONLY | O_CREAT
 * 25. Open symlink dir O_RDONLY | O_CREAT, expect EISDIR
 * 26. Open dir O_RDONLY | O_CREAT, expect EISDIR
 * 27. Open regular file O_RDONLY | O_TRUNC, behaviour is undefined but should
 *     not oops or hang
 * 28. Open regular file(non-empty) O_RDONLY | O_TRUNC, behaviour is undefined
 *     but should not oops or hang
 */

#define _GNU_SOURCE
#include <errno.h>
#include <sys/sysmacros.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include "tst_test.h"

#define MNTPOINT "/tmp/mntpoint"
#define T_REG "/tmp/t_reg"			/* regular file with content */
#define T_REG_EMPTY "/tmp/t_reg_empty"	/* empty regular file */
#define T_LINK_REG "/tmp/t_link_reg"		/* hard link to T_REG */
#define T_NEW_REG "t_new_reg"		/* new regular file to be created */
#define T_SYMLINK_REG "/tmp/t_symlink_reg"	/* symlink to T_REG */
#define T_DIR "/tmp/t_dir"			/* test dir */
#define T_SYMLINK_DIR "/tmp/t_symlink_dir"	/* symlink to T_DIR */
#define T_DEV MNTPOINT"/t_dev"		/* test device special file */

#define T_MSG "this is a test string"

static struct test_case {
	char *desc;
	char *path;
	int flags;
	mode_t mode;
	int err;
} tc[] = {
	/* Test open(2) regular file */
	{	/* open regular file O_RDONLY */
		.desc = "Open regular file O_RDONLY",
		.path = T_REG_EMPTY,
		.flags = O_RDONLY,
		.mode = 0644,
		.err = 0,
	},
};

static void verify_open(unsigned int n)
{
	tst_res(TPASS, "No Test function defined");
}

static void setup(void)
{
	int fd;
	int ret;

	fd = SAFE_OPEN(T_REG, O_WRONLY | O_CREAT, 0644);
	ret = write(fd, T_MSG, sizeof(T_MSG));
	if (ret == -1) {
		SAFE_CLOSE(fd);
		tst_brk(TBROK | TERRNO, "Write %s failed", T_REG);
	}
	SAFE_CLOSE(fd);

	SAFE_TOUCH(T_REG_EMPTY, 0644, NULL);
	SAFE_LINK(T_REG, T_LINK_REG);
	SAFE_SYMLINK(T_REG, T_SYMLINK_REG);
	SAFE_MKDIR(T_DIR, 0755);
	SAFE_SYMLINK(T_DIR, T_SYMLINK_DIR);
	SAFE_MKNOD(T_DEV, S_IFCHR, makedev(1, 5));
}

static struct tst_test test = {
	.tcnt = ARRAY_SIZE(tc),
	.setup = setup,
	.test = verify_open,
	.needs_devfs = 1,
	.mntpoint = MNTPOINT,
};
