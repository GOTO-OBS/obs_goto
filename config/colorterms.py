from lsst.pipe.tasks.colorterms import Colorterm, ColortermDict

config.data = {
    "ps1*": ColortermDict(data={
        "L": Colorterm(primary="g", secondary="r", c0=0.247, c1=-0.3516, c2=-0.1765),
        "R": Colorterm(primary="r", secondary="i", c0=0.09538, c1=-0.1455, c2=0.08284)
        "G": Colorterm(primary="g", secondary="r", c0=0.1872, c1=-0.3178, c2=-0.06752)
        "B": Colorterm(primary="g", secondary="r", c0=-0.0578, c1=0.283, c2=-0.007889)
})}
