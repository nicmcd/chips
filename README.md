# chips
A database and plotter for historic router chips

The "chips.py" program maintains the database (as a text file). It also plots the results.

To see all chips and values run this:
```bash
./chips.py show
```

To generate a plot, view it, then save it, run this:
```bash
./chips.py plot --view chips.png
```

If you have more results, please use the chips.py program to add more entries to the database:
```bash
./chips.py add <company> <chipname> <year> <bandwidth>
```

Don't forget to submit a pull request so we can unify our database!