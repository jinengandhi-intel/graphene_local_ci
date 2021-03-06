/*
 *
 *   Copyright (c) International Business Machines  Corp., 2001
 *
 *   This program is free software;  you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY;  without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
 *   the GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program;  if not, write to the Free Software
 *   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

/*
 * NAME
 * 	getpgid01.c
 *
 * DESCRIPTION
 *	Testcase to check the basic functionality of getpgid().
 *
 * ALGORITHM
 * 	block1: Does getpgid(0), and checks for error.
 * 	block2: Does getpgid(getpid()) and checks for error.
 * 	block3: Does getpgid(getppid()) and checks for error.
 * 	block4: Verifies that getpgid(getpgid(0)) == getpgid(0).
 * 	block5: Does getpgid(1) and checks for error.
 *
 * USAGE
 * 	getpgid01
 *
 * HISTORY
 *	07/2001 Ported by Wayne Boyer
 *
 * RESTRICTIONS
 *	Expects that there are no EPERM limitations on getting the
 *	process group ID from proc 1 (init).
 */
#define _GNU_SOURCE 1

#include <errno.h>
#include <unistd.h>
#include <stdarg.h>
#include <sys/wait.h>
#include <sys/types.h>
#include "test.h"

void setup(void);
void cleanup(void);

char *TCID = "getpgid01";
int TST_TOTAL = 1;

int main(int ac, char **av)
{
	int lc;

	register int pgid_0, pgid_1;
	register int my_pid, my_ppid;
	int ex_stat;

	tst_parse_opts(ac, av, NULL, NULL);

	setup();

	for (lc = 0; TEST_LOOPING(lc); lc++) {
		tst_count = 0;

		if ((pgid_0 = FORK_OR_VFORK()) == -1)
			tst_brkm(TBROK, cleanup, "fork failed");
		if (pgid_0 > 0) {
			while ((pgid_0 = wait(&ex_stat)) != -1) ;

			if (WEXITSTATUS(ex_stat) == 0)
				tst_resm(TPASS, "%s PASSED", TCID);
			else
				tst_resm(TINFO, "%s FAILED", TCID);

			exit(0);
		}

		if ((pgid_0 = getpgid(0)) == -1)
			tst_resm(TFAIL | TERRNO, "getpgid(0) failed");
		else
			tst_resm(TPASS, "getpgid(0) PASSED");

//block2:
		my_pid = getpid();
		if ((pgid_1 = getpgid(my_pid)) == -1)
			tst_resm(TFAIL | TERRNO, "getpgid(%d) failed", my_pid);

		if (pgid_0 != pgid_1) {
			tst_resm(TFAIL, "getpgid(my_pid=%d) != getpgid(0) "
				 "[%d != %d]", my_pid, pgid_1, pgid_0);
		} else
			tst_resm(TPASS, "getpgid(getpid()) PASSED");

//block3:
		my_ppid = getppid();
		if ((pgid_1 = getpgid(my_ppid)) == -1)
			tst_resm(TFAIL | TERRNO, "getpgid(%d) failed", my_ppid);

		if (pgid_0 != pgid_1) {
			tst_resm(TFAIL, "getpgid(%d) != getpgid(0) [%d != %d]",
				 my_ppid, pgid_1, pgid_0);
		} else
			tst_resm(TPASS, "getpgid(getppid()) PASSED");

//block4:
		if ((pgid_1 = getpgid(pgid_0)) < 0)
			tst_resm(TFAIL | TERRNO, "getpgid(%d) failed", pgid_0);

		if (pgid_0 != pgid_1) {
			tst_resm(TFAIL, "getpgid(%d) != getpgid(0) [%d != %d]",
				 pgid_0, pgid_1, pgid_0);
		} else
			tst_resm(TPASS, "getpgid(%d) PASSED", pgid_0);

//block5:
		if (getpgid(1) < 0)
			tst_resm(TFAIL | TERRNO, "getpgid(1) failed");
		else
			tst_resm(TPASS, "getpgid(1) PASSED");
	}
	cleanup();
	tst_exit();

}

void setup(void)
{

	tst_sig(FORK, DEF_HANDLER, cleanup);

	TEST_PAUSE;
}

void cleanup(void)
{
}
