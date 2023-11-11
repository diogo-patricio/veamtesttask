# veeamtesttask

Periodically synchronise a replica of a folder.

This project is an implementation of program for a tesk task for a Veeam Software recruitment process.

The task discription can be found [here](Internal%20Development%20in%20QA%20(SDET)%20Team_tesk%20task.pdf).

## Tasks and improvements
- [ ] Properly handle symlinks. Currently they are ignored.
- [ ] Change timing mechanism. Currently the interval only starts after the copy process ends and not at a precise interval.
- [ ] Extend tests:
  - [ ] Check possible directory cycles, such as syncing to a subdirectory.
  - [ ] Check metadata
  - [ ] Check permissions
- [ ] Improve testing tooling. Perhaps look into using some testing framework like [Pytest](https://docs.pytest.org/en/)
- [ ] Decide on a consistent code style. Maybe adopt [PEP 8](https://peps.python.org/pep-0008/).
