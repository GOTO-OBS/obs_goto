from lsst.pipe.tasks.colorterms import Colorterm, ColortermDict

config.data = {
    "ps1*": ColortermDict(data={
        "L": Colorterm(primary="g", secondary="r", c0=0.335, c1=-0.4579, c2=-0.0767),
        "R": Colorterm(primary="r", secondary="i", c0=0.1071, c1=-0.02849, c2=0.002471)
})}
