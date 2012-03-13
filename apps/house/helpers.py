from house.models import Klub, Posel, Posiedzenie, Punkt, Glosowanie

def update():
    Klub.update()
    Posel.update()
    Posiedzenie.update()
    Punkt.update()
    Glosowanie.update()
