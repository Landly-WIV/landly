from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from typing import List, Optional, Tuple
from src.backend import models
from geoalchemy2.functions import ST_Distance, ST_MakePoint
from geoalchemy2 import Geography

def search_bauern(
    db: Session,
    search: Optional[str] = None,
    max_distanz: Optional[float] = None,
    user_lat: Optional[float] = None,
    user_lon: Optional[float] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Tuple[models.Bauer, Optional[float]]]:
    """
    Sucht Bauern basierend auf verschiedenen Kriterien.
    
    Args:
        db: Database Session
        search: Suchbegriff für Firmenname oder Kontaktperson
        max_distanz: Maximale Entfernung in km (benötigt user_lat und user_lon)
        user_lat: Breitengrad des Nutzers
        user_lon: Längengrad des Nutzers
        skip: Anzahl zu überspringende Ergebnisse
        limit: Maximale Anzahl Ergebnisse
    
    Returns:
        Liste von Tupeln (Bauer, Entfernung in km) oder (Bauer, None) wenn keine Geo-Suche
    """
    # Basis-Query mit Eager Loading (lädt Ort und Standorte direkt mit, spart DB-Abfragen)
    query = db.query(models.Bauer).options(
        joinedload(models.Bauer.ort),
        joinedload(models.Bauer.standorte)
    )
    
    # Textsuche
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Bauer.firmenname.ilike(search_pattern),
                models.Bauer.kontaktperson.ilike(search_pattern)
            )
        )
    
    # Geografische Filterung über Standorte
    if max_distanz and user_lat is not None and user_lon is not None:
        # User-Position als PostGIS Point (Longitude, Latitude)
        user_point = ST_MakePoint(user_lon, user_lat)
        
        # Subquery: Finde Bauern mit Standorten in Reichweite
        # Gruppiert nach Bauer und nimmt jeweils die kürzeste Distanz
        standort_subquery = db.query(
            models.Standort.bauer_id,
            func.min(
                ST_Distance(
                    models.Standort.koordinate,  # Standort-Koordinate aus DB
                    func.cast(user_point, Geography)  # User-Position als Geography-Type
                )
            ).label('min_distance')  # Gibt Distanz in Metern zurück
        ).filter(
            # PostGIS ST_Distance arbeitet mit Metern, daher * 1000 für km→m Umrechnung
            ST_Distance(
                models.Standort.koordinate,
                func.cast(user_point, Geography)
            ) <= max_distanz * 1000  # Nur Standorte innerhalb max_distanz (in Metern)
        ).group_by(models.Standort.bauer_id).subquery()
        
        # Join mit Subquery und füge Distanz-Spalte hinzu
        query = query.join(
            standort_subquery,
            models.Bauer.bauer_id == standort_subquery.c.bauer_id
        ).add_columns(
            (standort_subquery.c.min_distance / 1000.0).label('distanz_km')  # Meter → Kilometer
        ).order_by(standort_subquery.c.min_distance)  # Sortiere nach nächstem zuerst
        
        results = query.offset(skip).limit(limit).all()
        # Rückgabe: Liste von Tupeln (Bauer-Objekt, Entfernung in km)
        return [(bauer, round(distanz, 2)) for bauer, distanz in results]
    
    # Ohne Geo-Filter: Rückgabe ohne Distanz-Info (None statt km)
    bauern = query.offset(skip).limit(limit).all()
    return [(bauer, None) for bauer in bauern]


def get_bauer_with_products(
    db: Session,
    bauer_id: int
) -> Optional[models.Bauer]:
    """
    Holt einen Bauern mit allen Produkten und Details.
    
    Args:
        db: Database Session
        bauer_id: ID des Bauern
    
    Returns:
        Bauer mit Produkten oder None
    """
    # Eager Loading: Lädt Bauer mit allen Relations in einem Query (keine N+1 Probleme)
    return db.query(models.Bauer).options(
        joinedload(models.Bauer.ort),  # Ort des Bauern
        joinedload(models.Bauer.produkte).joinedload(models.Produkt.produktart),  # Produkte + Produktart
        joinedload(models.Bauer.produkte).joinedload(models.Produkt.labels),  # Produkte + Labels
        joinedload(models.Bauer.standorte).joinedload(models.Standort.ort)  # Standorte + deren Orte
    ).filter(models.Bauer.bauer_id == bauer_id).first()


def get_produkte_by_bauer(
    db: Session,
    bauer_id: int,
    produktart_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.Produkt]:
    """
    Holt alle Produkte eines bestimmten Bauern.
    
    Args:
        db: Database Session
        bauer_id: ID des Bauern
        produktart_id: Optional - Filter nach Produktart
        skip: Anzahl zu überspringende Ergebnisse
        limit: Maximale Anzahl Ergebnisse
    
    Returns:
        Liste von Produkten
    """
    query = db.query(models.Produkt).options(
        joinedload(models.Produkt.produktart),
        joinedload(models.Produkt.labels)
    ).filter(models.Produkt.bauern_id == bauer_id)
    
    if produktart_id:
        query = query.filter(models.Produkt.produktart_id == produktart_id)
    
    return query.offset(skip).limit(limit).all()


def get_standorte_by_bauer(
    db: Session,
    bauer_id: int
) -> List[models.Standort]:
    """
    Holt alle Standorte eines Bauern.
    
    Args:
        db: Database Session
        bauer_id: ID des Bauern
    
    Returns:
        Liste von Standorten
    """
    return db.query(models.Standort).options(
        joinedload(models.Standort.ort)
    ).filter(models.Standort.bauer_id == bauer_id).all()


def get_nearest_bauern(
    db: Session,
    user_lat: float,
    user_lon: float,
    limit: int = 10
) -> List[Tuple[models.Bauer, float]]:
    """
    Findet die nächsten Bauern basierend auf User-Position.
    
    Args:
        db: Database Session
        user_lat: Breitengrad des Nutzers
        user_lon: Längengrad des Nutzers
        limit: Anzahl der nächsten Bauern
    
    Returns:
        Liste von Tupeln (Bauer, Entfernung in km), sortiert nach Entfernung
    """
    # User-Position als PostGIS Point
    user_point = ST_MakePoint(user_lon, user_lat)
    
    # Subquery: Finde kürzeste Distanz pro Bauer
    # Warum Subquery? Ein Bauer kann mehrere Standorte haben - wir wollen nur den nächsten
    standort_distances = db.query(
        models.Standort.bauer_id,
        func.min(  # Nimm den nächstgelegenen Standort pro Bauer
            ST_Distance(
                models.Standort.koordinate,
                func.cast(user_point, Geography)
            )
        ).label('min_distance')  # In Metern
    ).group_by(models.Standort.bauer_id).subquery()
    
    # Bauern mit Distanz: Join Bauer-Tabelle mit Distanz-Subquery
    results = db.query(
        models.Bauer,
        (standort_distances.c.min_distance / 1000.0).label('distanz_km')  # Meter → km
    ).join(
        standort_distances,
        models.Bauer.bauer_id == standort_distances.c.bauer_id
    ).options(
        joinedload(models.Bauer.ort)  # Lade Ort mit
    ).order_by(
        standort_distances.c.min_distance  # Sortiere: nächster zuerst
    ).limit(limit).all()
    
    # Rückgabe: [(Bauer, Distanz in km)], gerundet auf 2 Dezimalstellen
    return [(bauer, round(distanz, 2)) for bauer, distanz in results]


def count_bauern(
    db: Session,
    search: Optional[str] = None
) -> int:
    """
    Zählt Bauern basierend auf Suchkriterien.
    
    Args:
        db: Database Session
        search: Suchbegriff für Firmenname oder Kontaktperson
    
    Returns:
        Anzahl der gefundenen Bauern
    """
    query = db.query(func.count(models.Bauer.bauer_id))
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Bauer.firmenname.ilike(search_pattern),
                models.Bauer.kontaktperson.ilike(search_pattern)
            )
        )
    
    return query.scalar()
