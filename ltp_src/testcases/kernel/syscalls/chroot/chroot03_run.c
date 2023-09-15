// SPDX-License-Identifier: GPL-2.0-or-later
/*
 *   Copyright (c) International Business Machines  Corp., 2001
 *
 *	 07/2001 Ported by Wayne Boyer
 */

/*\
 * [Description]
 *
 * Testcase to test whether chroot(2) sets errno correctly.
 *
 * - to test whether chroot() is setting ENAMETOOLONG if the
 *   pathname is more than VFS_MAXNAMELEN.
 * - to test whether chroot() is setting ENOTDIR if the argument
 *   is not a directory.
 * - to test whether chroot() is setting ENOENT if the directory
 *   does not exist.
 * - attempt to chroot to a path pointing to an invalid address
 *   and expect EFAULT as errno.
 * - to test whether chroot() is setting ELOOP if the two
 *   symbolic directory who point to each other.
 */

#include <stdio.h>
#include "tst_test.h"

static char fname[255] = "/tmp/chroot03_file";
static char nonexistent_dir[100] = "/tmp/chroot03_dir";
static char bad_dir[] = "/tmp/abcdefghijklmnopqrstmnopqrstuvwxyzabcdefghijklmnopqrstmnopqrstuvwxyzabcdefghijklmnopqrstmnopqrstuvwxyzabcdefghijklmnopqrstmnopqrstuvwxyzabcdefghijklmnopqrstmnopqrstuvwxyzabcdefghijklmnopqrstmnopqrstuvwxyzabcdefghijklmnopqrstmnopqrstuvwxyzabcdefghijklmnopqrstmnopqrstuvwxyz";
static char symbolic_dir[] = "/tmp/sym_dir1";

static struct tcase {
	char *dir;
	int error;
	char *desc;
} tcases[] = {
	{bad_dir, ENAMETOOLONG, "chroot(longer than VFS_MAXNAMELEN)"},
	{fname, ENOTDIR, "chroot(not a directory)"},
	{nonexistent_dir, ENOENT, "chroot(does not exists)"},
	{(char *)-1, EFAULT, "chroot(an invalid address)"},
	{symbolic_dir, ELOOP, "chroot(symlink loop)"}
};

static void verify_chroot(unsigned int n)
{
	struct tcase *tc = &tcases[n];

	TST_EXP_FAIL(chroot(tc->dir), tc->error, "%s", tc->desc);
}

static void setup(void)
{}

static struct tst_test test = {
	.setup = setup,
	.tcnt = ARRAY_SIZE(tcases),
	.test = verify_chroot,
	// .needs_tmpdir = 1,
};
